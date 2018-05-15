import unittest

from hamcrest import equal_to, is_not
from hamcrest.core import assert_that

from reggie.core import *


class ReggieTest(unittest.TestCase):
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

    def test_or_escapes(self):
        term = one_of(escape('+1'), digit)
        assert_that(match(term,'+1'), is_not(None))
        assert_that(match(term,'1'), is_not(None))
        assert_that(match(term,'a'), equal_to(None))
        assert_that(match(term,'+2'), equal_to(None))

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


    def test_texts(self):
        term = one_of('AA','BB','CCC','D')
        assert_that(match(term,'AA'), is_not(None))
        assert_that(match(term,'AAA'), equal_to(None))
        assert_that(match(term,'BB'), is_not(None))
        assert_that(match(term,'CCC'), is_not(None))
        assert_that(match(term,'D'), is_not(None))

    def test_multiple(self):
        term = name(multiple(osp + one_of('NOP', 'CLA', 'CLL', 'CMA', 'CML', 'RAR', 'RAL', 'RTR', 'RTL', 'IAC')),
                  'group1')
        assert_that('group1' in match(term,'CLL'))
        assert_that(match(term, 'CLL CMA')['group1'], equal_to('CLL CMA'))

    def test_one_or_more(self):
        term = multiple('foo',1,0)
        assert_that(match(term,'foo'), is_not(None))
        assert_that(match(term,'foofoo'), is_not(None))
        assert_that(match(term,'foobar'), equal_to(None))

    def test_two(self):
        term = multiple('foo',2)
        assert_that(match(term,'foo'), equal_to(None))
        assert_that(match(term,'foofoo'), is_not(None))
        assert_that(match(term,'foobar'), equal_to(None))

    def test_multiple_ranged(self):
        term = multiple('foo',1,2)
        assert_that(match(term,''), equal_to(None))
        assert_that(match(term,'foo'), is_not(None))
        assert_that(match(term,'foofoo'), is_not(None))
        assert_that(match(term,'foofoofoo'), equal_to(None))

    def test_opt(self):
        term = multiple('foo',0,1)
        assert_that(match(term,''), is_not(None))
        assert_that(match(term,'foo'), is_not(None))
        assert_that(match(term,'foofoo'), equal_to(None))

    def test_csv(self):
        term=csv('A')
        assert_that(match(term,'A'), is_not(None))
        assert_that(match(term,'A,BB,C'), equal_to(None))
        term=csv('A','BB','C')
        assert_that(match(term,'A,BB,C'), is_not(None))




