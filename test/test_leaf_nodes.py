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

class TestCharacterRange(EasyRECase, TestCase):
   AUTO_TEST_RES = [CharacterRange(['B', 'F']), CharacterRange(['1', '8']), CharacterRange(['A', 'y'])]

   AUTO_TEST_MATCHES = ['BCDEF', '12345678', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxy']
   AUTO_TEST_NOMATCH = ['AG', '09', 'z']

class TestNegativeCharacterRange(EasyRECase, TestCase):
    NEGATIVE = True
    AUTO_TEST_RES = [NegativeCharacterRange(['B', 'F']), NegativeCharacterRange(['1', '8']), NegativeCharacterRange(['A', 'y'])]

    AUTO_TEST_MATCHES = ['AG', '09', 'z']
    AUTO_TEST_NOMATCH = ['BCDEF', '12345678', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxy']

class TestCharacterSet(EasyRECase, TestCase):
    AUTO_TEST_RES = [CharacterSet('abc'), CharacterSet('+'), CharacterSet('.'), CharacterSet('[+.*]')]
    # Note that that actual format for AUTO_TEST_MATCHES is a sequence
    # of sequences of strings - we're abusin the fact that a string is
    # a sequence of single character strings here ...
    AUTO_TEST_MATCHES = ['abc', '+', '.', '[+.*]']
    AUTO_TEST_NOMATCH = ['def', '-', '+[]', 'abc']

class TestNegativeCharacterSet(EasyRECase, TestCase):
    NEGATIVE = True
    AUTO_TEST_RES = [NegativeCharacterSet('abc'), NegativeCharacterSet('+'), NegativeCharacterSet('.'), NegativeCharacterSet('[+.*]')]
    # Note that that actual format for AUTO_TEST_MATCHES is a sequence
    # of sequences of strings - we're abusin the fact that a string is
    # a sequence of single character strings here ...
    AUTO_TEST_MATCHES = ['def', '-', '+[]', 'abc']
    AUTO_TEST_NOMATCH = ['abc', '+', '.', '[+.*]']

class TestWordSet(EasyRECase, TestCase):
    AUTO_TEST_RES = [WordSet(['foo', 'bar'])]
    AUTO_TEST_MATCHES = [['foo', 'bar']]
    AUTO_TEST_NOMATCH = [['gronk']]

class TestNumericRange(EasyRECase, TestCase):
    AUTO_TEST_RES = [NumericRange(101, 200),]
    AUTO_TEST_MATCHES = [map(str, range(101, 200))]
    AUTO_TEST_NOMATCH = [['99', '100', '200', '201']]

class TestText(EasyRECase, TestCase):

    AUTO_TEST_RES = [Text('def'), Text('+'), Text('*'), Text('.')]
    AUTO_TEST_MATCHES = [['def'], ['+'], ['*'], ['.']]
    AUTO_TEST_NOMATCH = [['abcd'], ['++'], ['**'], ['.q']]

    def test_matches(self):
        self.matches(Text('def'), 'def')
        self.doesnt_match(Text('def'), 'abcdefghi')
        self.matches(Text('def'), 'defghi')
        self.doesnt_match(Text('def'), 'abcdef')
        self.doesnt_match(Text('def'), 'xyz')

    def test_searches(self):
        self.searchs(Text('def'), 'def')
        self.searchs(Text('def'), 'abcdefghi')
        self.searchs(Text('def'), 'defghi')
        self.searchs(Text('def'), 'abcdef')
        self.doesnt_search(Text('def'), 'xyz')


    def test_exactly_matches(self):
        self.exactly_matches(Text('def'), 'def')
        self.doesnt_exactly_match(Text('def'), 'abcdef')
        self.doesnt_exactly_match(Text('def'), 'defghi')
        self.doesnt_exactly_match(Text('def'), 'abcdefghi')

class TestAnything(EasyRECase, TestCase):
   AUTO_TEST_RES = [Anything]
   AUTO_TEST_MATCHES = ['abcdefghijklmnopqrstuvwxyz']
   AUTO_TEST_NOMATCH = [['abc', '']]
