# -*- coding: utf-8 -*-

import re
import phonenumbers

from logzero import logger
from .smsflyservice import SmsFlyService


class SmsSender:
    def __init__(self,
        phones_file_path: str,
        mailing_system: str='',
        access_key: str='',
        template_content: str='',
    ):

        self.mailing_system = mailing_system
        self.access_key = access_key
        self.template_content = template_content
        self.phones_list =  self.__sort_phones(phones_file_path)

        self.mailing_services = {
            "sms-fly" : SmsFlyService,
        }
    
    def __sort_phones(self, phones_file_path: str) -> list:
        with open("documents/" + phones_file_path, "r") as file:
            phones_unsroted_list = [
                ''.join(re.findall("\d+", line))
                for line in file.readlines()
            ]

        phones_sorted_list = []
        for phone in phones_unsroted_list:
            if phonenumbers.is_valid_number(phonenumbers.parse(phone, "UA")) and \
                phone not in phones_sorted_list:
                phones_sorted_list.append(phone)
            
        return phones_sorted_list
    
    def start_sending_sms(self):
        service_obj = self.mailing_services[self.mailing_system]
        service = service_obj(self.access_key)

        for phone_number in self.phones_list:
            response = service.send_message_to_phone_number(
                phone_number=phone_number,
                text=self.template_content,
            )

            logger.info(response)
