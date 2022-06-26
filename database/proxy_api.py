# -*- coding: utf-8 -*-

from .models import Proxy
from sqlalchemy.sql import and_


async def create(
        ip: str,
        port: int,
        login: str,
        password: str,
        mailing_system: str,
    ) -> Proxy:
    
    record = await Proxy(
        ip=ip,
        port=port,
        login=login,
        password=password,
        status="active",
        mailing_system=mailing_system,
    ).create()

    return record


async def get_all() -> Proxy:
    records = await Proxy.query.gino.all()
    return records


async def get(db_id: int) -> Proxy:
    record = await Proxy.query.where(
        Proxy.db_id == db_id,
    ).gino.first()

    return record


async def delete(db_id: int):
    record = await get(db_id)
    await record.delete()


async def set_lock_status(db_id: int) -> Proxy:
    record = await get(db_id)
    await record.update(
        status="lock",
    ).apply()

    return await get(db_id)


async def get_active():
    record = await Proxy.query.where(
        Proxy.status == "active",
    ).gino.first()
    return record