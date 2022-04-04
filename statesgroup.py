# -*- coding: utf-8 -*-

from aiogram.dispatcher.filters.state import State, StatesGroup


class SettingsMenu(StatesGroup):
    choose_mailing_system = State()