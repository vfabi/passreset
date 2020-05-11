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

import os
import json
import logging
from flask_simple_captcha import CAPTCHA
from ..modules.userdb_backend.ldap import BackendLDAP
from .email import EmailTransportAwsSes, EmailTransportEmailServer


def get_variables():
    """Get all variables, from config and enviroment."""
    config = open(os.path.dirname(__file__) + '/../../config.json')
    vs = json.loads(config.read())
    vs['EMAIL_TRANSPORT'] = os.getenv('EMAIL_TRANSPORT', None)
    vs['EMAIL_SERVER_ADDRESS'] = os.getenv('EMAIL_SERVER_ADDRESS', None)
    vs['EMAIL_SERVER_PORT'] = os.getenv('EMAIL_SERVER_PORT', None)
    vs['EMAIL_SERVER_USER'] = os.getenv('EMAIL_SERVER_USER', None)
    vs['EMAIL_SERVER_PASSWORD'] = os.getenv('EMAIL_SERVER_PASSWORD', None)
    vs['EMAIL_AWSSES_ACCESS_KEY'] = os.getenv('EMAIL_AWSSES_ACCESS_KEY', None)
    vs['EMAIL_AWSSES_SECRET_KEY'] = os.getenv('EMAIL_AWSSES_SECRET_KEY', None)
    vs['EMAIL_AWSSES_REGION'] = os.getenv('EMAIL_AWSSES_REGION', None)
    vs['EMAIL_AWSSES_SENDER'] = os.getenv('EMAIL_AWSSES_SENDER', None)
    vs['BACKEND_TYPE'] = os.getenv('BACKEND_TYPE', None)
    vs['LDAP_SERVER_ADDRESS'] = os.getenv('LDAP_SERVER_ADDRESS', None)
    vs['LDAP_SERVER_USE_SSL'] = os.getenv('LDAP_SERVER_USE_SSL', False)
    vs['LDAP_SERVER_PORT'] = os.getenv('LDAP_SERVER_PORT', 389)
    vs['LDAP_SERVER_USER'] = os.getenv('LDAP_SERVER_USER', None)
    vs['LDAP_SERVER_PASSWORD'] = os.getenv('LDAP_SERVER_PASSWORD', None)
    vs['LDAP_SERVER_SEARCH_RDN'] = os.getenv('LDAP_SERVER_SEARCH_RDN', None)
    return vs

variables = get_variables()


class CustomCaptcha(CAPTCHA):
    """Redefined CAPTCHA from flask_simple_captcha.
    
    Note:
        Redefined because of captcha_html method, mo make custom nice form.
    """

    def captcha_html(self, captcha):
        inpu = '<input type="hidden" name="captcha-hash" value="%s">' % captcha['hash']
        img = '<img class="simple-captcha-img" src="data:image/png;base64, %s" />' % captcha['img']
        return '%s\n%s' % (img, inpu)


class SecurityHandler:
    """Security handler to react on security related events, logging, etc."""

    def __init__(self, logger):
        self.logger = logger

    def log(self, message):
        self.logger.warning(message)

    def process(self, message=None, ipaddress=None):
        self.log(f'message="{message}", ipaddress="{ipaddress}"')


# Email transport
if variables['EMAIL_TRANSPORT'] == 'aws_ses':
    mailer = EmailTransportAwsSes(variables)
elif variables['EMAIL_TRANSPORT'] == 'email_server':
    mailer = EmailTransportEmailServer(variables)
else:
   raise Exception('EMAIL_TRANSPORT variable is not set or have incorrect value.')


# User DB backend
if variables['BACKEND_TYPE'] == 'ldap':
    backend = BackendLDAP(variables)
else:
   raise Exception('BACKEND_TYPE variable is not set or have incorrect value.')