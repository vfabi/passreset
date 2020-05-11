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

import boto3
import smtplib
from email.mime.text import MIMEText as text
from botocore.exceptions import ClientError


EMAIL_SUBJECT_TEMPLATE = "Password reset"

EMAIL_BODY_TEMPLATE = """
Hello,

You requested password reset. Your password reset link {resetlink} will expire in 24h.

---
{signature}
"""


class EmailTransportAwsSes:
    """AWS SES email transport.
    
    Note:
        To use AWS SES as email transport you will need:
        1. AWS access key, AWS secret keys.
        2. AWS user access (policy or role) to AWS SES service.
        3. Add and verify your sender email address in AWS SES.
    """

    def __init__(self, variables):
        self.variables = variables
        self.ses = boto3.client(
            'ses',
            aws_access_key_id = self.variables['EMAIL_AWSSES_ACCESS_KEY'],
            aws_secret_access_key = self.variables['EMAIL_AWSSES_SECRET_KEY'],
            region_name=self.variables['EMAIL_AWSSES_REGION']
        )
        self.charset = 'UTF-8'
        self.sender = self.variables['EMAIL_AWSSES_SENDER']
        self.subject = EMAIL_SUBJECT_TEMPLATE

    def sendmail(self, resetlink, toemail):
        mail_body = EMAIL_BODY_TEMPLATE.format(resetlink=resetlink, signature=self.variables['app_name'])
        try:
            self.ses.send_email(
                Destination={
                    'ToAddresses': [
                        toemail,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': self.charset,
                            'Data': mail_body,
                        },
                    },
                    'Subject': {
                        'Charset': self.charset,
                        'Data': self.subject,
                    },
                },
                Source=self.sender,
            )
        except Exception as e:
            raise Exception(f'[{__class__.__name__}.change_password] {e}')


class EmailTransportEmailServer:
    """SMTP server email transport.
    
    Note:
        To use Gmail as smtp server you will need:
        1. Enable SMTP
        2. Set 'Allow less secure apps: ON' in Google account. More details:
            https://www.tutorialspoint.com/send-mail-from-your-gmail-account-using-python
            https://www.afternerd.com/blog/how-to-send-an-email-using-python-and-smtplib/
    """

    def __init__(self, variables):
        self.sender = variables['EMAIL_SERVER_USER']
        self.subject = EMAIL_SUBJECT_TEMPLATE
        self.variables = variables

    def sendmail(self, resetlink, toemail):
        #server = smtplib.SMTP('smtp.gmail.com', 587)
        #server.starttls()
        #server.login('username', 'password')
        server = smtplib.SMTP_SSL(self.variables['EMAIL_SERVER_ADDRESS'], self.variables['EMAIL_SERVER_PORT'])
        mail_text = EMAIL_BODY_TEMPLATE.format(resetlink=resetlink, signature=self.variables['app_name'])
        mail_body = text(mail_text)
        mail_body['Subject'] = self.subject
        mail_body['From'] = self.sender
        mail_body['To'] = toemail
        server.login(self.variables['EMAIL_SERVER_USER'], self.variables['EMAIL_SERVER_PASSWORD'])
        server.sendmail(
            self.sender, 
            toemail, 
            mail_body.as_string()
        )
        server.quit()
