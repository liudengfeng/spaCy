#!/usr/bin/env python
#encoding=utf-8
import sys
import os.path
module_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(module_dir+'/../../lib/')
from tencent_ai_texsmart import *

print('Creating and initializing the NLU engine...')
engine = NluEngine(module_dir + '/../../data/nlu/kb/', 1)

print(u'=== 解析一个中文句子 ===')
output = engine.parse_text(u"据北京市疾病预防控制中心，4月4日0时至24时，北京市新增报告1例境外输入新冠肺炎确诊病例，来自英国，有市内小区短暂居家停留（不足24小时），涉及的小区是：朝阳区团结湖街道团结湖公寓。")
print(u'细粒度分词:')
for item in output.words():
    print(u'\t{0}\t{1}\t{2}\t{3}'.format(item.str, item.offset, item.len, item.tag))
print(u'粗粒度分词:')
for item in output.phrases():
    print(u'\t{0}\t{1}\t{2}\t{3}'.format(item.str, item.offset, item.len, item.tag))
print(u'命名实体识别（NER）:')
for entity in output.entities():
    type_str = u'({0},{1},{2},{3})'.format(entity.type.name, entity.type.i18n, entity.type.flag, entity.type.path)
    print(u'\t{0}\t({1},{2})\t{3}\t{4}'.format(entity.str, entity.offset, entity.len, type_str, entity.meaning))
