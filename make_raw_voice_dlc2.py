import os
import gradio as gr
import utils
import argparse
import commons

import yaml
from models import SynthesizerTrn
from text import text_to_sequence
import torch
from torch import no_grad, LongTensor
import soundfile as sf
from pydub import AudioSegment
import shutil
import tqdm

audio_postprocess_ori = gr.Audio.postprocess
limitation = os.getenv("SYSTEM") == "spaces"  # limit text and audio length in huggingface spaces

parser = argparse.ArgumentParser()
parser.add_argument('--device', type=str, default='cpu')
parser.add_argument('--lang', type=str, default='zh', choices=['zh', 'ja'])
parser.add_argument('--log', type=str, default='', help='xxx.exceed.json, only process those words')
parser.add_argument('-n', default='biker', type=str, choices=['biker', 'teengirl', 'manager', 'namvet'])
args = parser.parse_args()

device = torch.device(args.device)

hps_ms = utils.get_hparams_from_file(r'./model/config.json')
net_g_ms = SynthesizerTrn(
    len(hps_ms.symbols),
    hps_ms.data.filter_length // 2 + 1,
    hps_ms.train.segment_size // hps_ms.data.hop_length,
    n_speakers=hps_ms.data.n_speakers,
    **hps_ms.model)
_ = net_g_ms.eval().to(device)
speakers = hps_ms.speakers
model, optimizer, learning_rate, epochs = utils.load_checkpoint(r'./model/G_953000.pth', net_g_ms, None)

def get_text(text, hps):
    text_norm, clean_text = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm, clean_text

def vits(text, language, speaker_id, noise_scale, noise_scale_w, length_scale):
    if not len(text):
        return "输入文本不能为空！", None, None
    text = text.replace('\n', ' ').replace('\r', '').replace(" ", "")
    if len(text) > 100 and limitation:
        return f"输入文字过长！{len(text)}>100", None, None
    if language == 0:
        text = f"[ZH]{text}[ZH]"
    elif language == 1:
        text = f"[JA]{text}[JA]"
    else:
        text = f"{text}"
    stn_tst, clean_text = get_text(text, hps_ms)
    with no_grad():
        x_tst = stn_tst.unsqueeze(0).to(device)
        x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
        speaker_id = LongTensor([speaker_id]).to(device)
        # tensor([132]) 0.1 0.668 1.1
        audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=speaker_id, noise_scale=noise_scale, noise_scale_w=noise_scale_w,
                               length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()

    return 22050, audio

def get_make_list(transcription: dict, log: str) -> list:
    if not os.path.exists(log):
        return list(transcription.keys())
    else:
        data = utils.read_json(log)
        return list(data.keys())


lang_code = {
    'zh': 0,
    'ja': 1
}

if __name__ == '__main__':
    name: str = args.n
    lang: str = args.lang
    log: str = args.log

    lang_code: int = lang_code[lang]

    transcription = utils.read_json(f'transcription/dlc1/{name}_{lang}.json')
    meta_data = utils.read_json(f'transcription/dlc1/{name}.meta.json')
    
    with open(f'./config/voice_{lang}.yaml', 'r', encoding='utf-8') as fp:
        config = yaml.load(fp, Loader=yaml.FullLoader)
    
    mod_root = os.path.join('dlc2_dist', config[name]['mod_name'])
    root = os.path.join(mod_root, 'sound', 'player', 'survivor', 'voice', name)
    
    # if os.path.exists(mod_root):
    #     shutil.rmtree(mod_root)
    if not os.path.exists(root):
        os.makedirs(root)
        
    default_config = config[name]['config']
    speaker_id, noise_scale, noise_scale_w, length_scale = default_config

    make_list = get_make_list(transcription, log)

    for wave_file in make_list:
        assert wave_file in meta_data, 'meta_data is broken, {} not in'.format(wave_file)

    print('generate raw voice')
    for wave_file in tqdm.tqdm(make_list):
        target_file = os.path.join(root, wave_file)
        words = transcription[wave_file].strip()
        assert len(words) > 0, '{} words is blank'.format(wave_file) 
        sr, audio = vits(words, lang_code, speaker_id, noise_scale, noise_scale_w, length_scale)
        sf.write(target_file, audio, samplerate=sr)
    
    print('scale audio that lasts too long partly')
    for wave_file in tqdm.tqdm(make_list):
        target_file = os.path.join(root, wave_file)
        words = transcription[wave_file].strip()
        gen_audio: AudioSegment = AudioSegment.from_file(target_file)
        
        expect_len = meta_data[wave_file]['length']
        gen_len = len(gen_audio)
        if gen_len > expect_len:
            scale_ratio = expect_len / gen_len
            new_noise_scale_w = max(0.1, noise_scale_w * scale_ratio - 0.1)
            new_length_scale = length_scale * scale_ratio
            sr, audio = vits(words, lang_code, speaker_id, noise_scale, new_noise_scale_w, new_length_scale)
            sf.write(target_file, audio, samplerate=sr)