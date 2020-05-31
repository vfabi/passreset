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

from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, PasswordField, TextField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.meta import DefaultMeta
from .utils import variables


# class BindNameMeta(DefaultMeta):
#     '''Redefine 'name' field.'''
#     def bind_field(self, form, unbound_field, options):
#         if 'custom_name' in unbound_field.kwargs:
#             options['name'] = unbound_field.kwargs.pop('custom_name')
#         return unbound_field.bind(form=form, **options)


class PasswdResetForm(FlaskForm):
    #Meta = BindNameMeta

    email = EmailField('Email', validators=[DataRequired(), Email()])
    captcha_text = TextField('Captcha', validators=[DataRequired()])
    submit = SubmitField('Reset')


class PasswdChangeForm(FlaskForm):
    new_password = PasswordField(
        'New Password',
        validators=[DataRequired(),
        Length(min=variables['USER_PASSWORD_MIN_SIZE'])]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(),
        Length(min=variables['USER_PASSWORD_MIN_SIZE']),
        EqualTo('new_password',
        message='Both field values must be equal.')]
    )
    submit = SubmitField('Submit')
