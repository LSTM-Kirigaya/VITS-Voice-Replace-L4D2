from pydub import AudioSegment
from pydub.effects import compress_dynamic_range, normalize
import pydub.scipy_effects as scipy_effects


import os
import tqdm
import argparse
import yaml
import json

with open('./config/voice.yaml', 'r', encoding='utf-8') as fp:
    config = yaml.load(fp, Loader=yaml.FullLoader)


def change_db(wav_file: str, target_dbfs: int=0, focus_freq = 1000) -> AudioSegment:
    input_audio: AudioSegment = AudioSegment.from_file(wav_file, format="wav")
    gain = target_dbfs - input_audio.max_dBFS
    out = scipy_effects.eq(input_audio, focus_freq=focus_freq, gain_dB=gain, filter_mode="high_shelf", order=2)
    out = normalize(out, headroom=0.05)
    return out


def align_audio_two_folders(name: str):
    meta_path = os.path.join('transcription', f'{name}.meta.json')
    with open(meta_path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    target_folder = os.path.join('dist', config[name]['mod_name'])
    root = os.path.join(target_folder, 'sound', 'player', 'survivor', 'voice', name)

    for wav_file in tqdm.tqdm(os.listdir(root)):
        wav_path = os.path.join(root, wav_file)
        if wav_file not in data:
            os.remove(wav_path)
        else:
            target_wav_info = data[wav_file]
            align_sample_rate(wav_path, target_wav_info['sr'])
            align_length(wav_path, target_wav_info['length'])


def align_length(target_wav_file: str, target_length: int):
    target_audio = AudioSegment.from_file(target_wav_file)
    length = len(target_audio)

    if length == target_length:
        return

    # if length2 > length1:
    #     audio2 = audio2[:length1]

    if length < target_length:
        silence = AudioSegment.silent(duration=target_length - length)
        target_audio += silence

    target_audio.export(target_wav_file, format="wav")

def align_sample_rate(target_wav_file: str, target_sr: int):
    audio: AudioSegment = AudioSegment.from_file(target_wav_file)
    audio.set_frame_rate(target_sr)
    audio.export(target_wav_file, format='wav')


def print_base_wav_info(wav_file: str):
    audio: AudioSegment = AudioSegment.from_file(wav_file)
    print("name:{}  sr: {}, length: {}, width: {}".format(wav_file, audio.frame_rate, audio.__len__(), audio.frame_width))

def make_voice_brighter(root: str):
    for wave_file in tqdm.tqdm(os.listdir(root)):
        wave_path = os.path.join(root, wave_file)
        target_path = os.path.join(root, wave_file)

        result_audio = change_db(wave_path, target_dbfs, focus_freq=config[name]['filter_center'])
        result_audio.export(target_path, format='wav')
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', default='producer', type=str, choices=['producer', 'coach', 'gambler', 'mechanic'])
    parser.add_argument('-t', default=0, type=int)
    args = parser.parse_args()

    name: str = args.n
    target_dbfs: int = args.t

    target_folder = os.path.join('dist', config[name]['mod_name'])
    root = os.path.join(target_folder, 'sound', 'player', 'survivor', 'voice', name)
    if not os.path.exists(root):
        os.mkdir(root)

    print('postprocess voice...')
    make_voice_brighter(root)

    print('align length and sample rate...')
    align_audio_two_folders(name)

    print('generate vpk')
    os.system('vpk {}'.format(target_folder))
    print('bingo :D')