# -*- coding: utf-8 -*-

from aiogram import types
from loader import dp
from keyboards import inline, reply, ctypes
from statesgroup import SettingsMenu


@dp.message_handler(text="⚙️ Настройки", state="*")
async def show_settings(message: types.Message):
    await SettingsMenu.choose_mailing_system.set()
    await message.answer(
        text="❔ Выберите систему где вы хотите редактировать аккаунты:",
        reply_markup=await inline.settings_menu(),
    )


@dp.message_handler(text="🔨 Настройка шаблонов")
async def show_templates(message: types.Message):
    pass