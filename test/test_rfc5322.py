from xr.regex.rfc5322 import FQDN, RFC5322, Name
from unittest import TestCase

class TestRFC5322(TestCase):
    def test_fqdn(self):
        self.assertTrue(FQDN.match_exact('easyre.io'))
        self.assertFalse(FQDN.match_exact('examplecom'))

    def test_name(self):
        self.assertTrue(Name.match_exact('adamdeprince'))
        self.assertTrue(Name.match_exact('adam.deprince'))
        self.assertTrue(Name.match_exact('adam.d.e.prince'))
        self.assertFalse(Name.match_exact('.adamdeprince'))
        self.assertFalse(Name.match_exact('adam..deprince'))

    def test_simple_case(self):
        self.assertTrue(RFC5322.match_exact('adamdeprince@example.com'))
        self.assertFalse(RFC5322.match_exact('adamdeprince@@example.com'))
        self.assertTrue(RFC5322.match_exact('adam.deprince@example.com'))
        self.assertFalse(RFC5322.match_exact('adam..deprince@example.com'))
        
