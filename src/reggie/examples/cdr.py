from reggie.core import *

call_type = options('N','V','D').called('call_type')
number = plus + multiple(digit, 12, 15)
dd = multiple(digit, 2, 2)
year = multiple(digit, 4 ,4)
date =  (dd + slash + dd + slash + year).called('date')
time = (dd + colon + dd + colon + dd).called('time')
duration = multiple(digit).called('duration')
cc = (multiple(capital, 0, 50)).called('call_class')
cdr = csv(call_type, number.called('caller'), optional(number).called('called'),date, time, duration ,cc)

print(cdr.matches('N,+448000077938,+441603761827,09/08/2015,07:00:12,2,'))
print(cdr.matches('V,+442074958968,,05/08/2015,08:01:11,9,CALLRETURN'))
print(cdr.matches('Rubbish!'))
