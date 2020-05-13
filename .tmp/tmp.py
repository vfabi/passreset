#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Some python code tests

import os
import base64
from datetime import datetime, timedelta


a = datetime.now() + timedelta(days=+1)
print(a)
b = a.strftime("%Y%m%d%H%M%S")
print(b)

# c = base64.b64encode(b.encode('utf-8'))
# print(c)

resetstring = f'23123gjasdad8qwudjhxc312nsidaasd-{b}'
print(resetstring)

dtdecoded = resetstring.split('-')[1]
print(dtdecoded)

dt = datetime.strptime(dtdecoded, "%Y%m%d%H%M%S")
print(dt)

now = datetime.now()
print(now)

if now > dt:
    print('error')
