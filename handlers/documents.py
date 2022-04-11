# -*- coding: utf-8 -*-

from aiogram import types
from aiogram.dispatcher import FSMContext
from statesgroup import CreateSmsSending
from loader import dp, bot
from keyboards import inline


@dp.message_handler(content_types=['document'], state="*")
async def get_phones_list(message: types.Message, state: FSMContext):
    file_data = await bot.get_file(message.document.file_id)
    document_dir = file_data.file_path.split("/")[0]
    await message.document.download(
        destination_dir=document_dir,
    )

    await CreateSmsSending.choose_mailing_system.set()
    async with state.proxy() as data:
        data['file_path'] = file_data.file_path

    await message.answer(
        text="Данные успешно загружены, выберите " +\
            "систему через которую нужно делать рассылку",
        reply_markup=await inline.settings_menu(),
    )