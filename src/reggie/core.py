"""
regular expressions made easy-ish
"""
from abc import ABCMeta, abstractmethod
import re


def re_for(term):
    reexp = ncg(term).expr() + '$'
    return re.compile(reexp)



class Term():
    __metaclass__ = ABCMeta

    @abstractmethod
    def expr(self):
        pass

    def __add__(self, term):
        return Join(self, term)

    def __or__(self, term):
        return Or(self, term)

    def matches(self, text):
        def values(self, match):
            result = {}
            names = self.names()
            for fieldname in names:
                value = field(self, fieldname, match)
                if value:
                    result[fieldname] = value
            return result

        def field(self, fname, match):
            if not match:
                return None
            return match.group(fname)
        rx = re.compile(re_for(self))
        match = rx.match(text)
        if match is None:
            return None
        return values(self, match)

    def is_simple(self):
        return False

    def called(self, name):
        return NamedGroup(name, self)

    def names(self):
        return []


class Text(Term):
    def __init__(self, text):
        self.text = self.escape(text)

    def expr(self):
        return self.text

    def escape(self, text):
        return ''.join(self.escape_character(ch) for ch in text)

    def escape_character(self, ch):
        return ch if ch not in '.^$*+?{}[]\|()' else r'\%s' % ch


class Osp(Term):
    def expr(self):
        return '\s*'


class NamedGroup(Term):
    def __init__(self, name, term):
        self.name = name
        self.term = term

    def expr(self):
        return '(?P<%s>%s)' % (self.name, self.term.expr())

    def names(self):
        return [self.name]+self.term.names()

class Character(Term):
    def expr(self):
        return '.'

    def is_simple(self):
        return True


class Multiple(Term):
    def __init__(self, term, minimum, maximum):
        self.term = ncg(term)
        self.minimum = minimum
        self.maximum = maximum

    def qualifier(self):
        if self.minimum == 1 and self.maximum == 0:
            return '+'
        first = str(self.minimum)
        second = '' if self.maximum == 0 else str(self.maximum)
        return '{%s,%s}' % (first, second)


    def expr(self):
        return self.term.expr()+self.qualifier()

    def names(self):
        return self.term.names()


class Optional(Term):
    def __init__(self, option):
        self.option = ncg(option)

    def expr(self):
        return self.option.expr()+'?'

    def names(self):
        return self.option.names()


class BinaryTerm(Term):
    __metaclass__ = ABCMeta

    def __init__(self, left, right):
        self.left = left
        self.right = right

    @abstractmethod
    def expr(self):
        pass

    def names(self):
        return self.left.names()+self.right.names()


class Or(BinaryTerm):
    def __init__(self, left, right):
        BinaryTerm.__init__(self, left, right)

    def expr(self):
        return self.left.expr()+'|'+self.right.expr()

    def names(self):
        return self.left.names()+self.right.names()


class Capital(Term):
    def expr(self):
        return '[A-Z]'

    def is_simple(self):
        return True


class Digit(Term):
    def expr(self):
        return '[0-9]'

    def is_simple(self):
        return True


class Join(BinaryTerm):
    def __init__(self, left, right):
        BinaryTerm.__init__(self, left, right)

    def expr(self):
        return self.left.expr()+self. right.expr()


def multiple(term, minimum=1, maximum=1):
    return Multiple(term, minimum, maximum)


def optional(term):
    return Optional(term)


def g(name, term):
    return NamedGroup(name, term)


class NonCapturingGroup(Term):
    def __init__(self, term):
        self.term = term

    def expr(self):
        return '(?:%s)' % self.term.expr()

    def names(self):
        return self.term.names()


def ncg(term):
    if term.is_simple():
        return term
    return NonCapturingGroup(term)


def text(text):
    return Text(text)

osp = Osp()


class Space(Term):
    def expr(self):
        return '\s'


class Options(Term):
    def __init__(self, *options):
        self.options = options

    def expr(self):
        result = '(%s)' % '|'.join(self.options)
        return result


def options(*texts):
    return Options(*texts)

def default(match, key, value):
    if key not in match:
        match[key] = value

# cos I am lazy
def opt(term):
    return optional(term)


def csv(field1, *fields):
    result = field1
    for field in fields:
        result = result + comma + field
    return result

comma = text(',')
slash = text('/')
colon = text(':')
space = Space()
plus = Text('+')
digit = Digit()
digits = multiple(digit)
capital= Capital()
capitals = multiple(capital)
character = Character()
characters = multiple(character)
an = digit | capital
identifier = capital + optional(multiple(an))
lp = text('(')
rp = text(')')
dash = text('-')
