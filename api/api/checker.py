# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import DNS
import smtplib

import helpers


class Checker(object):

    SLEEP_TIME = 1
    MAX_ATTEMPTS = 2

    MX_RECORD = 'MX'

    DEFAULT_TIMEOUT = 3
    STATUS_SUCCEEDED = 250
    SMTP_PORTS = [25, 587, 465]

    def run(self, email):
        email_hostname = email.split('@')[-1]
        mx_records = self._check_mx_record(email_hostname)
        if not mx_records:
            return helpers.EnumBool.NO

        for _, mx_record in mx_records:
            for port in self.SMTP_PORTS:
                check_result = self._check_mailbox(email, mx_record, port)
                if check_result is None:
                    continue

                return check_result

        return helpers.EnumBool.UNKNOWN

    def _check_mx_record(self, hostname):
        try:
            return DNS.mxlookup(hostname)
        except DNS.ServerError:
            return

    @helpers.retry(max_attempts=MAX_ATTEMPTS, sleep_time=SLEEP_TIME)
    def _check_mailbox(self, email, mx_record, port):
        smtp_server = smtplib.SMTP(timeout=self.DEFAULT_TIMEOUT)
        smtp_server.connect(mx_record, port)
        status, _ = smtp_server.helo()
        if status != self.STATUS_SUCCEEDED:
            smtp_server.quit()
            return

        smtp_server.mail('')
        code, message = smtp_server.rcpt(email)
        smtp_server.quit()

        if code == 250:
            return helpers.EnumBool.YES

        return helpers.EnumBool.NO


checker = Checker()
