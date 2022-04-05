# -*- coding: utf-8 -*-

from aiogram import types
from loader import dp
from keyboards import inline
from statesgroup import SettingsMenu
from database import tempalte_api
from aiogram.dispatcher import FSMContext


@dp.message_handler(text="⚙️ Настройки", state="*")
async def show_settings(message: types.Message):
    await SettingsMenu.choose_mailing_system.set()
    await message.answer(
        text="❔ Выберите систему где вы хотите редактировать аккаунты:",
        reply_markup=await inline.settings_menu(),
    )


@dp.message_handler(text="🔨 Настройка шаблонов", state="*")
async def show_templates(message: types.Message, state: FSMContext):
    await state.finish()
    templates_records = await tempalte_api.get_all(message.from_user.id)

    await message.answer(
        text="Выберите шаблон",
        reply_markup=await inline.templates_menu(templates_records)
    )