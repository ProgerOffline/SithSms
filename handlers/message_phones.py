# -*- coding: utf-8 -*-

import random

from aiogram import types
from loader import dp
from aiogram.dispatcher import FSMContext
from statesgroup import CreateSmsSending
from keyboards import inline


@dp.message_handler(state="*")
async def get_phones_from_message(message: types.Message, state: FSMContext):
    await state.finish()
    
    file_name = random.randint(10_000_000, 90_000_000)
    with open(f"documents/documents/{file_name}.txt", "w") as file:
        file.write(message.text)
    
    await CreateSmsSending.choose_mailing_system.set()
    async with state.proxy() as data:
        data['file_path'] = f"documents/{file_name}.txt"

    await message.answer(
        text="Данные успешно загружены, выберите " +\
            "систему через которую нужно делать рассылку",
        reply_markup=await inline.settings_menu(),
    )