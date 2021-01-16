#!/usr/bin/env python

import re

line = "(($var_1*$var2)-$var3)"

matchObj = re.findall( r'\$\w*', line, flags=0)
line = line.replace('$var_1', str(10))
print(line)
for match in matchObj:
    line = line.replace(match, match+'_repaced')
    print(match.replace('$', ''))

print("Replaced string ", line)

