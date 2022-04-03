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


async def settings_menu():
    return types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=1
    ).row(
        types.KeyboardButton(
            text="🗺 SMS77",
        ),

        types.KeyboardButton(
            text="☀️SMS-FLY",
        ),

        types.KeyboardButton(
            text="📱Senysms",
        ),
    ).row(
        types.KeyboardButton(
            text="📞 Viber",
        ),

        types.KeyboardButton(
            text="🆑 SMSClub",
        ),

        types.KeyboardButton(
            text="📲SMS-Smart",
        ),
    ).row(
        types.KeyboardButton(
            text="㊗️ Twilio",
        ),

        types.KeyboardButton(
            text="🌐 BSG World",
        ),
    )