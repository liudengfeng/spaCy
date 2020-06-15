from . import online


class TextSmart(object):
    """腾讯AI文本处理工具"""
    def __init__(self, use_online=True):
        self.use_online = use_online
        if use_online:
            self.mod = online
        else:
            from . import offline
            self.mod = offline

    def lcut(self, text):
        """分词列表"""
        return self.mod.lcut(text)

    def get_entities(self, text):
        """命名实体列表"""
        return self.mod.entities(text)

    # TODO:废除以下部分
    @classmethod
    def cut_word(cls, text, coarse=False):
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

    @classmethod
    def tag_word(cls, text, coarse=False):
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

    @classmethod
    def ner(cls, text):
        """命名实体

        Args:
            text (str): 未分词的文本
        Returns:
            list: 词、中文实体名称 二元组列表
        """
        output = engine.parse_text_ext(text, options)
        return [(en.str, en.type.i18n) for en in output.entities()]
