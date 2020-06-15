import sys
import os.path
import os
module_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(module_dir + '/lib/')
from tencent_ai_texsmart import *
from functools import lru_cache

print('创建和初始化腾讯AI-NLU引擎...')
max_cpu = max(os.cpu_count() // 2, 1)
# 默认为串行，修改为使用本机物理cpu个数
engine = NluEngine(module_dir + '/data/nlu/kb/', 1)  #max_cpu)
# disable fine-grained NER，加快解析速度
options = '{"ner":{"enable":true,"fine_grained":true}}'


@lru_cache(None)
def parse_out(text):
    return engine.parse_text_ext(text, options)


def _to_name(x):
    return x.split('.')[0].upper()


def lcut(text):
    """离线api分词

    Args:
        text (str): 要分词的文本

    Returns:
        list: 分词列表
    """
    output = parse_out(text)
    return [w.str for w in output.words()]


def entities(text):
    """离线命名实体解析

    Args:
        text (str): 输入文本

    Returns:
        list: 命名实体信息列表 (开始位置、结束位置、类型名称)
    """
    output = parse_out(text)
    spans = []
    for en in output.entities():
        start = en.offset
        end = en.offset + en.len
        # 专门化适用于大量语料。此处简化为父类，忽略子类
        name = _to_name(en.type.name)
        spans.append((start, end, name))
    return spans
