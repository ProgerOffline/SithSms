# -*- coding: utf-8 -*-

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from keyboards import inline, ctypes
from statesgroup import SettingsMenu
from database import proxy_api
from database import sms_account_api


@dp.callback_query_handler(
    ctypes.proxy.filter(action="show_all"), 
    state=SettingsMenu.edit_accounts,
)
@dp.callback_query_handler(
    ctypes.proxy.filter(action="back_menu"),
    state=SettingsMenu.edit_proxies,
)
async def edit_proxies(call: types.CallbackQuery, state: FSMContext):
    proxies = await proxy_api.get_all()

    await SettingsMenu.edit_proxies.set()
    await call.message.edit_text(
        text="Выберите прокси",
        reply_markup=await inline.proxy_settings(proxies),
    )

@dp.callback_query_handler(
    ctypes.proxy.filter(action="back"), 
    state=SettingsMenu.edit_proxies,
)
async def show_accountas(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        mailing_system = data['mailing_system']

    account_records = await sms_account_api.get_all(
        owner_tg_id=call.message.chat.id,
        mailing_system=mailing_system,
    )

    await call.answer()
    await SettingsMenu.edit_accounts.set()
    await call.message.edit_text(
        text="Выберите аккаунт",
        reply_markup=await inline.accounts_menu(account_records)
    )


@dp.callback_query_handler(
    ctypes.proxy.filter(action="load_proxy"), 
    state=SettingsMenu.edit_proxies,
)
async def load_proxy(call: types.CallbackQuery, state: FSMContext):
    await SettingsMenu.get_proxies.set()
    await call.message.edit_text(
        text="📩 Отправьте мне список прокси в таком формате: " +\
            "IP:PORT:LOGIN:PASSWORD, разделяя их переносом строки",
    )


@dp.message_handler(state=SettingsMenu.get_proxies)
async def get_proxies(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        mailing_system = data['mailing_system']

    text = message.text
    proxies = text.split("\n")

    try:
        for proxy in proxies:
            proxy = proxy.split(":")
            await proxy_api.create(
                ip=proxy[0],
                port=int(proxy[1]),
                login=proxy[2],
                password=proxy[3],
                mailing_system=mailing_system,
            )
    except:
        await state.finish()
        await mesage.answer(
            text="❌ Произошла ошибка, проверьте правильность данных"
        )
        return

    proxies = await proxy_api.get_all()
    await SettingsMenu.edit_proxies.set()
    await message.answer(
        text="Загрузка успешно завершена",
        reply_markup=await inline.proxy_settings(proxies),
    )


@dp.callback_query_handler(ctypes.proxy.filter(action="show_one"), state=SettingsMenu.edit_proxies)
async def show_one(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    proxy = await proxy_api.get(int(callback_data['id']))
    status = "✅" if proxy.status == "active" else "❌"

    await call.message.edit_text(
        text=f"{status} {proxy.ip}:{proxy.port}:{proxy.login}:{proxy.password}",
        reply_markup=await inline.edit_proxy(proxy)
    )


@dp.callback_query_handler(ctypes.proxy.filter(action="delete"), state=SettingsMenu.edit_proxies)
async def delete(call: types.CallbackQuery, state: FSMContext, callback_data: int):
    proxy = await proxy_api.get(int(callback_data['id']))
    status = "✅" if proxy.status == "active" else "❌"

    await proxy_api.delete(int(callback_data['id']))
    await call.message.edit_text(
        text=f"Прокси {proxy.ip}:{proxy.port}:{proxy.login}:{proxy.password} успешно удален",
    )

    proxies = await proxy_api.get_all()

    await SettingsMenu.edit_proxies.set()
    await call.message.answer(
        text="Выберите прокси",
        reply_markup=await inline.proxy_settings(proxies),
    )