import re


def escape(text):
    return ''.join(escape_character(ch) for ch in text)


def escape_character(ch):
    return ch if ch not in '.^$*+?{}[]\|()' else r'\%s' % ch


def ncg(term):
    if term.startswith('(') and term.endswith(')'):
        return term
    else:
        return '(?:%s)' % term


def multiple(term, minimum=None, maximum=None):
    if maximum is None:
        if minimum is None:
            return term+'+'
        else:
            maximum = minimum
    term = ncg(term)
    if minimum == 1 and maximum == 0:
        return term+'+'
    if minimum == 0 and maximum == 1:
            return term+'?'
    first = str(minimum)
    second = '' if maximum == 0 else str(maximum)
    return '%s{%s,%s}' % (term, first, second)


def optional(term):
    return ncg(term)+'?'


def one_of(*options, escape=False):
    if escape:
        options = map(escape, options)
    return '(%s)' % '|'.join(options)


def names_in(regex):
    pass


def match(regex, text, line=True):
    if line:
        regex = '^%s$' % regex
    rx = re.compile(regex)
    matched = rx.match(text)
    if matched is None:
        return None
    result = {}
    for name in rx.groupindex.keys():
        value = matched.group(name)
        if value:
                    result[name] = value
    return result


def name(text, name):
    return '(?P<%s>%s)' % (name, text)


def default(matched, key, value):
    if key not in matched:
        matched[key] = value


def csv(field1, *fields):
    result = field1
    for field in fields:
        result = result + comma + field
    return result

comma = ','
slash = '/'
colon = ':'
space = '\s'
spaces = '\s+'
osp = '\s?'
plus = escape('+')
digit = '\d'
digits = multiple(digit)
capital = '[A-Z]'
letter = '[A-Za-z]'
capitals = multiple(capital)
character = '.'
characters = multiple(character)
an = one_of(digit, letter)
identifier = capital + multiple(an, 0, 0)
lp = escape('(')
rp = escape(')')
dash = escape('-')
