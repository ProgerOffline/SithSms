# -*- coding: utf-8 -*-

import requests


class SmsFlyService:
    def __init__(self, access_key: str, accont_name: str, proxy: str = ""):
        self.access_key = access_key
        self.api_url = "https://sms-fly.ua/api/v2/api.php"
        
        if proxy == "":
            self.use_proxy = False
        else:
            self.use_proxy = True
        self.proxy = {"https" : proxy}

    def send_message_to_phone_number(self, phone_number: str, text: str):
        request_data = {
            "auth": {
                "key": self.access_key,
            },
            "action": "SENDMESSAGE",
            "data": {
                "recipient": phone_number,
                "channels": [
                    "sms",
                ],
                "sms": {
                    "source": "InfoCenter",
                    "ttl": 5,
                    "text": text,
                }
            }
        }

        response = requests.post(self.api_url, json=request_data, proxies=self.proxy)
        return response.text

    def get_balance(self):
        request_data = {
            "auth": {
                "key": self.access_key,
            },
            "action": "GETBALANCE",
        }

        if self.use_proxy:
            response = requests.post(self.api_url, json=request_data, proxies=self.proxy)
        else:
            response = requests.post(self.api_url, json=request_data)

        return response.text
