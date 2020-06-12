#!/usr/bin/env python
#encoding=utf-8
import sys
import os.path
module_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(module_dir + '/../../lib/')
from tencent_ai_texsmart import *

print('Creating and initializing the NLU engine...')
engine = NluEngine(module_dir + '/../../data/nlu/kb/', 1)

options = '{"ner":{"enable":true,"fine_grained":false}}'

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

import time
docs = [
    """特斯拉板块开盘走强，华昌达一字涨停，秀强股份开盘冲板，杉杉股份、奥特佳、世运电路跟涨。""",
    """游戏股走强，凯撒文化、星辉娱乐涨停，迅游科技、富春股份、姚记科技等跟涨。""",
    """近期，国内稀土价格不断攀升，尤其轻稀土价格频频异动。上海有色网数据显示，6月10日，镨钕氧化物、氧化钕价格连续三日上调，分别较初的报价上涨6.09%、5.89%。中重稀土价格亦出现较大幅上涨。对于轻稀土价格连续异动的原因，一位稀土研究人士表示，下游需求好转，使上游商家的惜售和看涨情绪较浓。中重稀土方面，除了终端新能源汽车市场回暖等积极因素外，收储预期也支撑着价格。""",
    """塔牌集团在互动平台表示，近期公司水泥价格有小幅回调，目前水泥价格较去年同期高10%左右。新投产的文福万吨线第二条生产线磨合得较好，预计2-3个月内可以达到达标达产状态。""",
    """摩根士丹利：电视面板价格6月见底后，三季度有望反弹，或有助于京东方和群创光电等面板股的基本面改善。""",
]


def cut_word(sentence):
    output = engine.parse_text_ext(sentence, options)
    return ' '.join([w.str for w in output.words()])


def tag_word(sentence):
    output = engine.parse_text_ext(sentence, options)
    return [(item.str, item.tag) for item in output.phrases()]


def ner(sentence):
    output = engine.parse_text_ext(sentence, options)
    return [(en.str, en.type.i18n) for en in output.entities()]


s = time.time()
for doc in docs:
    print(cut_word(doc))
print(f"{time.time()-s:0.4f}")


