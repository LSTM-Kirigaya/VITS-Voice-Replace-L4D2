# from transformers import (
#   T5Tokenizer,
#   MT5ForConditionalGeneration,
#   Text2TextGenerationPipeline,
# )

# path = "K024/mt5-zh-ja-en-trimmed"
# pipe = Text2TextGenerationPipeline(
#   model=MT5ForConditionalGeneration.from_pretrained(path),
#   tokenizer=T5Tokenizer.from_pretrained(path),
# )

# sentence = "ja2zh: 吾輩は猫である。名前はまだ無い。"
# res = pipe(sentence, max_length=100, num_beams=4)
# res[0]['generated_text']
import json

config = json.load(open('./model/config.json', 'r', encoding='utf-8'))
print(config['speakers'][132])