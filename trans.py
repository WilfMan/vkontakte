#! -*- coding: utf-8 -*-
from trans_l.decorators import transliterate_function


@transliterate_function(language_code="ru", reversed=False)
def trans_word(word):
    return word
