from functools import total_ordering, reduce
import re
import string

import six


@total_ordering
class _Infinite(object):

    def __eq__(self, other):
        return other is Infinite

    def __lt__(self, other):
        return False

    def __str__(self):
        return ""

    def __add__(self, other):
        return Infinite


Infinite = _Infinite()


class RE(object):

    def __add__(self, other):
        if isinstance(other, six.string_types):
            return self + Text(other)
        return Append(self, other)

    def __radd__(self, other):
        if isinstance(other, six.string_types):
            return Append(Text(other), self)
        return Append(other, self)

    def __ror__(self, other):
        if isinstance(other, six.string_types):
            return Or(self, Text(other))
        return Or(self, other)

    def __or__(self, other):
        if isinstance(other, six.string_types):
            return Or(self, Text(other))
        return Or(self, other)

    def match(self, s):
        return re.match(str(self), s)

    def matches(self, s):
        return re.match(str(self), s)

    def search(self, s):
        return re.search(str(self), s)

    def optimize(self):
        return self

    def compile(self, *args, **kwargs):
        return re.compile(str(self), *args, **kwargs)

    def find_all(self, s, *args, **kwargs):
        return self.compile(*args, **kwargs).findall(s)

    def __str__(self):
        return self._str

    def __eq__(self, other):
        return str(self) == str(other)

    def matches(self, s):
        return re.match(str(self), s)

    def exactly_matches(self, s):
        return re.match('^%s$' % self, s)

    def startswith(self, s):
        return re.match('^%s' % self, s)

    def endswith(self, s):
        return re.search('%s$' % self, s)

    def match_exact(self, s):
        return self.exactly_matches(s)

    def exact_match(self, s):
        return self.exactly_matches(s)

    def split(self, string, *args, **kwargs):
        return re.split(self.compile(), string, *args, **kwargs)

    def __mul__(self, other):
        if not isinstance(other, int) or other < 0:
            raise TypeError("Can only multiply regular expressions by positive integers")

        return Many(self, other, other)

    def maybe(self):
        return self.mult(0, 1)

    def optional(self):
        return self.maybe()

    def star(self):
        return self.mult()

    def plus(self):
        return self.mult(1)

    def mult(self, m=0, n=Infinite):
        return Many(self, m, n)

    def many(self, *args, **kwargs):
        return self.mult(*args, **kwargs)

    def group(self, key=None):
        return Group(self, key)


    def __call__(self, s):
        match = self.match_exact(s)
        if match:
            return match.groupdict()
        else:
            return None


class OneOp(RE):

    def optimize(self):
        self._re = self._re.optimize()
        return self


class TwoOp(RE):

    def optimize(self):
        self.left = self.left.optimize()
        self.right = self.right.optimize()
        return self


class Append(TwoOp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.left) + str(self.right)

    def __or__(self, other):
        return Or(self, other)

    def optimize(self):
        self.left = self.left.optimize()
        self.right = self.right.optimize()

        if isinstance(self.left, Text) and isinstance(self.right, Text):
            if self.left == self.right:
                return Many(self.left, m=2, n=2)
            return Text(self.left._s + self.right._s)
        if isinstance(self.left, Many) and isinstance(self.right, Many):
            if self.left._re == self.right._re:
                return Many(
                    self.left._re,
                    self.left._m +
                    self.right._m,
                    self.left._n +
                    self.right._n)

        if isinstance(self.left, Many) and self.right == self.left._re:
            return Many(self.left._re, self.left._m + 1, self.left._n + 1)

        if isinstance(self.right, Many) and self.left == self.right._re:
            return Many(self.right._re, self.right._m + 1, self.right._n + 1)
        return self


class Or(TwoOp):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "(?:%s|%s)" % (self.left, self.right)

    def optimize(self):
        self.left = self.left.optimize()
        self.right = self.right.optimize()

        if self.left == self.right:
            return self.left

        if isinstance(self.left, CharacterSet) and isinstance(self.right, CharacterSet):
            return CharacterSet(self.left._characters + self.right._characters)

        if isinstance(self.left, CharacterRange) and isinstance(self.right, CharacterRange):
            ranges = set()
            ranges.update(self.left._ranges)
            ranges.update(self.right._ranges)
            return CharacterRange(*ranges)
        return self


class Group(OneOp):

    def __init__(self, re, group=None):
        if group is not None and not isinstance(group, six.string_types):
            raise ValueError('Group must be a string')
        self.group = group
        if not isinstance(re, RE):
            raise ValueError('re must be a RE')
        self._re = re

        if group is None:
            self._str = "(%s)" % re
        else:
            self._str = "(?P<%s>%s)" % (group, re)

    def optimize(self):
        self._re = self._re.optimize()
        return self


