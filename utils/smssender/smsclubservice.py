# -*- coding: utf-8 -*-

import random
import requests


class SmsClubService:
    def __init__(self,
            access_key: str,
            account_name: str,
            proxy: str = "",
            alpha_name: str="",
        ):
        self.access_key = f"Bearer {access_key}"
        self.headers = {
            "Authorization": self.access_key,
            "Content-Type": "application/json",
        }
        
        if proxy == "":
            self.use_proxy = False
        else:
            self.use_proxy = True
        self.proxy = {"https" : proxy}
        self.alpha_name = alpha_name

    def get_alpha_names(self):
        url = "https://im.smsclub.mobi/sms/originator"
        response = requests.post(url, headers=self.headers)

        return response.json()['success_request']['info']

    def get_balance(self):
        url = "https://im.smsclub.mobi/sms/balance"
        response = requests.post(url, headers=self.headers)

        return response.json()

    def send_message_to_phone_number(self, phone_number: str, text: str):
        url = "https://im.smsclub.mobi/sms/send"
        request_data = {
            "phone": [phone_number],
            "src_addr": self.alpha_name,
            "message": text,
        }

        if self.use_proxy:
            response = requests.post(
                url=url,
                headers=self.headers,
                json=request_data,
                proxies=self.proxy,
            )
        else:
            response = requests.post(
                url=url,
                headers=self.headers,
                json=request_data,
            )     

        return response.json()
