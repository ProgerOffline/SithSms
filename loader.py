# -*- coding: utf-8 -*-

from aiogram import types
from aiogram import Dispatcher, Bot

from data.config import BOT_TOKEN
from logzero import logger, logfile


logfile("bot_log.log")


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)
