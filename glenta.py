#!/usr/bin/python

import pyzmail
from random import choice

from settings import *

def send_glenta(to, buy_for):
    message = MESSAGE % (to[0], buy_for)

    mail, mail_from, mail_to, msg_id = pyzmail.compose_mail(
        SMTP['from'],
        [to],
        SUBJECT,
        'utf-8',
        (message.encode('iso-8859-1'), 'iso-8859-1')
    )

    result = pyzmail.send_mail(
        mail, mail_from, mail_to,
        SMTP['host'], smtp_port=SMTP['port'], smtp_mode=SMTP['mode'],
        smtp_login=SMTP['login'], smtp_password=SMTP['password']
    )

    print result

def assign(people):
    pool = map(lambda p: p[0], people)
    def pick(name, email, *avoid):
        avoid = list(avoid) + [name]
        limited_pool = [name for name in pool if name not in avoid]
        if not limited_pool:
            raise Exception("No options left for %s" % name)
        buy = choice(limited_pool)
        pool.remove(buy)
        return buy

    assigned = []
    for person in people:
        buy = pick(person[0], person[1], *person[2:])
        assigned.append(((person[0], person[1]), buy))

    return assigned

if __name__ == '__main__':
    assigned = assign(PEOPLE)
    for names in assigned:
        send_glenta(*names)
