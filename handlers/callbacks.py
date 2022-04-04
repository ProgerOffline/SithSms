# -*- coding: utf-8 -*-

from aiogram import types
from loader import dp
from keyboards import ctypes, inline
from statesgroup import SettingsMenu
from aiogram.dispatcher import FSMContext
from database import sms_account_api


@dp.callback_query_handler(
    ctypes.mailing_system.filter(),
    state=SettingsMenu.choose_mailing_system,
)
async def get_mailing_system(
    call: types.CallbackQuery, 
    callback_data: dict,
    state: FSMContext,
):
    mailing_system = callback_data['type']

    async with state.proxy() as data:
        data['mailing_system'] = mailing_system

    account_records = await sms_account_api.get_all(
        owner_tg_id=call.message.chat.id,
        mailing_system=mailing_system
    )

    await call.answer()
    await call.message.answer(
        text="Выберите аккаунт",
        reply_markup=inline.accounts_menu(account_records)
    )