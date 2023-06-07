from pydub import AudioSegment
from pydub.effects import compress_dynamic_range, normalize

import os
import tqdm
import argparse

def change_db(wav_file: str, target_dbfs: int=0) -> AudioSegment:
    input_audio: AudioSegment = AudioSegment.from_file(wav_file, format="wav")
    gain = target_dbfs - input_audio.max_dBFS
    louder_audio = input_audio + gain

    normalized_audio = normalize(louder_audio, headroom=0.05)
    return normalized_audio

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', default='producer', type=str, choices=['producer', 'coach', 'gambler', 'mechanic'])
    parser.add_argument('-t', default=0, type=int)
    args = parser.parse_args()

    name: str = args.n
    target_dbfs: int = args.t

    root = os.path.join('sound', name)
    target_root = os.path.join('sound', name + '_post')
    if not os.path.exists(root):
        os.mkdir(root)
    if not os.path.exists(target_root):
        os.mkdir(target_root)

    for wave_file in tqdm.tqdm(os.listdir(root)):
        wave_path = os.path.join(root, wave_file)
        target_path = os.path.join(target_root, wave_file)

        result_audio = change_db(wave_path, target_dbfs)
        result_audio.export(target_path, format='wav')