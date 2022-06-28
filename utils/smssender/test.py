# -*- coding: utf-8 -*-

from smsflyservice import SmsFlyService
from smsclubservice import SmsClubService

import time

proxy = "socks5://mandaloreccs:wFaPm8NBkfOrTAmMUDz2@217.77.218.120:1054"
service = SmsFlyService("2qShJV8A36clDj5O8xvzlATYRU6kx1A5", "sdfsd", proxy=proxy)
response = service.send_message_to_phone_number("+380507496037", "Hello")
print(response)

while True:
    print(response)
    response = service.get_message_status(response['data']['messageID'])
    time.sleep(0.5)

# service = SmsClubService("w17vcQsrpHRgcmV")