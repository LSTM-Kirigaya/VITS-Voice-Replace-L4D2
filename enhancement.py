import os
from pydub import AudioSegment
from pydub.effects import compress_dynamic_range, normalize
import pydub.scipy_effects as scipy_effects
import numpy as np

from postprocess import change_db


experiment_root = 'experiment'

os.makedirs(experiment_root, exist_ok=True)

def apply_saturation(audio_segment: AudioSegment, saturation_level: float = 1.5):
    """
    应用饱和度处理到音频片段。

    :param audio_segment: pydub.AudioSegment 对象
    :param saturation_level: 饱和度水平，值越大，饱和度越高
    :return: 处理后的 pydub.AudioSegment 对象
    """
    # 将音频数据转换为 numpy 数组
    samples = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
    print(samples.shape)

    # 应用饱和度处理
    saturated_samples = np.tanh(samples * saturation_level) / np.tanh(saturation_level)

    # 将处理后的数据转换回 pydub.AudioSegment 对象
    saturated_audio = audio_segment._spawn(saturated_samples.astype(np.int16))

    return saturated_audio

target_dbfs = 0

input_audio: AudioSegment = AudioSegment.from_file(r'dist\elysia_voice\sound\player\survivor\voice\producer\adrenaline03.wav', format='wav')
gain = target_dbfs - input_audio.max_dBFS
out = scipy_effects.eq(input_audio, focus_freq=800, gain_dB=gain, filter_mode="high_shelf", order=2)
out = normalize(out, headroom=0.05)
out.export(os.path.join(experiment_root, 'test.wav'), format='wav')