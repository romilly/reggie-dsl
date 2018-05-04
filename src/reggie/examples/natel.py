from reggie.core import *

d3 = digit + digit + digit
d4 = d3 + digit
international = opt(text('+1').called('i'))
area = opt(osp + lp + d3.called('area') + rp)
local = osp + d3.called('exchange') + dash + d4.called('number')
number = international + area + local


def convert(text, area_default='123'):
    match = number.matches(text)
    if match is None:
        return None
    default(match, 'i','+1')
    default(match, 'area', area_default)
    return '{i} {area} {exchange} {number}'.format(**match)

print(convert('(123) 345-2192'))
print(convert('345-2192'))
print(convert('+1 (123) 345-2192'))
