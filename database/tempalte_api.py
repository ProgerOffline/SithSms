# -*- coding: utf-8 -*-

from .models import MessageTemplate


async def create(owner_tg_id, name, content):
    record = await MessageTemplate(
        owner_tg_id=owner_tg_id,
        name=name,
        content=content,
    ).create()

    return record


async def get_one(record_id):
    record = await MessageTemplate.query.where(
        MessageTemplate.id == record_id
    ).gino.first()

    return record


async def get_all(owner_tg_id):
    records = await MessageTemplate.query.where(
        MessageTemplate.owner_tg_id == owner_tg_id,
    ).gino.all()

    return records


async def update_name(record_id, new_name):
    record = await get_one(record_id)
    
    new_record = await record.update(
        name=new_name
    ).apply()

    return await get_one(record_id)


async def update_content(record_id, new_content):
    record = await get_one(record_id)

    new_record = await record.update(
        content=new_content,
    ).apply()

    return await get_one(record_id)


async def delete(record_id):
    record = await get_one(record_id)
    await record.delete()