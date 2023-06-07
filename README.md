![](https://img.shields.io/badge/Python-3.8-blue) ![](https://img.shields.io/badge/AI-VITS-green) ![](https://img.shields.io/badge/Game-L4D2-orange)


Original repo : https://github.com/wuheyi/vits-uma-genshin-honkai

Where to get access to my MOD : https://steamcommunity.com/profiles/76561199183298707/myworkshopfiles/?appid=550

---


## Prepare

1. install python and correct version of `pytorch`, I believe you can do this easily since 2023 :D
2. install dependencies:
```bash
pip install -r requirements.txt
```
3. install model checkpoints:
```bash
# Windows
wget -O model/G_953000.pth https://huggingface.co/spaces/zomehwh/vits-uma-genshin-honkai/resolve/main/model/G_953000.pth

# Linux
wget -P model/ https://huggingface.co/spaces/zomehwh/vits-uma-genshin-honkai/resolve/main/model/G_953000.pth
```
4. add L4D2 tool bin to environment to ensure you can use `vpk` in your command. You should ensure no error take place when you enter the following command：
```
vpk -h
```

> Path of tool bin in my PC is `D:\Download\steam\steam\steamapps\common\Left 4 Dead 2\bin`




## Command to make custom VITS voice of a specific character in L4D2

### Make all voice in default config

This is quite easy: 

```bash
# Windows
.\build_all.bat

# Linux
sh build_all.bash
```

### Custom Config

If you want adjust voice source, please edit `./config/voice.yaml`, take `producer` as an example:

```yaml
producer: 
  mod_name: shenhe_voice
  config: [132, 0.3, 0.668, 1.0]
  filter_center: 150
```

the only vital number above is `132` (voice code), it represents the voice source, you can view it in `./config/vit_character.json`. As you see, 132 represents "申鹤". You can view the voice of different source via:

```bash
python app.py --device cuda
```
This will open a application in your brower through http://127.0.0.1:7860/ , where you can quickly view different voice.

Just edit the voice code as you like :D

## Publish your VITS voice MOD

use `Left 4 Dead 2 Authoring Tools`, you can google its usage.