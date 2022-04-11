# -*- coding: utf-8 -*-

from loader import dp
from aiogram import types
from keyboards import reply
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['start'], state="*")
async def start_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text="ℹ️ Для отправки СМС - просто отправьте номера в чат!",
        reply_markup=await reply.main_menu(),
    )