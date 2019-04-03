from reggie.core import *

d3 = multiple(digit, 3)
d4 = d3 + digit
international = name(optional(escape('+1')),'i')
area = optional(osp + lp + name(d3,'area') + rp)
local = osp + name(d3,'exchange') + dash + name(d4,'number')
number = international + area + local


def convert(text, area_default='123'):
    matched = match_line(number, text)
    if matched is None:
        return None
    default(matched, 'i','+1')
    default(matched, 'area', area_default)
    return '{i} {area} {exchange} {number}'.format(**matched)


if __name__ == '__main__':
    print(convert('(123) 345-2192'))
    print(convert('345-2192'))
    print(convert('+1 (123) 345-2192'))
