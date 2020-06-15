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
from .texsmart import TextSmart


def try_tct_import(require_online):
    ts = TextSmart(require_online)
    if require_online:
        # 如果在线api异常，使用离线模式
        try:
            # TODO:检验长度
            assert len(ts.lcut('国务院总理李克强毕业于北京大学。')) == 9, 'len(tokens) != 9'
            # 默认使用在线api
            return ts.lcut
        except Exception as e:
            print(f"{e!r}")
            return TextSmart(False).lcut
    return ts.lcut


class ChineseTokenizer(DummyTokenizer):
    def __init__(self, cls, nlp=None, config={}):
        self.use_tct = config.get("use_tct", cls.use_tct)
        self.require_online = config.get("require_online", cls.require_online)
        print(f'Tencet Textsmart {"在线" if self.require_online else "离线"}模式')
        self.vocab = nlp.vocab if nlp is not None else cls.create_vocab(nlp)
        self.tct_seg = try_tct_import(self.require_online)
        # remove relevant settings from config so they're not also saved in
        # Language.meta
        for key in ["use_tct", "require_online"]:
            if key in config:
                del config[key]
        self.tokenizer = Language.Defaults().create_tokenizer(nlp)

    def __call__(self, text):
        use_tct = self.use_tct
        if use_tct:
            words = list([x for x in self.tct_seg(text) if x])
            (words, spaces) = util.get_words_and_spaces(words, text)
            return Doc(self.vocab, words=words, spaces=spaces)
        else:
            # split into individual characters
            words = list(text)
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
    # 默认使用在线api
    use_tct = True
    require_online = True

    @classmethod
    def create_tokenizer(cls, nlp=None, config={}):
        return ChineseTokenizer(cls, nlp, config=config)


class Chinese(Language):
    lang = "zh"
    Defaults = ChineseDefaults  # override defaults

    def make_doc(self, text):
        return self.tokenizer(text)


__all__ = ["Chinese"]
