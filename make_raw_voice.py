import time
import os
import gradio as gr
import utils
import argparse
import commons

from models import SynthesizerTrn
from text import text_to_sequence
import torch
from torch import no_grad, LongTensor
import soundfile as sf
import json
import tqdm

audio_postprocess_ori = gr.Audio.postprocess
limitation = os.getenv("SYSTEM") == "spaces"  # limit text and audio length in huggingface spaces

parser = argparse.ArgumentParser()
parser.add_argument('--device', type=str, default='cpu')
parser.add_argument('--lang', type=str, default='zh', choices=['zh', 'ja'])
parser.add_argument('-n', default='producer', type=str, choices=['producer', 'coach', 'gambler', 'mechanic'])
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


make_config = {
    'producer': (torch.tensor([132]), 0.3, 0.668, 1.0),     # 申鹤
    'gambler':  (torch.tensor([228]), 0.6, 0.668, 1.0),     # 胡桃
    'mechanic': (torch.tensor([91]), 0.4, 0.668, 1.0),      # 荧
    'coach':    (torch.tensor([115]), 0.3, 0.668, 1.0),     # 刻晴
}

lang_code = {
    'zh': 0,
    'ja': 1
}

if __name__ == '__main__':
    name: str = args.n
    lang: str = args.lang
    lang_code: int = lang_code[lang]
    with open(f'transcription/{name}_{lang}.json', 'r', encoding='utf-8') as fp:
        transcription = json.load(fp)
    
    root = os.path.join('sound', name)
    if not os.path.exists(root):
        os.mkdir(root)
    
    for wave_file in tqdm.tqdm(transcription):
        target_file = os.path.join(root, wave_file)
        words = transcription[wave_file].strip()
        if len(words) > 0:
            sr, audio = vits(words, lang_code, *make_config[name])
            sf.write(target_file, audio, samplerate=sr)