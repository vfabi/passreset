#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    @project: passreset
    @component: modules
    @copyright: © 2020 by vfabi
    @author: vfabi
    @support: vfabi
    @inital date: 2020-05-08 21:08:07
    @license: this file is subject to the terms and conditions defined
        in file 'LICENSE', which is part of this source code package
    @description:
    @todo:
"""

from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
from . import BackendBase


class BackendLDAP(BackendBase):
    """LDAP users database backend."""

    def __init__(self, variables):
        super().__init__()
        use_ssl = True if variables['LDAP_SERVER_USE_SSL'] == "True" else False
        self.server = Server(variables['LDAP_SERVER_ADDRESS'], port=int(variables['LDAP_SERVER_PORT']), use_ssl=use_ssl, get_info=ALL)
        self.variables = variables

    def change_password(self, email, password):
        try:
            ldap = Connection(self.server, self.variables['LDAP_SERVER_USER'], self.variables['LDAP_SERVER_PASSWORD'], auto_bind=True)
            ldap.search(self.variables['LDAP_SERVER_SEARCH_RDN'], f'(&(objectclass=inetOrgPerson)(mail={email}))')
            entry_dn = ldap.entries[0].entry_dn
            ldap.modify(entry_dn, {'userPassword': [(MODIFY_REPLACE, [password])]})
        except Exception as e:
            raise Exception(f'[{__class__.__name__}.change_password] {e}')
    
    def check_exists(self, email):
        try:
            ldap = Connection(self.server, self.variables['LDAP_SERVER_USER'], self.variables['LDAP_SERVER_PASSWORD'], auto_bind=True)
            return ldap.search(self.variables['LDAP_SERVER_SEARCH_RDN'], f'(&(objectclass=inetOrgPerson)(mail={email}))')
        except Exception as e:
            raise Exception(f'[{__class__.__name__}.check_exists] {e}')
