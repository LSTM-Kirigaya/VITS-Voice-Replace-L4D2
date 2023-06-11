from pydub import AudioSegment
from pydub.effects import compress_dynamic_range, normalize
import pydub.scipy_effects as scipy_effects
import utils

import os
import tqdm
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument('-n', default='producer', type=str, choices=['whitaker', 'virgil', 'pilot', 'soldier', 'soldier1', 'soldier2', '05_military'])
parser.add_argument('-t', default=0, type=int)
parser.add_argument('--lang', type=str, default='zh', choices=['zh', 'ja'])
parser.add_argument('--log', type=str, default='', help='xxx.exceed.json, only process those words')
args = parser.parse_args()

exceed_logs = {}

def change_db(wav_file: str, target_dbfs: int=0, focus_freq = 1000) -> AudioSegment:
    input_audio: AudioSegment = AudioSegment.from_file(wav_file, format="wav")
    gain = target_dbfs - input_audio.max_dBFS
    out = scipy_effects.eq(input_audio, focus_freq=focus_freq, gain_dB=gain, filter_mode="high_shelf", order=2)
    out = normalize(out, headroom=0.05)
    return out


def align_audio_two_folders(name: str, wav_files: list=None):
    meta_path = os.path.join('transcription', 'npc', f'{name}.meta.json')
    data = utils.read_json(meta_path)

    target_folder = os.path.join('dist', config[name]['mod_name'])
    root = os.path.join(target_folder, 'sound', 'npc', name)

    handle_files = os.listdir(root)
    if wav_files is not None:
        handle_files = wav_files

    for wav_file in tqdm.tqdm(handle_files):
        wav_path = os.path.join(root, wav_file)
        if wav_file not in data:
            os.remove(wav_path)
        else:
            target_wav_info = data[wav_file]
            align_sample_rate(wav_path, target_wav_info['sr'])
            align_length(wav_path, target_wav_info['length'])

    if len(exceed_logs) > 0:
        utils.write_json(f'./log/{name}.exceed.json', exceed_logs)

def align_length(target_wav_file: str, target_length: int):
    target_audio = AudioSegment.from_file(target_wav_file)
    length = len(target_audio)

    if length == target_length:
        return

    if length > target_length:
        exceed_logs[os.path.basename(target_wav_file)] = { 'expect' : target_length, 'fact' : length }

    if length < target_length:
        silence = AudioSegment.silent(duration=target_length - length + 2)
        target_audio += silence

    target_audio.export(target_wav_file, format="wav")

def align_sample_rate(target_wav_file: str, target_sr: int):
    audio: AudioSegment = AudioSegment.from_file(target_wav_file)
    audio = audio.set_frame_rate(target_sr)
    audio.export(target_wav_file, format='wav')

def print_base_wav_info(wav_file: str):
    audio: AudioSegment = AudioSegment.from_file(wav_file)
    print("name:{}  sr: {}, length: {}, width: {}".format(wav_file, audio.frame_rate, audio.__len__(), audio.frame_width))

def make_voice_brighter(root: str, wav_files: list=None):
    handle_files = os.listdir(root)
    if wav_files is not None:
        handle_files = wav_files

    for wave_file in tqdm.tqdm(handle_files):
        wave_path = os.path.join(root, wave_file)
        target_path = os.path.join(root, wave_file)

        result_audio = change_db(wave_path, target_dbfs, focus_freq=config[name]['filter_center'])
        result_audio.export(target_path, format='wav')

def phone_like(wav: AudioSegment, low_center=2400, high_center=500) -> AudioSegment:
    # audio = scipy_effects.low_pass_filter(wav, low_center)
    audio = scipy_effects.high_pass_filter(wav, high_center)
    audio = normalize(audio, headroom=0.05)
    return audio


def make_voice_like_phone(root: str, wav_files: list=None):
    handle_files = os.listdir(root)
    if wav_files is not None:
        handle_files = wav_files

    for wave_file in tqdm.tqdm(handle_files):
        wave_path = os.path.join(root, wave_file)
        target_path = os.path.join(root, wave_file)

        input_audio = AudioSegment.from_file(wave_path)
        result_audio = phone_like(input_audio)
        result_audio.export(target_path, format='wav')    

if __name__ == "__main__":

    if not os.path.exists('log'):
        os.makedirs('log')

    name: str = args.n
    target_dbfs: int = args.t
    log: str = args.log
    lang: str = args.lang

    wav_files = None
    if os.path.exists(log):
        log_data = utils.read_json(log)
        wav_files = list(log_data.keys())

    meta_path = os.path.join('transcription', 'npc', f'{name}.meta.json')
    data = utils.read_json(meta_path)

    with open(f'./config/voice_{lang}.yaml', 'r', encoding='utf-8') as fp:
        config = yaml.load(fp, Loader=yaml.FullLoader)

    target_folder = os.path.join('dist', config[name]['mod_name'])
    root = os.path.join(target_folder, 'sound', 'npc', name)

    if not os.path.exists(root):
        os.mkdir(root)

    print('postprocess voice...')
    if name == 'whitaker':
        make_voice_like_phone(root, wav_files)
    elif name == 'virgil':
        make_voice_like_phone(root, wav_files)
    elif name == 'soldier1':
        make_voice_like_phone(root, wav_files)
    elif name == 'soldier2':
        make_voice_like_phone(root, wav_files)
    else:
        make_voice_brighter(root, wav_files)

    print('align length and sample rate...')
    align_audio_two_folders(name, wav_files)

    print('generate vpk')
    os.system('vpk {}'.format(target_folder))
    print('bingo :D')