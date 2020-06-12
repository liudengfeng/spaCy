import sys
import os.path
module_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(module_dir+'/../../lib/')
from tencent_ai_texsmart import *
options = '{"ner":{"enable":true,"fine_grained":false}}'

print('Creating and initializing the NLU engine...')
engine = NluEngine(module_dir + '/../../data/nlu/kb/', 1)

# 粗颗粒解析出 流浪地球 电影
print(u'=== 解析一个中文句子 ===')
output = engine.parse_text_ext(u"上个月30号，南昌王先生在自己家里边看流浪地球边吃煲仔饭", options)
print(u'细粒度分词:')
for item in output.words():
    print(u'\t{0}\t{1}\t{2}\t{3}'.format(item.str, item.offset, item.len, item.tag))
print(u'粗粒度分词:')
for item in output.phrases():
    print(u'\t{0}\t{1}\t{2}\t{3}'.format(item.str, item.offset, item.len, item.tag))
