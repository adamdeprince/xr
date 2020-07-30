import itertools
import operator
from functools import reduce

def all_combinations(seq):
    seq = list(seq)

    for x in range(2, len(seq) + 1):
        for combination in itertools.combinations(seq, x):
            yield combination


class EasyRECase(object):
    NEGATIVE = False
    def matches(self, re, candidate):
        self.assertTrue(re.matches(candidate), msg="%s does not match %s" % (re, candidate))
        self.assertTrue(re.optimize().matches(candidate), msg="%s does not match %s" % (re, candidate))

    def doesnt_match(self, re, candidate):
        self.assertFalse(re.matches(candidate), msg="%s matches %s" % (re, candidate))
        self.assertFalse(re.optimize().matches(candidate), msg="%s matches %s" % (re, candidate))

    def searchs(self, re, candidate):
        self.assertTrue(re.search(candidate), msg="\%s does not search %s" % (re, candidate))
        self.assertTrue(re.optimize().search(candidate), msg="\%s does not search %s" % (re, candidate))

    def doesnt_search(self, re, candidate):
        self.assertFalse(re.matches(candidate), msg="%s searches %s" % (re, candidate))
        self.assertFalse(re.optimize().matches(candidate), msg="%s searches %s" % (re, candidate))

    def exactly_matches(self, re, candidate):
        self.assertTrue(re.matches(candidate), msg="%s does not match %s" % (re, candidate))
        self.assertTrue(re.optimize().matches(candidate), msg="%s does not match %s" % (re, candidate))

    def doesnt_exactly_match(self, re, candidate):
        self.assertFalse(re.exact_match(candidate), msg="%s matches %s" % (re, candidate))
        self.assertFalse(re.optimize().exact_match(candidate), msg="%s matches %s" % (re, candidate))

    def doesnt_match_exactly(self, re, candidate):
        self.assertFalse(re.exa(candidate), msg="%s matches %s" % (re, candidate))
        self.assertFalse(re.optimize().exa(candidate), msg="%s matches %s" % (re, candidate))

    def test_or(self):
        all_matches = set()
        for matches in self.AUTO_TEST_MATCHES:
            all_matches.update(matches)

        for re_and_matches in all_combinations(zip(self.AUTO_TEST_RES, self.AUTO_TEST_MATCHES)):
            res, matches = zip(*re_and_matches)

            re = reduce(operator.or_, res)
            these_matches = set()
            for re_specific_matches in matches:
                these_matches.update(re_specific_matches)
                for match in re_specific_matches:
                    self.exactly_matches(re, match)
            if not self.NEGATIVE:
                for match in all_matches - these_matches:
                    self.doesnt_exactly_match(re, match)

    def test_add(self):
        if self.NEGATIVE:
            return
        all_matches = set()
        for matches in self.AUTO_TEST_MATCHES:
            all_matches.update(matches)

        all_possiable_candidates = set()
        for candidates in all_combinations(self.AUTO_TEST_MATCHES):
            all_possiable_candidates.update(itertools.product(*candidates))

        for re_and_match in all_combinations(zip(self.AUTO_TEST_RES, self.AUTO_TEST_MATCHES)):
            for re_and_match_ordered in itertools.permutations(re_and_match):
                res, matches = zip(*re_and_match_ordered)
                re = reduce(operator.add, res)
                matches = set(itertools.product(*matches))

                for candidate in all_possiable_candidates:
                    if candidate in matches:
                        self.exactly_matches(re, ''.join(candidate))
                    else:
                        self.doesnt_exactly_match(re, ''.join(candidate))

    def test_plain(self):
        for re, accept, reject in zip(self.AUTO_TEST_RES, self.AUTO_TEST_MATCHES, self.AUTO_TEST_NOMATCH):
            for candidate in accept:
                self.exactly_matches(re, candidate)
            for candidate in reject:
                self.doesnt_exactly_match(re, candidate)

    def test_maybe(self):
        for re, candidates in zip(self.AUTO_TEST_RES, self.AUTO_TEST_MATCHES):
            self.matches(re.maybe(), '')
            for candidate in candidates:
                self.exactly_matches(re.maybe(), candidate)

    def test_star(self):
        for re, candidates in zip(self.AUTO_TEST_RES, self.AUTO_TEST_MATCHES):
            self.matches(re.star(), '')
            for candidate in candidates:
                for count in [1, 2, 3, 4, 5, 6, 10, 100]:
                    self.exactly_matches(re.star(), candidate * count)

    def test_plus(self):
        for re, candidates in zip(self.AUTO_TEST_RES, self.AUTO_TEST_MATCHES):
            self.doesnt_exactly_match(re.plus(), '')
            for candidate in candidates:
                for count in [1, 2, 3, 4, 5, 6, 10, 100]:
                    self.exactly_matches(re.plus(), candidate * count)

    def test_multiplication(self):
        for re, candidates in zip(self.AUTO_TEST_RES, self.AUTO_TEST_MATCHES):
            for candidate in candidates:
                for count in [1, 2, 3, 4, 5, 6, 10, 100]:
                    self.exactly_matches(re * count, candidate * count)
                    self.doesnt_exactly_match(re * count, candidate * (count + 1))
                    self.doesnt_exactly_match(re * count, candidate * (count - 1))
