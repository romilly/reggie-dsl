import unittest

from hamcrest import equal_to, is_not
from hamcrest.core import assert_that

from reggie.core import *


class ReggieTest(unittest.TestCase):
    def test_matches_digit(self):
        term = digit
        assert_that(match_line(term, '1'), is_not(None))
        assert_that(match_line(term, '11'), equal_to(None))
        assert_that(match_line(term, 'A'), equal_to(None))

    def test_matches_digits(self):
        term = digits
        assert_that(match_line(term, '1'), is_not(None))
        assert_that(match_line(term, '12'), is_not(None))
        assert_that(match_line(term, 'A'), equal_to(None))

    def test_capital(self):
        term = capital
        assert_that(match_line(term, 'A'), is_not(None))
        assert_that(match_line(term, 'a'), equal_to(None))
        assert_that(match_line(term, 'A1'), equal_to(None))
        assert_that(match_line(term, '1'), equal_to(None))

    def test_or(self):
        term = one_of(capital, digit)
        assert_that(match_line(term, 'A'), is_not(None))
        assert_that(match_line(term, '1'), is_not(None))
        assert_that(match_line(term, 'a'), equal_to(None))
        assert_that(match_line(term, 'A1'), equal_to(None))

    def test_or_escapes(self):
        term = one_of(escape('+1'), digit)
        assert_that(match_line(term, '+1'), is_not(None))
        assert_that(match_line(term, '1'), is_not(None))
        assert_that(match_line(term, 'a'), equal_to(None))
        assert_that(match_line(term, '+2'), equal_to(None))

    def test_add(self):
        term = capital + digit
        assert_that(match_line(term, 'A1'), is_not(None))
        assert_that(match_line(term, 'a'), equal_to(None))
        assert_that(match_line(term, '1'), equal_to(None))
        assert_that(match_line(term, '1A'), equal_to(None))

    def test_text(self):
        term = plus
        assert_that(match_line(term, '+'), is_not(None))
        assert_that(match_line(term, 'A'), equal_to(None))
        assert_that(match_line(term, '1'), equal_to(None))

    def test_optional(self):
        term = optional(capitals)
        assert_that(match_line(term, ''), is_not(None))
        assert_that(match_line(term, 'A'), is_not(None))
        assert_that(match_line(term, 'AA'), is_not(None))
        assert_that(match_line(term, '1'), equal_to(None))

    def test_texts(self):
        term = one_of('AA', 'BB', 'CCC', 'D')
        assert_that(match_line(term, 'AA'), is_not(None))
        assert_that(match_line(term, 'AAA'), equal_to(None))
        assert_that(match_line(term, 'BB'), is_not(None))
        assert_that(match_line(term, 'CCC'), is_not(None))
        assert_that(match_line(term, 'D'), is_not(None))

    def test_multiple(self):
        term = name(multiple(osp +
                one_of('NOP', 'CLA', 'CLL', 'CMA', 'CML', 'RAR', 'RAL', 'RTR', 'RTL', 'IAC')),
                'group1')
        assert_that('group1' in match_line(term, 'CLL'))
        assert_that(match_line(term, 'CLL CMA')['group1'], equal_to('CLL CMA'))

    def test_one_or_more(self):
        term = multiple('foo', 1, 0)
        assert_that(match_line(term, 'foo'), is_not(None))
        assert_that(match_line(term, 'foofoo'), is_not(None))
        assert_that(match_line(term, 'foobar'), equal_to(None))

    def test_two(self):
        term = multiple('foo', 2)
        assert_that(match_line(term, 'foo'), equal_to(None))
        assert_that(match_line(term, 'foofoo'), is_not(None))
        assert_that(match_line(term, 'foobar'), equal_to(None))

    def test_multiple_ranged(self):
        term = multiple('foo', 1, 2)
        assert_that(match_line(term, ''), equal_to(None))
        assert_that(match_line(term, 'foo'), is_not(None))
        assert_that(match_line(term, 'foofoo'), is_not(None))
        assert_that(match_line(term, 'foofoofoo'), equal_to(None))

    def test_opt(self):
        term = multiple('foo', 0, 1)
        assert_that(match_line(term, ''), is_not(None))
        assert_that(match_line(term, 'foo'), is_not(None))
        assert_that(match_line(term, 'foofoo'), equal_to(None))

    def test_csv(self):
        term = csv('A')
        assert_that(match_line(term, 'A'), is_not(None))
        assert_that(match_line(term, 'A,BB,C'), equal_to(None))
        term = csv('A', 'BB', 'C')
        assert_that(match_line(term, 'A,BB,C'), is_not(None))

    def test_findall(self):
        term = name(one_of('11', '00'), 'twos')
        assert_that(find_all(term, '110101001'),
                    equal_to([{'twos': '11'}, {'twos': '00'}]))

    # match in re, and in reggie, matches from the start of the string
    # search matches anywhere within the string
    # matchline attempts to match the whole line
    def test_match(self):
        term = 'A'
        assert_that(match(term, 'A'), is_not(None))
        assert_that(match(term, 'A1'), is_not(None))
        assert_that(match_line(term, 'A1'), equal_to(None)) # to illustrate the difference
        assert_that(match(term, '1A'), equal_to(None))
        assert_that(search(term, '1A'), is_not(None)) # to illustrate the difference

