#! python

"""
This module provides one function, languageName(), that returns
the human-readable name of a language from a codename (like 'nl').

The data is in the data.py file.
The file generate.py can be used by developers to (re-)generate
the data file.

Thanks go to the KDE developers for their translated language names
which are used currently in data.py.

"""

import itertools
import locale
from .data import language_names

__all__ = ['languageName']


def languageName(code, language=None):
    """Returns a human-readable name for a language.
    
    The language must be given in the 'code' attribute.
    The 'language' attribute specifies in which language
    the name must be translated and defaults to the current locale.
    
    """
    if language is None:
        language = locale.getdefaultlocale()[0] or "C"
        
    for lang in _try(language, True):
        try:
            d = language_names[lang]
        except KeyError:
            continue
        
        for c in _try(code):
            try:
                return d[c]
            except KeyError:
                continue
        break
    return code


def _try(lang, c=False):
    """Yields e.g. "nl_NL", "nl" for "nl_NL". If c == True, yields "C" at the end."""
    yield lang
    if '_' in lang:
        yield lang.split('_')[0]
    if c:
        yield "C"
