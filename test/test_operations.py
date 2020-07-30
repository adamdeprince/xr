from xr.test.case import EasyRECase
from unittest import TestCase

from easyre import (
    CharacterSet,
    NegativeCharacterSet,
    Text,
    WordSet,
    NumericRange,
    CharacterRange,
    NegativeCharacterRange,
    Anything,
)


class TestAdd(EasyRECase, TestCase):
    AUTO_TEST_RES = [Text('a') + Text('b')]

    AUTO_TEST_MATCHES = [['ab']]
    AUTO_TEST_NOMATCH = [['ba']]


class TestTextAdd(EasyRECase, TestCase):
    AUTO_TEST_RES = [Text('a') + 'b']

    AUTO_TEST_MATCHES = [['ab']]
    AUTO_TEST_NOMATCH = [['ba']]


class TestTextRAdd(EasyRECase, TestCase):
    AUTO_TEST_RES = ['a' + Text('b')]

    AUTO_TEST_MATCHES = [['ab']]
    AUTO_TEST_NOMATCH = [['ba']]
