# -*- coding: utf-8 -*-

from aiogram import types
from loader import dp
from keyboards import reply


@dp.message_handler(text="⚙️ Настройки")
async def show_settings(message: types.Message):
    await message.answer(
        text="❔ Выберите систему где вы хотите редактировать аккаунты:",
        reply_markup=await reply.settings_menu(),
    )


@dp.message_handler(text="🔨 Настройка шаблонов")
async def show_templates(message: types.Message):
    pass