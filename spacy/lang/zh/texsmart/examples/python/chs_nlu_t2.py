#!/usr/bin/env python
#encoding=utf-8
import sys
import os.path
module_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(module_dir+'/../../lib/')
from tencent_ai_texsmart import *

print('Creating and initializing the NLU engine...')
engine = NluEngine(module_dir + '/../../data/nlu/kb/', 1)

print('=== 解析一个中文句子 ===')
output = engine.parse_text("上个月30号，南昌王先生在自己家里边看流浪地球边吃煲仔饭")
print('细粒度分词:')
for item in output.words():
    print('\t{0}\t{1}\t{2}\t{3}'.format(item.str, item.offset, item.len, item.tag))
print('粗粒度分词:')
for item in output.phrases():
    print('\t{0}\t{1}\t{2}\t{3}'.format(item.str, item.offset, item.len, item.tag))
print('命名实体识别（NER）:')
for entity in output.entities():
    type_str = '({0},{1},{2},{3})'.format(entity.type.name, entity.type.i18n, entity.type.flag, entity.type.path)
    print('\t{0}\t({1},{2})\t{3}\t{4}'.format(entity.str, entity.offset, entity.len, type_str, entity.meaning))
