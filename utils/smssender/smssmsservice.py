# -*- coding: utf-8 -*-

import requests


class SmsSmsService:
    def __init__(self, account_name: str, access_key: str):
        self.api_url = f"http://{account_name}:{access_key}@sms-fly.com/api/api.php"
        self.headers = {"Content-Type" : "application/xml"}

    def send_message_to_phone_number(self, phone_number: str, text: str):
        request_data = f"""
            <?xml version="1.0" encoding="utf-8"?>
            <request>
                <operation>SENDSMS</operation>
                <message start_time=" AUTO " 
                         end_time=" AUTO " 
                         lifetime="4" 
                         rate="120" 
                         desc="My first campaign " 
                         source="InfoCentr"
                >

                    <body>{text.encode("utf-8")}</body>
                    <recipient>{phone_number}</recipient>
                </message>
            </request>
        """
        response = requests.post(
            url=self.api_url,
            data=request_data,
            headers=self.headers,
        )
        return response.text