class Many(RE):

    def __init__(self, re, m=0, n=Infinite):
        self._m = m
        self._re = re
        self._n = n

        m = int(m)
        if m < 0:
            raise ValueError('m must be >= 0')
        if n < m:
            raise ValueError('m must not be larger than n')

        if m == 0:
            if n == 0:
                self._str = ""
                return
            if n == 1:
                self._str = "(?:%s)?" % self._re
                return
            if n is Infinite:
                self._str = "(?:%s)*" % self._re
                return
            self._str = "(?:%s){0,%d}" % (self._re, n)
            return
        if m == 1:
            if n is Infinite:
                self._str = "(?:%s)+" % self._re
                return
            if n == 1:
                self._str = str(self._re)
                return
        if m == n:
            if len(str(self._re)) * n < 6:
                self._str = str(self._re) * n
                return
            self._str = "(?:%s){%s}" % (self._re, n)
            return
        self._str = "(?:%s){%s,%s}" % (self._re, m, n)

    def __mul__(self, other):
        if not isinstance(other, int) or other < 0:
            raise ValueError("Can only multiple regular expressions by positive integers")

        return Many(self._re, self._m * other, self._n * other)


class Text(RE):

    def __init__(self, s):
        self._str = re.escape(s)
        self._s = s


class _CharacterRange(RE):

    def __init__(self, *ranges):
        self._ranges = []
        for start, stop in ranges:
            if not isinstance(start, six.string_types) or len(start) != 1:
                raise ValueError('Start must be a single characters, not %r' % (start,))
            if not isinstance(stop, six.string_types) or len(stop) != 1:
                raise ValueError('Stop must be a single characters, not %r' % (stop,))

            # if start in '^-':
            #     raise ValueError('Cannot build a character range starting with ^ or -')
            # if stop in '^-':
            #     raise ValueError('Cannot build a character range stopping with ^ or -')

            if start > stop:
                self._ranges.append((stop, start))
            else:
                self._ranges.append((start, stop))
        self._ranges = set(self._ranges)

        self._str = self._build_str(self._ranges)

    def init_args(self):
        for start, stop in self._ranges:
            yield start + stop


class NegativeCharacterRange(_CharacterRange):

    def __neg__(self):
        return CharacterRange(*self.init_args())

    def _build_str(self, ranges):
        output = ['[^']
        for start, stop in ranges:
            if start in '^-':
                start = '\\' + start
            if stop in '^-':
                stop = '\\' + stop
            output.append('%s-%s' % (start, stop))
        output.append(']')
        return ''.join(output)


class CharacterRange(_CharacterRange):

    def __neg__(self):
        return NegativeCharacterRange(*self.init_args())

    def _build_str(self, ranges):
        output = ['[']
        for start, stop in ranges:
            if start in '^-':
                start = '\\' + start
            if stop in '^-':
                stop = '\\' + stop
            output.append('%s-%s' % (start, stop))
        output.append(']')
        return ''.join(output)


class CharacterSetMixin(object):
    REQUIRES_ESCAPE = set('\\\]-')
    PLACEMENT = {'-': -1, '^': 1}

    def __init__(self, characters):
        self._characters = set()
        for char in characters:
            if not isinstance(char, six.string_types):
                raise ValueError(
                    'CharacterSet expects a sequence of unicode or str objects; %r is a %s' % (
                        char, type(char)))
            self._characters.add(char)

        self._characters = ''.join(
            sorted(
                self._characters,
                key=lambda x: (
                    self.PLACEMENT.get(
                        x,
                        0),
                    x)))
        self._build_str()


class NegativeCharacterSet(RE, CharacterSetMixin):

    def __neg__(self):
        return CharacterSet(self._characters)

    def _build_str(self):
        output = []
        write = output.append
        write('[^')
        for character in self._characters:
            if character in self.REQUIRES_ESCAPE:
                write('\\')
            write(character)
        write(']')
        self._str = ''.join(output)


class CharacterSet(RE, CharacterSetMixin):
    def __neg__(self):
        return NegativeCharacterSet(self._chararcters)

    def _build_str(self):
        if self._characters == '^':
            self._str = '^'
            return
        output = []
        write = output.append
        write('[')
        for character in self._characters:
            if character in self.REQUIRES_ESCAPE:
                write('\\')
            write(character)
        write(']')
        self._str = ''.join(output)


class WordSet(RE):
    # There is a huge opportunity for optimization here

    def __init__(self, values):
        self._str = "(?:%s)" % '|'.join(map(re.escape, values))


class NumericRange(RE):

    def __new__(self, low, high, zeropad=False):
        low = int(low)
        high = int(high)
        if low < 0:
            raise ValueError('low must be >= 0')
        if high < low:
            raise ValueError('high must be > low')

        if not zeropad:
            return WordSet(map(str, range(low, high)))

        values = []
        for value in xrange(low, high):
            value = str(value)
            values.append(value)
            while len(str(value)) < len(str(high)):
                value = '0' + value
                values.append(value)
        return WordSet(values)


class _Anything(RE):

    def __init__(self):
        self._str = '.'


Anything = _Anything()
WhiteSpace = CharacterSet(string.whitespace)
