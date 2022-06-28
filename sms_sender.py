# -*- coding: utf-8 -*-

import sys
import asyncio
from database import create_db
from database import proxy_api
from utils.smssender import SmsSender


async def main(mailing_system, access_key, template_content, phones_file_path, account_name):
    await create_db(drop_all=False)
    # Запускаем рассылку
    proxy = await proxy_api.get_active()
    service = SmsSender(
        mailing_system=mailing_system,
        access_key=access_key,
        template_content=template_content,
        phones_file_path=phones_file_path,
        account_name=account_name,
    )

    try:
        service.start_sending_sms(proxy)
    except Exception as e:
        print(e)    
        await proxy_api.set_lock_status(proxy.db_id)


if __name__ == "__main__":
    # Принимаем аргуметы
    mailing_system, access_key, template_content, phones_file_path, account_name = sys.argv[1:]
    asyncio.run(main(mailing_system, access_key, template_content, phones_file_path, account_name))