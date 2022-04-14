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

        types.InlineKeyboardButton(
            text="📨 СМС-СМС",
            callback_data=ctypes.mailing_system.new(type="sms-sms"),
        ),
    )


async def accounts_menu(account_records):
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            text="🆕 Добавить аккаунт",
            callback_data=ctypes.accounts_menu.new(
                button="create_accont",
                id="",
            )
        )
    )

    for record in account_records:
        keyboard.add(
            types.InlineKeyboardButton(
                text=record.name,
                callback_data=ctypes.accounts_menu.new(
                    button="account",
                    id=record.id,
                )
            )
        )

    keyboard.add(
        types.InlineKeyboardButton(
            text="↩️ Назад",
            callback_data=ctypes.accounts_menu.new(
                button="back",
                id="",
            )
        )
    )
    
    return keyboard


async def select_account_menu(account_records):
    keyboard = types.InlineKeyboardMarkup()

    for record in account_records:
        keyboard.add(
            types.InlineKeyboardButton(
                text=record.name,
                callback_data=ctypes.select_account_menu.new(
                    action="select",
                    id=record.id,
                )
            )
        )

    keyboard.add(
        types.InlineKeyboardButton(
            text="↩️ Назад",
            callback_data=ctypes.select_account_menu.new(
                action="back",
                id="",
            )
        )
    )
    
    return keyboard


async def edit_account_menu(record_id, mailing_system):
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            text="Именить название",
            callback_data=ctypes.edit_account.new(
                action="edit_name",
                id=record_id,
            ),
        ),
        types.InlineKeyboardButton(
            text="Именить ключ доступа",
            callback_data=ctypes.edit_account.new(
                action="edit_access_key",
                id=record_id,
            ),
        ),
    ).add(
        types.InlineKeyboardButton(
            text="Удалить аккаунт",
            callback_data=ctypes.edit_account.new(
                action="request_delete_account",
                id=record_id,
            ),
        ),
    ).add(
        types.InlineKeyboardButton(
            text="Назад",
            callback_data=ctypes.mailing_system.new(
                type=mailing_system,
            ),
        ), 
    )


async def delete_account_menu(record_id):
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            text="Да",
            callback_data=ctypes.edit_account.new(
                action="confirm_delete",
                id=record_id,
            )
        ),
        types.InlineKeyboardButton(
            text="Нет",
            callback_data=ctypes.accounts_menu.new(
                button="account",
                id=record_id,
            )
        ),
    )


async def templates_menu(templates_records):
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(
            text="🆕 Добавить шаблон",
            callback_data=ctypes.templates_menu.new(
                button="create_template",
                id="",
            ),
        ),
    )

    for record in templates_records:
        keyboard.add(
            types.InlineKeyboardButton(
                text=record.name,
                callback_data=ctypes.templates_menu.new(
                    button="template",
                    id=record.id,
                ),
            ),
        )

    return keyboard


async def select_template_menu(templates_records):
    keyboard = types.InlineKeyboardMarkup()

    for record in templates_records:
        keyboard.add(
            types.InlineKeyboardButton(
                text=record.name,
                callback_data=ctypes.select_template_menu.new(
                    action="template",
                    id=record.id,
                ),
            ),
        )

    keyboard.add(
        types.InlineKeyboardButton(
            text="↩️ Назад",
            callback_data=ctypes.select_template_menu.new(
                action="back",
                id="",
            )
        )
    )

    return keyboard


async def edit_template_menu(record_id):
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            text="Именить название",
            callback_data=ctypes.edit_template.new(
                action="edit_name",
                id=record_id,
            ),
        ),
        types.InlineKeyboardButton(
            text="Именить текст",
            callback_data=ctypes.edit_template.new(
                action="edit_content",
                id=record_id,
            ),
        ),
    ).add(
        types.InlineKeyboardButton(
            text="Удалить шаблон",
            callback_data=ctypes.edit_template.new(
                action="request_delete_tempalte",
                id=record_id,
            ),
        ),
    ).add(
        types.InlineKeyboardButton(
            text="Назад",
            callback_data=ctypes.edit_template.new(
                action="back",
                id="",
            ),
        ), 
    )


async def delete_template_menu(record_id):
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton(
            text="Да",
            callback_data=ctypes.edit_template.new(
                action="confirm_delete",
                id=record_id,
            )
        ),
        types.InlineKeyboardButton(
            text="Нет",
            callback_data=ctypes.templates_menu.new(
                button="template",
                id=record_id,
            )
        ),
    )
