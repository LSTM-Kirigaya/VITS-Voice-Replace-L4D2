voice_character_name = 'Kokomi'
game_character_name = 'Francis'
target_lang = 'zh'

lang_mapper = {
    'ja': {
        'en': 'Japanese',
        'zh': '日语'
    },
    'zh': {
        'en': 'Chinese',
        'zh': '中文'    
    },
    'en': {
        'en': 'English',
        'zh': '英文'
    }
}

title = '{} voice replace {} (AI {} Voice)'.format(voice_character_name, game_character_name, lang_mapper[target_lang]['en'])

introductionEn = '''Install Procedure:

1. click subscribe above.
2. enter game via steam.
3. waiting for downloading and enjoy.

> no need for extra command!

Use {} to replace voice of {}. Target language of voice is {}. Hope you like it!

If you are interested in my work, welcome to follow me in:

- QQ Group: 2166020149
- Zhihu: https://www.zhihu.com/people/can-meng-zhong-de-che-xian
- BiliBili: https://space.bilibili.com/434469188
- Personal Website: https://kirigaya.cn/home

Tech list:
- ASR: openai/whisper-medium (huggingface)
- Translation en-zh: Helsinki-NLP/opus-mt-en-zh (huggingface)
- Translation zh-ja: K024/mt5-zh-ja-en-trimmed (huggingface)
- TTS: https://github.com/wuheyi/vits-uma-genshin-honkai (github)

Original well established project was accomplished in just two nights by me: https://github.com/LSTM-Kirigaya/VITS-Voice-Replace-L4D2. Expect your valuable star and follows!

You know guys, the fact that those projects are always motivated by your support and enthusiasm :D'''.format(voice_character_name, game_character_name, lang_mapper[target_lang]['en'])


introductionCn = '''安装步骤：

1. 点击上方的订阅按钮。
2. 通过Steam进入游戏。
3. 等待下载完成并享受游戏。

> 无需额外命令！

使用 {} 替换 {} 的语音。目标语音语言为 {}。希望你喜欢！

如果你对我的工作感兴趣，欢迎关注我：

- QQ群：2166020149
- 知乎：https://www.zhihu.com/people/can-meng-zhong-de-che-xian
- BiliBili：https://space.bilibili.com/434469188
- 个人网站：https://kirigaya.cn/home

技术列表：
- ASR：openai/whisper-medium (huggingface)
- 英译中：Helsinki-NLP/opus-mt-en-zh (huggingface)
- 中译日：K024/mt5-zh-ja-en-trimmed (huggingface)
- TTS：https://github.com/wuheyi/vits-uma-genshin-honkai (github)

这个原本已经完善的项目仅用两个晚上就完成了：https://github.com/LSTM-Kirigaya/VITS-Voice-Replace-L4D2。期待你的宝贵星标和关注！

你知道的，这些项目的动力总是来自于你们的支持和热情 :D'''.format(voice_character_name, game_character_name, lang_mapper[target_lang]['zh'])


print(title)

print('-' * 20, end='\n')

print(introductionCn, end='\n\n---\n\n')

print(introductionEn)
