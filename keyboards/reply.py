# -*- coding: utf-8 -*-

from aiogram import types


async def main_menu():
    return types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1,
    ).add(
        types.KeyboardButton(
            text="⚙️ Настройки",
        ),
        types.KeyboardButton(
            text="🔨 Настройка шаблонов",
        ),
    )
