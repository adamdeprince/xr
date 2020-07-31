from xr.test.case import EasyRECase
from unittest import TestCase

from xr import (
    CharacterSet,
    NegativeCharacterSet,
    Text,
    WordSet,
    NumericRange,
    CharacterRange,
    NegativeCharacterRange,
    Anything,
    )

class TestPeriod(EasyRECase, TestCase):
   AUTO_TEST_RES = [Text('.')]

   AUTO_TEST_MATCHES = [['.']]
   AUTO_TEST_NOMATCH = [['x']]

