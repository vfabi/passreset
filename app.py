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

import os
import logging
from flask import Flask, render_template, flash, redirect, url_for, request
from application.core.forms import PasswdResetForm, PasswdChangeForm
from application.core.models import ResetLinkModel
from application.core.utils import variables, CustomCaptcha, SecurityHandler, mailer, backend


captcha = CustomCaptcha(config={'SECRET_CSRF_KEY': variables['FLASK_SIMPLE_CAPTCHA_SECRET_CSRF_KEY']})
app = Flask(__name__, template_folder=os.path.abspath('application/templates'), static_folder='application/static')
app.config['SECRET_KEY'] = variables['FLASK_SECRET_KEY']
app = captcha.init_app(app)
app.jinja_env.globals.update(variables=variables)
app.logger.handlers[0].setFormatter(logging.Formatter("%(asctime)s [%(name)s] %(levelname)s %(message)s"))
security_handler = SecurityHandler(app.logger)
resetlink_storage = ResetLinkModel()


@app.route("/", methods=['GET', 'POST'])
@app.route("/reset", methods=['GET', 'POST'])
def reset():
    form = PasswdResetForm()
    if form.validate_on_submit():
        try:
            # check captcha
            captcha_hash = request.form.get('captcha-hash')
            captcha_text = request.form.get('captcha_text')
            if not captcha.verify(captcha_text, captcha_hash):
                security_handler.process(message='Invalid captcha.', ipaddress=request.remote_addr, level='warning')
                flash(f'Captcha is not valid. Please try again.', 'warning')
                return redirect(url_for('reset'))
            # check email exists in user database
            if backend.check_exists(form.email.data):
                resetlink_string = resetlink_storage.generate()
                resetlink_url = f'{request.url_root}resetlink/{resetlink_string}/'
                resetlink_storage.add(resetlink_string, form.email.data)
                mailer.sendmail(resetlink_url, form.email.data)
                security_handler.process(message=f'Resetlink sent to {form.email.data}.', ipaddress=request.remote_addr, level='info')
                flash(f'Password reset link sent to {form.email.data}.', 'success')
                return redirect(url_for('reset'))
            else:
                security_handler.process(message=f'Email {form.email.data} was not found in user registry.', ipaddress=request.remote_addr, level='warning')
                flash(f'Email {form.email.data} was not found in user registry', 'warning')
                return redirect("reset")
        except Exception as e:
            security_handler.process(message=f'Exception: {e}.', ipaddress=request.remote_addr, level='error')
            flash(f'Internal error. Details: {e}.', 'danger')
            return render_template('blank.html', title='Error')
    return render_template('reset.html', title=variables['page_title'], form=form, captcha=captcha.create())


@app.route('/resetlink/<string:resetlink>/', methods=['GET', 'POST'])
def article(resetlink):
    if resetlink_storage.exists(resetlink):
        form = PasswdChangeForm()
        if form.validate_on_submit():
            try:
                email = resetlink_storage.get(resetlink)
                backend.change_password(email, form.new_password.data)
                resetlink_storage.delete(resetlink)
                security_handler.process(message=f'Password for {email} was changed.', ipaddress=request.remote_addr, level='info')
                flash('Your password was successfully changed.', 'success')
                return render_template('blank.html', title='Success')
            except Exception as e:
                security_handler.process(message=f'Exception: {e}.', ipaddress=request.remote_addr, level='error')
                flash(f'Internal error. Details: {e}.', 'danger')
                return render_template('blank.html', title='Error')
        return render_template('resetlink_ok.html', title=variables['page_title'], form=form)
    security_handler.process(message='Incorrect link or your link expaired.', ipaddress=request.remote_addr, level='warning')
    flash('Incorrect link or your link expaired.', 'warning')
    return render_template('blank.html', title='Warning'), 403


@app.errorhandler(404)
def page_not_found(e):
    security_handler.process(message='404 Page not found.', ipaddress=request.remote_addr, level='warning')
    return render_template('404.html', title='Error 404'), 404


if __name__ == "__main__":
    app.run(
        debug=False,
        host='0.0.0.0',
        port=8000
    )
