# -*- coding: utf-8 -*-

from loader import dp
from aiogram import types
from keyboards import reply


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(
        text="ℹ️ Для отправки СМС - просто отправьте номера в чат!",
        reply_markup=await reply.main_menu(),
    )