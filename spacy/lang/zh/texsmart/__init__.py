import sys
import os.path
module_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(module_dir + '/lib/')
from tencent_ai_texsmart import *

print('创建和初始化腾讯AI-NLU引擎...')
# 默认为串行
engine = NluEngine(module_dir + '/data/nlu/kb/', 1)
# disable fine-grained NER，加快解析速度
options = '{"ner":{"enable":true,"fine_grained":false}}'


class TextSmart(object):
    """腾讯AI文本处理工具"""
    @staticmethod
    def cut(text):
        output = engine.parse_text_ext(text, options)
        return [w.str for w in output.words()]

    @staticmethod
    def cut_word(text, coarse=False):
        """切词并以空格连接返回文本

        Args:
            text (str): 未分词的文本
            coarse (bool, optional): 是否粗颗粒分词 Defaults to False.
                细颗粒对应词汇总量少，而粗颗粒导致大量的名词组合，词汇量加大
        Returns:
            str: 分词后的文本
        """
        output = engine.parse_text_ext(text, options)
        iter_ = output.phrases() if coarse else output.words()
        return ' '.join([w.str for w in iter_])

    @staticmethod
    def tag_word(text, coarse=False):
        """分词标注

        Args:
            text (str): 未分词的文本
            coarse (bool, optional): 是否粗颗粒分词 Defaults to False.
                细颗粒对应词汇总量少，而粗颗粒导致大量的名词组合，词汇量加大
        Returns:
            list: 词、TAG二元组列表
        """
        output = engine.parse_text_ext(text, options)
        iter_ = output.phrases() if coarse else output.words()
        return [(w.str, w.tag) for w in iter_]

    @staticmethod
    def ner(text):
        """命名实体

        Args:
            text (str): 未分词的文本
        Returns:
            list: 词、中文实体名称 二元组列表
        """
        output = engine.parse_text_ext(text, options)
        return [(en.str, en.type.i18n) for en in output.entities()]

    @staticmethod
    def get_entities(text):
        output = engine.parse_text_ext(text, options)
        return output.entities()