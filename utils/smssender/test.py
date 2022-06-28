# -*- coding: utf-8 -*-

from smsflyservice import SmsFlyService
from smsclubservice import SmsClubService


# proxy = "http://F4026BM2:tehayaf750@45.138.96.81l8"
# service = SmsFlyService("F8YNa1fyuHZvlLjLS9rNwSqfbfls76mJ", "sdfsd")
# print(service.get_balance())

service = SmsClubService("w17vcQsrpHRgcmV")
print(service.send_message_to_phone_number("+380507496037", "dsfas"))