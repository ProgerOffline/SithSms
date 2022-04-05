# -*- coding: utf-8 -*-

from aiogram.dispatcher.filters.state import State, StatesGroup


class SettingsMenu(StatesGroup):
    choose_mailing_system = State()
    edit_accounts = State()


class CreateAccount(StatesGroup):
    get_name = State()
    get_access_key = State()


class EditAccount(StatesGroup):
    edit_name = State()
    edit_access_key = State()