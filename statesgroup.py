# -*- coding: utf-8 -*-

from aiogram.dispatcher.filters.state import State, StatesGroup


class SettingsMenu(StatesGroup):
    choose_mailing_system = State()
    edit_accounts = State()
    edit_proxies = State()
    get_proxies = State()


class CreateAccount(StatesGroup):
    get_name = State()
    get_access_key = State()


class EditAccount(StatesGroup):
    edit_name = State()
    edit_access_key = State()


class CreateTemplate(StatesGroup):
    get_name = State()
    get_content = State()


class EditTemplate(StatesGroup):
    edit_name = State()
    edit_content = State()


class CreateSmsSending(StatesGroup):
    choose_mailing_system = State()
    choose_account = State()
    choose_alpha_name = State()
    choose_template = State()