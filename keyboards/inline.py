# -*- coding: utf-8 -*-

from aiogram import types
from . import ctypes


async def settings_menu():
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            text="🗺 SMS77",
            callback_data=ctypes.mailing_system.new(type="sms77"),
        ),

        types.InlineKeyboardButton(
            text="☀️SMS-FLY",
            callback_data=ctypes.mailing_system.new(type="sms-fly"),
        ),

        types.InlineKeyboardButton(
            text="📱Senysms",
            callback_data=ctypes.mailing_system.new(type="senysms"),
        ),
    ).row(
        types.InlineKeyboardButton(
            text="📞 Viber",
            callback_data=ctypes.mailing_system.new(type="viber"),
        ),

        types.InlineKeyboardButton(
            text="🆑 SMSClub",
            callback_data=ctypes.mailing_system.new(type="smsclub"),
        ),

        types.InlineKeyboardButton(
            text="📲SMS-Smart",
            callback_data=ctypes.mailing_system.new(type="sms-smart"),
        ),
    ).row(
        types.InlineKeyboardButton(
            text="㊗️ Twilio",
            callback_data=ctypes.mailing_system.new(type="twilio"),
        ),

        types.InlineKeyboardButton(
            text="🌐 BSG World",
            callback_data=ctypes.mailing_system.new(type="bsg-world"),
        ),
    )


async def accounts_menu(account_records):
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            text="🆕 Добавить аккаунт",
            callback_data=ctypes.accounts_menu.new(button="create_accont")
        )
    )

    for record in account_records:
        keyboard.add(
            types.InlineKeyboardButton(
                text=record.name,
                callback_data=ctypes.accounts_menu.new(button=f"account#{record.id}")
            )
        )
    
    return keyboard