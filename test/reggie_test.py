from unittest import TestCase

from hamcrest import equal_to, is_not
from hamcrest.core import assert_that

from reggie.core import *


class ReggieTest(TestCase):
    def test_matches_digit(self):
        term = digit
        assert_that(match(term,'1'), is_not(None))
        assert_that(match(term,'11'), equal_to(None))
        assert_that(match(term,'A'), equal_to(None))

    def test_matches_digits(self):
        term = digits
        assert_that(match(term,'1'), is_not(None))
        assert_that(match(term,'12'), is_not(None))
        assert_that(match(term,'A'), equal_to(None))

    def test_capital(self):
        term = capital
        assert_that(match(term,'A'), is_not(None))
        assert_that(match(term,'a'), equal_to(None))
        assert_that(match(term,'A1'), equal_to(None))
        assert_that(match(term,'1'), equal_to(None))

    def test_or(self):
        term = one_of(capital, digit)
        assert_that(match(term,'A'), is_not(None))
        assert_that(match(term,'1'), is_not(None))
        assert_that(match(term,'a'), equal_to(None))
        assert_that(match(term,'A1'), equal_to(None))


    def test_add(self):
        term = capital + digit
        assert_that(match(term,'A1'), is_not(None))
        assert_that(match(term,'a'), equal_to(None))
        assert_that(match(term,'1'), equal_to(None))
        assert_that(match(term,'1A'), equal_to(None))

    def test_text(self):
        term = plus
        assert_that(match(term,'+'), is_not(None))
        assert_that(match(term,'A'), equal_to(None))
        assert_that(match(term,'1'), equal_to(None))

    def test_optional(self):
        term = optional(capitals)
        assert_that(match(term,''), is_not(None))
        assert_that(match(term,'A'), is_not(None))
        assert_that(match(term,'AA'), is_not(None))
        assert_that(match(term,'1'), equal_to(None))

        # TODO: add tests for NamedGroups

    def test_texts(self):
        term = one_of('AA','BB','CCC','D')
        assert_that(match(term,'AA'), is_not(None))
        assert_that(match(term,'AAA'), equal_to(None))
        assert_that(match(term,'BB'), is_not(None))
        assert_that(match(term,'CCC'), is_not(None))
        assert_that(match(term,'D'), is_not(None))



