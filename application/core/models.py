#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    @project: passreset
    @component: core
    @copyright: © 2020 by vfabi
    @author: vfabi
    @support: vfabi
    @inital date: 2020-05-08 21:08:07
    @license: this file is subject to the terms and conditions defined
        in file 'LICENSE', which is part of this source code package
    @description:
    @todo:
"""

import json
from jsondb import Database
from .utils import variables


class ResetLinkModel:
    """Database model to store generated reset links."""

    def __init__(self):
        self.db = Database(variables['db'])

    def add(self, resetlink, email):
        self.db.data(key=resetlink, value=email)

    def get(self, resetlink):
        return self.db.data(key=resetlink)

    def exists(self, resetlink):
        return resetlink in self.db

    def delete(self, resetlink):
        self.db.delete(resetlink)
