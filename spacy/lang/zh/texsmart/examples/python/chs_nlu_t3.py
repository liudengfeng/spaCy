#!/usr/bin/env python
#encoding=utf-8
import sys
import os.path
module_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(module_dir + '/../../lib/')
from tencent_ai_texsmart import *

print('Creating and initializing the NLU engine...')
engine = NluEngine(module_dir + '/../../data/nlu/kb/', 1)

print('=== 解析一个中英混合句子 ===')
output = engine.parse_text(
    "化妆品零售商丝芙兰（Sephora）的美国部门周三宣布，将把15%的售货空间留给黑人拥有的品牌，成为首个加入“15%承诺”的零售商。这一运动是由美国黑人女设计师、配饰品牌Brother Vellies创始人奥罗拉-詹姆斯（Aurora James）发起的，要求零售商评估其商品供应商的多样性，并将至少15%的份额留给黑人品牌。"
)
print('细粒度分词:')
for item in output.words():
    print('\t{0}\t{1}\t{2}\t{3}'.format(item.str, item.offset, item.len,
                                        item.tag))
print('粗粒度分词:')
for item in output.phrases():
    print('\t{0}\t{1}\t{2}\t{3}'.format(item.str, item.offset, item.len,
                                        item.tag))
print('命名实体识别（NER）:')
for entity in output.entities():
    type_str = '({0},{1},{2},{3})'.format(entity.type.name, entity.type.i18n,
                                          entity.type.flag, entity.type.path)
    print('\t{0}\t({1},{2})\t{3}\t{4}'.format(entity.str, entity.offset,
                                              entity.len, type_str,
                                              entity.meaning))
