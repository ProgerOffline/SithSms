# -*- coding: utf-8 -*-

from .models import SmsAccount
from sqlalchemy.sql import and_


async def create(owner_tg_id, name, access_key, mailing_system):
    record = await SmsAccount(
        owner_tg_id=owner_tg_id,
        name=name,
        access_key=access_key,
        mailing_system=mailing_system,
    ).create()

    return record


async def delete(record_id):
    account = await get_one(record_id)
    await account.delete()


async def get_all(owner_tg_id, mailing_system):
    records = await SmsAccount.query.where(
        and_(
            SmsAccount.owner_tg_id == owner_tg_id,
            SmsAccount.mailing_system == mailing_system,
        )
    ).gino.all()

    return records


async def get_one(record_id):
    record = await SmsAccount.query.where(
        SmsAccount.id == record_id
    ).gino.first()

    return record


async def update_name(record_id, new_name):
    record = await get_one(record_id)

    new_record = await record.update(
        name=new_name,
    ).apply()

    return new_record


async def update_access_key(record_id, new_access_key):
    record = await get_one(record_id)

    new_record = await record.update(
        access_key=new_access_key,
    ).apply()

    return new_record