# -*- coding: utf-8 -*-

import DNS
import smtplib


class EnumBool:

    NO = 'no'
    YES = 'yes'


class Checker(object):

    MX_RECORD = 'MX'
    STATUS_SUCCEEDED = 250

    def run(self, email):
        email_hostname = email.split('@')[-1]
        mx_records = self._check_mx_record(email_hostname)
        if not mx_records:
            return EnumBool.NO

        for mx_record in mx_records:
            check_result = self._check_mailbox(email, unicode(mx_record[1]))
            if check_result is None:
                continue

            return check_result

        return EnumBool.NO

    def _check_mx_record(self, hostname):
        try:
            return DNS.mxlookup(hostname)
        except DNS.ServerError:
            return

    def _check_mailbox(self, email, mx_record):
        smtp_server = smtplib.SMTP()
        smtp_server.connect(mx_record)
        status, _ = smtp_server.helo()
        if status != self.STATUS_SUCCEEDED:
            smtp_server.quit()
            return

        smtp_server.mail('')
        code, message = smtp_server.rcpt(unicode(email))
        smtp_server.quit()

        if code == 250:
            return EnumBool.YES

        return EnumBool.NO


checker = Checker()
