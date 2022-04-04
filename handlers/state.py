# -*- coding: utf-8 -*-

from aiogram import types
from loader import dp
from statesgroup import SettingsMenu
from aiogram.dispatcher import FSMContext


@dp.message_handler(state=SettingsMenu.choose_mailing_system)
async def choose_mailing_system(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['mailing_system'] = message.text