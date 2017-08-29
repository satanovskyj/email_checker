# -*- coding: utf-8 -*-

import time


class EnumBool:

    UNKNOWN = 'unknown'
    NO = 'no'
    YES = 'yes'


def retry(max_attempts, sleep_time):
    def retry_decorator(function):
        def _wrapper(*args, **kwargs):
            attempt = 0
            while True:
                attempt += 1
                try:
                    return function(*args, **kwargs)
                except:
                    if attempt >= max_attempts:
                        return

                    time.sleep(sleep_time)

        return _wrapper

    return retry_decorator
