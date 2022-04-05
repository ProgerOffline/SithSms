# -*- coding: utf-8 -*-

from aiogram.utils.callback_data import CallbackData


mailing_system = CallbackData("mailing_system", "type")
accounts_menu = CallbackData("account_menu", "button", "id")
edit_account = CallbackData("edit_account", "action", "id")

templates_menu = CallbackData("templates_menu", "button", "id")
edit_template = CallbackData("edit_template", "action", "id")