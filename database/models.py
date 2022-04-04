# -*- coding: utf-8 -*-

from gino import Gino
from sqlalchemy import Column, BigInteger, Sequence, String


db = Gino()


class SmsAccount(db.Model):
    __tablename__ = "sms_account"
    id = Column(BigInteger, Sequence("smsaccount_id_seq"), primary_key=True)
    owner_tg_id = Column(BigInteger)
    name = Column(String)
    access_key = Column(String)
    mailing_system = Column(String)