"""
time: 2023.06.06
author: Kirigaya
purpose: 用于将生成的 audio 长度与原本的音频对齐(x)，重采样到和原本音频采样率一致，顺便删除不存在于原本文件夹中的音频
要求 root 的内部有如下文件：
* .coach
* coach
* .gambler
* gambler
* .mechanic
* mechanic
* .producer
* producer
其中 .xxx 是原本的音频， xxx 是生成后的音频
"""

import os
import argparse
from pydub import AudioSegment
import soundfile as sf
import librosa
from tqdm import tqdm

names = ['producer', 'coach', 'gambler', 'mechanic']
root = r'D:\Download\steam\steam\steamapps\common\Left 4 Dead 2\left4dead2\sound\player\survivor\voice'

def need_align_length(wav_name: str) -> bool:
    for k in align_length_keywords:
        if k in wav_name:
            return True
    return False

def align_audio_two_folders(src_folder: str, out_folder: str):
    assert os.path.exists(src_folder)
    assert os.path.exists(out_folder)

    src_wavs = set(os.listdir(src_folder))

    for wav_file in tqdm(os.listdir(out_folder)):
        wav_path = os.path.join(out_folder, wav_file)
        if wav_file not in src_wavs:
            os.remove(wav_path)
        else:
            src_wav_path = os.path.join(src_folder, wav_file)
            align_sample_rate(src_wav_path, wav_path)
            align_length(src_wav_path, wav_path)

def align_audio(mod_wav_file: str, aligned_wav_file: str):
    align_sample_rate(mod_wav_file, aligned_wav_file)
    align_length(mod_wav_file, aligned_wav_file)


def align_length(mod_wav_file: str, aligned_wav_file: str):
    audio1 = AudioSegment.from_file(mod_wav_file)
    audio2 = AudioSegment.from_file(aligned_wav_file)

    length1 = len(audio1)
    length2 = len(audio2)

    if length1 == length2:
        return

    # if length2 > length1:
    #     audio2 = audio2[:length1]

    if length2 < length1:
        silence = AudioSegment.silent(duration=length1-length2)
        audio2 += silence

    # 将处理后的第二个音频保存为新的文件
    audio2.export(aligned_wav_file, format="wav")

def align_sample_rate(mod_wav_file: str, aligned_wav_file: str):
    _, sr = sf.read(mod_wav_file)
    aligned_signal, origial_sr = sf.read(aligned_wav_file)
    if sr == origial_sr:
        return

    resample_sig = librosa.resample(aligned_signal, orig_sr=origial_sr, target_sr=sr)
    sf.write(aligned_wav_file, resample_sig, sr)


def print_base_wav_info(wav_file: str):
    audio: AudioSegment = AudioSegment.from_file(wav_file)
    print("name:{}  sr: {}, length: {}, width: {}".format(wav_file, audio.frame_rate, audio.__len__(), audio.frame_width))

if __name__ == '__main__':
    # voice_root = r'D:\Download\steam\steam\steamapps\common\Left 4 Dead 2\left4dead2\sound\player\survivor\voice'

    # wav1 = os.path.join(voice_root, '.coach', 'worldc1m1b118.wav')
    # wav2 = os.path.join(voice_root, 'coach', 'worldc1m1b118.wav')

    # align_sample_rate(wav1, wav2)
    # print_base_wav_info(wav1)
    # print_base_wav_info(wav2)
    # print_base_wav_info('test.wav')


    for name in names:
        src_folder = os.path.join(root, '.' + name)
        out_folder = os.path.join(root, name)
        align_audio_two_folders(src_folder, out_folder)