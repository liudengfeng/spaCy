# coding: utf8
from __future__ import unicode_literals

import tempfile
import srsly
from pathlib import Path
from collections import OrderedDict
from ...attrs import LANG
from ...language import Language
from ...tokens import Doc
from ...util import DummyTokenizer
from ..tokenizer_exceptions import BASE_EXCEPTIONS
from .lex_attrs import LEX_ATTRS
from .stop_words import STOP_WORDS
from .tag_map import TAG_MAP
from ... import util


def try_tct_import():
    try:
        from .texsmart import TextSmart

        # segment a short text to have jieba initialize its cache in advance
        # list(jieba.cut("作为", cut_all=False))
        # 默认使用细颗粒分词
        return TextSmart
    except Exception as e:
        print(f"{e!r}")


class ChineseTokenizer(DummyTokenizer):
    def __init__(self, cls, nlp=None, config={}):
        self.vocab = nlp.vocab if nlp is not None else cls.create_vocab(nlp)
        self.tct_seg = try_tct_import()
        self.tokenizer = Language.Defaults().create_tokenizer(nlp)

    def __call__(self, text):
        words = list([x for x in self.tct_seg.cut(text) if x])
        (words, spaces) = util.get_words_and_spaces(words, text)
        return Doc(self.vocab, words=words, spaces=spaces)


class ChineseDefaults(Language.Defaults):
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    lex_attr_getters.update(LEX_ATTRS)
    lex_attr_getters[LANG] = lambda text: "zh"
    tokenizer_exceptions = BASE_EXCEPTIONS
    stop_words = STOP_WORDS
    tag_map = TAG_MAP
    writing_system = {
        "direction": "ltr",
        "has_case": False,
        "has_letters": False
    }
    use_tct = True
    # use_pkuseg = False

    @classmethod
    def create_tokenizer(cls, nlp=None, config={}):
        return ChineseTokenizer(cls, nlp, config=config)


class Chinese(Language):
    lang = "zh"
    Defaults = ChineseDefaults  # override defaults

    def make_doc(self, text):
        return self.tokenizer(text)


__all__ = ["Chinese"]
