from unittest import TestCase
from reggie.core import *


class NATelTest(TestCase):
    def setUp(self):
        d3 = digit + digit + digit
        d4 = d3 + digit
        international = name(optional(escape('+1')),'i')
        area = optional(osp + lp + name(d3,'area') + rp)
        local = osp + name(d3,'exchange') + dash + name(d4,'number')
        self.regex = international + area + local
        self.test_numbers = ['(123) 345-2192','345-2192','+1 (123) 345-2192']

    def test_parses_number_variants(self):
        for number in self.test_numbers:
            self.assertTrue(match(self.regex, number),'%s should match %s' % (self.regex, number))
        rubbish = 'rubbish'
        self.assertFalse(match(self.regex, rubbish), '%s should not match %s' % (self.regex, rubbish))

    def test_supplies_defaults(self):
        for number in self.test_numbers:
            text = self.convert(number)
            self.assertEqual(text, '+1 123 345 2192')

    def convert(self, number):
        area_default='123'
        matched = match(self.regex, number)
        if matched is None:
            return None
        default(matched, 'i','+1')
        default(matched, 'area', area_default)
        return '{i} {area} {exchange} {number}'.format(**matched)
