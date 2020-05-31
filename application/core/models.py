#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    @project: passreset
    @component: core
    @copyright: © 2020 by vfabi
    @author: vfabi
    @support: vfabi
    @initial date: 2020-05-08 21:08:07
    @license: this file is subject to the terms and conditions defined
        in file 'LICENSE', which is part of this source code package
    @description:
    @todo:
"""

import json
import random
from datetime import datetime, timedelta
from jsondb import Database
from .utils import variables


class ResetLinkModel:
    """Database model to store generated reset links."""

    def __init__(self):
        self.db = Database(variables['db'])
    
    def generate(self):
        random_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890') for _ in range(30))
        dt = datetime.now() + timedelta(days=+1)
        dt_string = dt.strftime("%Y%m%d%H%M%S")
        reset_string = f'{random_string}-{dt_string}'
        return reset_string
    
    def _check_expire(self, resetlink):
        now = datetime.now()
        dt_expire_string = resetlink.split('-')[1]
        dt_expire = datetime.strptime(dt_expire_string, "%Y%m%d%H%M%S")
        return dt_expire > now

    def add(self, resetlink, email):
        self.db.data(key=resetlink, value=email)

    def get(self, resetlink):
        return self.db.data(key=resetlink)

    def exists(self, resetlink):
        if resetlink in self.db:
            return self._check_expire(resetlink)
        return False

    def delete(self, resetlink):
        self.db.delete(resetlink)
