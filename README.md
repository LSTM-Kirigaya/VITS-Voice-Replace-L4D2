![](https://img.shields.io/badge/Python-3.8-blue) ![](https://img.shields.io/badge/AI-VITS-green) ![](https://img.shields.io/badge/Game-L4D2-orange)


Original repo : https://github.com/wuheyi/vits-uma-genshin-honkai

Where to get access to my MOD : https://steamcommunity.com/profiles/76561199183298707/myworkshopfiles/?appid=550

---

Warning: this project haven't been accomplished yet! Don't publish issue, please.


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



## Step to make custom VITS voice of a specific character in L4D2

make the voice of Nick：

```bash
# synthesis (use VITS)
python main.py --device cuda -n gambler
# postprocess the sound (see ./notebook/sound.ipynb to see the detail)
python postprocess.py -n gambler
```

> name of input and according character share the following relationship：

- coach -> Coach
- producer -> Rochelle
- gambler -> Nick
- mechanic -> Ellis

## How to publish

