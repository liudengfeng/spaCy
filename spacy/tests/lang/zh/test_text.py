# coding: utf-8
from __future__ import unicode_literals

import pytest


@pytest.mark.parametrize(
    "text,match,length",
    [
        ("10", True, 1),
        ("1", True, 1),
        ("999.0", True, 3),  # 默认基础粒度，将数字分为三部分
        ("一", True, 1),
        ("二", True, 1),
        ("〇", True, 1),
        ("十一", True, 1),
        ("狗", False, 1),
        (",", False, 1),
    ],
)
def test_lex_attrs_like_number(zh_tokenizer_tct_offline, text, match, length):
    """测试离线token的数字特性"""
    tokens = zh_tokenizer_tct_offline(text)
    assert len(tokens) == length
    assert tokens[0].like_num == match


@pytest.mark.parametrize(
    "text,match,length",
    [
        ("10", True, 1),
        ("1", True, 1),
        ("999.0", True, 3),
        ("一", True, 1),
        ("二", True, 1),
        ("〇", True, 1),
        ("十一", True, 1),
        ("狗", False, 1),
        (",", False, 1),
    ],
)
def test_lex_attrs_like_number_online(zh_tokenizer_tct_online, text, match,
                                      length):
    """测试在线api分词token的数字特性"""
    tokens = zh_tokenizer_tct_online(text)
    assert len(tokens) == length
    assert tokens[0].like_num == match