from unittest import TestCase

from hamcrest import equal_to, is_not
from hamcrest.core import assert_that

from reggie.core import *


class ReggieTest(TestCase):
    def test_matches_digit(self):
        term = digit
        assert_that(term.matches('1'), is_not(None))
        assert_that(term.matches('11'), equal_to(None))
        assert_that(term.matches('A'), equal_to(None))

    def test_matches_digits(self):
        term = digits
        assert_that(term.matches('1'), is_not(None))
        assert_that(term.matches('12'), is_not(None))
        assert_that(term.matches('A'), equal_to(None))

    def test_capital(self):
        term = capital
        assert_that(term.matches('A'), is_not(None))
        assert_that(term.matches('a'), equal_to(None))
        assert_that(term.matches('A1'), equal_to(None))
        assert_that(term.matches('1'), equal_to(None))

    def test_or(self):
        term = capital | digit
        assert_that(term.matches('A'), is_not(None))
        assert_that(term.matches('1'), is_not(None))
        assert_that(term.matches('a'), equal_to(None))
        assert_that(term.matches('A1'), equal_to(None))


    def test_add(self):
        term = capital + digit
        assert_that(term.matches('A1'), is_not(None))
        assert_that(term.matches('a'), equal_to(None))
        assert_that(term.matches('1'), equal_to(None))
        assert_that(term.matches('1A'), equal_to(None))

    def test_text(self):
        term = plus
        assert_that(term.matches('+'), is_not(None))
        assert_that(term.matches('A'), equal_to(None))
        assert_that(term.matches('1'), equal_to(None))

    def test_optional(self):
        term = optional(capitals)
        assert_that(term.matches(''), is_not(None))
        assert_that(term.matches('A'), is_not(None))
        assert_that(term.matches('AA'), is_not(None))
        assert_that(term.matches('1'), equal_to(None))

        # TODO: add tests for NamedGroups

    def test_texts(self):
        term = texts('AA','BB','CCC','D')
        assert_that(term.matches('AA'), is_not(None))
        assert_that(term.matches('AAA'), equal_to(None))
        assert_that(term.matches('BB'), is_not(None))
        assert_that(term.matches('CCC'), is_not(None))
        assert_that(term.matches('D'), is_not(None))



