"""
header 给出的是一些说明API调用的辅助信息（耗时、错误码等）
norm_str 给出的是文本正规化的结果
word_list 包含基础粒度的分词及其词性标注结果
phrase_list 是复合粒度的分词和词性标注
entity_list 给出了所有识别出的实体及其类型
syntactic_parsing_str 和 srl_str 分别表示成分句法树和语义角色标注结果
"""
import json
import requests
from functools import lru_cache

API_URL = "https://texsmart.qq.com/api"
default_options = {
    "input_spec": {
        "lang": "chs"
    },
    "word_seg": {
        "enable": True
    },
    "pos_tagging": {
        "enable": True,
        "alg": "log_linear"
    },
    "ner": {
        "enable": True,
        "alg": "crf",
        "fine_grained": True
    },
    "syntactic_parsing": {
        "enable": False
    },
    "srl": {
        "enable": False
    }
}


@lru_cache(None)
def get_textsmart_api_data(text):
    """textsmart Html api 解析结果"""
    obj = {"str": text, "options": default_options}
    req_str = json.dumps(obj).encode()
    try:
        r = requests.post(API_URL, data=req_str)
    except ConnectionError:
        raise
    r.encoding = "utf-8"
    data = r.json()
    data.pop('header')
    return data


def _to_name(x):
    return x.split('.')[0].upper()


def lcut(text):
    """在线api分词

    Args:
        text (str): 要分词的文本

    Returns:
        list: 分词列表
    """
    # 配置对返回值好像没有影响
    data = get_textsmart_api_data(text)
    return [w['str'] for w in data['word_list']]


def entities(text):
    """在线命名实体解析

    Args:
        text (str): 输入文本

    Returns:
        list: 命名实体信息列表 (开始位置、结束位置、类型名称)
    """
    data = get_textsmart_api_data(text)
    ents = data['entity_list']
    spans = []
    for en in ents:
        start = en['hit'][0]
        end = start + en['hit'][1]
        # 专门化适用于大量语料。此处简化为父类，忽略子类
        name = _to_name(en['type']['name'])
        spans.append((start, end, name))
    return spans