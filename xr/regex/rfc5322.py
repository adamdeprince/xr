from xr import CharacterSet, CharacterRange, Text, NumericRange
from string import ascii_lowercase, digits

AlphaNum = CharacterSet(ascii_lowercase + digits)

# https://www.ietf.org/rfc/rfc5322.html#page-32
ObsQText = CharacterRange(('\x01', '\x08'),('\x0e', '\x1f')) | CharacterSet('\x0b\x0c')

# https://www.ietf.org/rfc/rfc5322.html#page-14
QText = ObsQText | CharacterRange(('\x21', '\x5b'), ('\x5d', '\x7f'))

# https://www.ietf.org/rfc/rfc5322.html#page-11
QuotedPair = CharacterRange(('\x01', '\x09')) | CharacterSet('\x0b\x0c') | CharacterRange(('\x0e', '\x7f'))

# https://www.ietf.org/rfc/rfc5322.html#page-13
AText = CharacterSet(ascii_lowercase + digits + '!#$%&\'*+=?^_`{|}~-')

Name = AText.many(1) + ('.' + AText.many(1)).many()

# https://www.ietf.org/rfc/rfc5322.html#page-14
QuotedString = '"' + (QText | (Text("\\") + QuotedPair)).many() + Text('"')

# Includes dot-atom and dot-atom text from https://www.ietf.org/rfc/rfc5322.html#page-13
Domain = AlphaNum + ((AlphaNum | '-').many() + AlphaNum).maybe()
FQDN = (Domain + "." ).many(1) + Domain

IP = NumericRange(0, 255)

# https://www.ietf.org/rfc/rfc5322.html#page-18
DText = ObsQText | CharacterRange(('\x21', '\x5a'), ('\x5e', '\x7f'))

# https://www.ietf.org/rfc/rfc5322.html#section-4.4
ObsRoute = '[' + ((AlphaNum + '-').many() + AlphaNum) + ':' + (DText | ('\\' + QuotedPair)).many() + ']'
ObsDomain = (IP + '.') * 3 + (IP | ObsRoute)

RFC5322 = (Name | QuotedString) + '@' + (FQDN | ObsDomain)
