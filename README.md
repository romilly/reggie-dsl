## REGGIE - simpler regexs in Python

Regular expressions are powerful but easy to get wrong and hard to debug.

*REGGIE* is a simple Python DSL for creating and using regular expressions for validation and parsing.

I'm using it for three projects at the moment, and it works well.

It needs more tests and a lot more documentation.

I'll add these if others are interested in using the package,
so let me know if you are!

Here's the solution to a classic problem, converting variants of North American
telephone numbers to international format.

(The code is in the examples directory).

    from reggie.core import *
    
    d3 = digit + digit + digit
    d4 = d3 + digit
    intl = text('+1')
    
    number = optional(intl).called('i')  \
              + optional(osp + lp + d3.called('area') + rp) \
              +(osp + d3.called('exchange') + dash + d4.called('number'))
    
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
    
Here's the output:

    +1 123 345 2192
    +1 123 345 2192
    +1 123 345 2192


