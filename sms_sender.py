# -*- coding: utf-8 -*-

import sys
from utils.smssender import SmsSender


if __name__ == "__main__":
    # Принимаем аргуметы
    mailing_system, access_key, template_content, phones_file_path, account_name = sys.argv[1:]
    
    # Запускаем рассылку
    service = SmsSender(
        mailing_system=mailing_system,
        access_key=access_key,
        template_content=template_content,
        phones_file_path=phones_file_path,
        account_name=account_name,
    )

    service.start_sending_sms()