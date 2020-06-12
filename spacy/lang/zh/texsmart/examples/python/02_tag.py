import sys
import os.path
module_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(module_dir+'/../../lib/')
from tencent_ai_texsmart import *
options = '{"ner":{"enable":true,"fine_grained":false}}'

print('Creating and initializing the NLU engine...')
engine = NluEngine(module_dir + '/../../data/nlu/kb/', 1)

# 粗颗粒解析出 流浪地球 电影
print('=== 解析一个中文句子 ===')
text = "俄罗斯报告新增9877例新冠肺炎确诊病例，累计确诊511423例；新增183例新冠肺炎死亡病例，累计死亡6715例。"
output = engine.parse_text_ext(text, options)

print('粗粒度分词:')
for item in output.phrases():
    print(f"{item.str} -> {item.tag} -> {item.tag_id} ->{item.start_token} -> {item.token_count}")


print("结巴标注")
import jieba.posseg as pseg
words = pseg.cut(text)
for word, flag in words:
    print('%s %s' % (word, flag))
