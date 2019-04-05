# Simpler regular expressions in Python

This version (still alpha) inroduces a breaking chage to the API.

The method `match` actually tries tp match an entire string; in other words,
the regex you provide is prefixes by `^` and followed by `$`

That method is now called `match_line`; `match` will now, by default,
try to match anywhere within the string being searched.

![Build status](https://api.travis-ci.org/romilly/reggie-dsl.svg?branch=master)

Regular Expressions are powerful but they can be hard to tame.

There’s an old programmer’s joke:

    A programmer has a problem, and she decides to use regular expressions.
    Now she has two problems.

Unless you use regular expressions regularly (sorry for the awful pun!), they can be

* Hard to read
* Hard to write
* Hard to debug

*reggie* makes regular expressions readable and easy to use.

I've used regular expressions for a number of projects over the years, but the idea for *reggie* came
about a decade ago.

I was working on a project where [Nat Pryce](http://www.natpryce.com/) and I had to parse CDRs (Call Detail Records).
These are text files that Telecommunication Service Providers use to identify calls and other services billable to
their customers.

The CDRs we received were CSV files with a complex format and we decided to use regexes
(Regular Expressions) to verify and interpret them.

We liked regexes, but they were less popular with our business analysts.
The BAs were happy with our Java code, but they found the regexes much less readable.

[Nat Pryce](http://www.natpryce.com/) and I came up with a simple DSL (Domain Specific Language) which we used to
describe and then analyse the CDRs. That made it much easier for our BAs and Testers to
understand our code, and developers joining the team mastered the code quickly.

The Java syntax was a bit messy, though. These days I do most of my development in
Python or APL, and a couple of years ago I realised that Python's syntax would allow a
much cleaner implementation, which I called *reggie*.

It's been useful for several projects, and I decided to share it. You can now use *reggie* for your own work; it's
[available on GitHub](https://github.com/romilly/reggie).

## A simple example 

Here's the solution to a classic problem, converting variants of North American
telephone numbers to international format.

(The code is in the examples directory).

    from reggie.core import *

    d3 = digit + digit + digit
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
    
    print(convert('(123) 345-2192'))
    print(convert('345-2192'))
    print(convert('+1 (123) 345-2192'))
    
Here's the output:

    +1 123 345 2192
    +1 123 345 2192
    +1 123 345 2192

## CDR Example

The next example is inspired by the original Java-based project.

Here's a **simplified** example of the format of CDRs (Call Data Records) for UK Land Lines and a raw regex
(ugh) that could be used to parse it.


    Type,   Caller,         Called,        Date,       Time,       Duration,   Call Class
    N,      +448000077938,  +441603761827, 09/08/2015, 07:00:12,   2,
    N,      +448450347920,  +441383626902, 27/08/2015, 23:53:15,   146,
    V,      +441633614985,  +441633435179, 27/08/2015, 18:36:14,   50,
    V,      +441733360100,  +441733925173, 12/08/2015, 02:49:24,   78,
    V,      +442074958968,  ,              05/08/2015, 08:01:11,   9,          CALLRETURN
    D,      +441392517158,  +447917840223, 22/08/2015, 10:14:39,   2,
    V,      +441914801773,  ,              18/08/2015, 17:29:50,   7,           ALARM CALL
    
Regex: (one long line, split for readability, not a pretty sight!)

    (?P<type>(N|V|D)),(?P<caller>\+[0-9]{12,15}),(?P<called>(?:\+[0-9]{12,15})?)
    (?P<date>[0-9]{2,2}/[0-9]{2,2}/[0-9]{4,4}),(?P<time>[0-9]{2,2}:[0-9]{2,2}:[0-9]{2,2}),
    (?P<duration>[0-9]{1,1}),(?P<call_class>[A-Z]{0,50})

For educational purposes, I've adapted the CDR specification/sample data from the
official standard provided by [FCS](http://www.fcs.org.uk/member-groups/billing).

I've also omitted a lot of fields and inserted spaces to clarify the layout.
The spaces are not present in a real file and the regex examples correctly assume
there are no spaces in a real CDR.

Below it you can see the definition of the format using **reggie**.

    from reggie.core import *

    call_type = name(one_of('N','V','D'),'call_type')
    number = plus + multiple(digit, 12, 15)
    dd = multiple(digit, 2, 2)
    year = multiple(digit, 4 ,4)
    date =  name(dd + slash + dd + slash + year,'date')
    time = name(dd + colon + dd + colon + dd,'time')
    duration = name(multiple(digit),'duration')
    cc = name(multiple(capital, 0, 50),'call_class')
    cdr = csv(call_type, name(number,'caller'), name(optional(number),'called'),date, time, duration, cc)

Now you can try to parse some CDRs. The last one is wrongly formatted.

Parsing a well-formed record returns a Python dictionary.

Parsing an ill-formed record returns the value `None`.

So running

    print(cdr.matches('N,+448000077938,+441603761827,09/08/2015,07:00:12,2,'))
    print(cdr.matches('V,+442074958968,,05/08/2015,08:01:11,9,CALLRETURN'))
    print(cdr.matches('Rubbish!'))
  
will print

    {'caller': '+448000077938', 'call_type': 'N', 'date': '09/08/2015', 'called': '+441603761827', 'duration': '2', 'time': '07:00:12'}
    {'caller': '+442074958968', 'call_type': 'V', 'date': '05/08/2015', 'duration': '9', 'call_class': 'CALLRETURN', 'time': '08:01:11'}
    None

## Other Applications

I've used *reggie* to build parsers for simple languages. Regular Expressions have some limitations -
in particular, you can't use standard regular expressions to analyse recursive grammars.
But there are a surprising number of applications where a DSL without recursion does the trick.

I've recently been working on an emulator for the venerable (and wonderful) PDP-8 computer, and I needed to create a
Python assembler for PAL, the PDP-8's assembly language. The assembler uses *reggie* and it's about an
A4 page of fairly simple code.

I've also been working on [Breadboarder](https://github.com/romilly/breadboarder),
a DSL for documenting breadboard-based electronics projects. At present you have
to define your project using Python code but I think I can use *reggie* to create a natural-language version.

Watch this space!

Morten Kromberg and I have also been experimenting with an APL version of *reggie*. APL syntax is well suited to
*reggie*, and the experiments look very promising. I'll blog about that once the code has stabilised.

In the meantime, take a look at the Python version and leave a comment to let me know what you think of it!




