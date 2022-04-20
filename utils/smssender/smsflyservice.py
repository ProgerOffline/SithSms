# -*- coding: utf-8 -*-

import requests


class SmsFlyService:
    def __init__(self, access_key: str, account_name: str):
        self.access_key = access_key
        self.api_url = "https://sms-fly.ua/api/v2/api.php"

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

        response = requests.post(self.api_url, json=request_data)
        return response.text
