#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Some python code tests

import base64
from datetime import datetime, timedelta


a = datetime.now() + timedelta(days=+1)
print(a)
b = a.strftime("%Y%m%d%H%M%S")
print(b)
c = base64.b64encode(b.encode('utf-8'))
print(c)
