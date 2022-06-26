# -*- coding: utf-8 -*-

from gino import Gino
from sqlalchemy import Column, BigInteger, Sequence, String, Text, Integer


db = Gino()


class SmsAccount(db.Model):
    __tablename__ = "sms_account"
    id = Column(BigInteger, Sequence("smsaccount_id_seq"), primary_key=True)
    owner_tg_id = Column(BigInteger)
    name = Column(String)
    access_key = Column(String)
    mailing_system = Column(String)


class MessageTemplate(db.Model):
    __tablename__ = "message_template"
    id = Column(BigInteger, Sequence("messagetemplate_id_seq"), primary_key=True)
    owner_tg_id = Column(BigInteger)
    name = Column(String)
    content = Column(Text)


class Proxy(db.Model):
    __tablename__ = "proxies"
    db_id = Column(BigInteger, Sequence("db_proxies_seq"), primary_key=True)
    ip = Column(String)
    port = Column(Integer)
    login = Column(String)
    password = Column(String)
    status = Column(String)
    mailing_system = Column(String)