# -*- coding: utf-8 -*-

import os

from aiogram import types
from loader import dp
from keyboards import ctypes, inline
from aiogram.dispatcher import FSMContext
from statesgroup import CreateSmsSending
from database import sms_account_api, tempalte_api
from utils.smssender import SmsSender
from datetime import datetime
from loader import logger


@dp.callback_query_handler(
    ctypes.mailing_system.filter(),
    state=CreateSmsSending.choose_mailing_system
)
async def choose_mailing_system_for_sending(
    call: types.CallbackQuery,
    state: FSMContext,
    callback_data: dict,
):
    async with state.proxy() as data:
        data['mailing_system'] = callback_data['type']
    
    account_records = await sms_account_api.get_all(
        owner_tg_id=call.message.chat.id,
        mailing_system=callback_data['type'],
    )

    await CreateSmsSending.choose_account.set()
    await call.answer()
    await call.message.edit_text(
        text="Выберите аккаунт для шлюза {name}".format(
                name=callback_data['type']
            ),
        reply_markup=await inline.select_account_menu(account_records),
    )


@dp.callback_query_handler(
    ctypes.select_account_menu.filter(action="back"),
    state=CreateSmsSending.choose_account,
)
async def back_to_choose_mailing_system_menu(call: types.CallbackQuery):
    await CreateSmsSending.choose_mailing_system.set()
    await call.answer()
    await call.message.edit_text(
        text="Данные успешно загружены, выберите " +\
            "систему через которую нужно делать рассылку",
        reply_markup=await inline.settings_menu(),
    )


@dp.callback_query_handler(
    ctypes.select_account_menu.filter(action="select"),
    state=CreateSmsSending.choose_account,
)
async def choose_account(
    call: types.CallbackQuery,
    callback_data: dict,
    state: FSMContext,
):  
    account = await sms_account_api.get_one(int(callback_data['id']))
    async with state.proxy() as data:
        data['account_name'] = account.name
        data['access_key'] = account.access_key
        mailing_system = data['mailing_system']
    
    if mailing_system != "sms-fly":
        service = SmsSender(
            access_key=account.access_key,
            account_name=account.name,
            mailing_system=mailing_system,
        )

        await CreateSmsSending.choose_alpha_name.set()
        await call.answer()
        await call.message.edit_text(
            text="Выберите альфа имя",
            reply_markup=await inline.select_alpha_name(service.get_alpha_names())
        )
    else:    
        templates_records = await tempalte_api.get_all(
            owner_tg_id=call.message.chat.id,
        )
        await CreateSmsSending.choose_template.set()
        await call.answer()
        await call.message.edit_text(
            text="Выберите шаблон, или используйте ввод.",
            reply_markup=await inline.select_template_menu(templates_records)
        )


@dp.callback_query_handler(
    ctypes.alpha_names.filter(),
    state=CreateSmsSending.choose_alpha_name,
)
async def choose_alpha_name(
        call: types.CallbackQuery,
        state: FSMContext,
        callback_data: dict
    ):
    async with state.proxy() as data:
        data['alpha_name'] = callback_data['name']

    templates_records = await tempalte_api.get_all(
        owner_tg_id=call.message.chat.id,
    )
    await CreateSmsSending.choose_template.set()
    await call.answer()
    await call.message.edit_text(
        text="Выберите шаблон, или используйте ввод.",
        reply_markup=await inline.select_template_menu(templates_records)
    )


@dp.callback_query_handler(
    ctypes.select_template_menu.filter(action="back"),
    state=CreateSmsSending.choose_template,
)
async def back_to_choose_account_menu(
    call: types.CallbackQuery,
    state: FSMContext,
):
    await CreateSmsSending.choose_account.set()
    async with state.proxy() as data:
        mailing_system = data['mailing_system']

    account_records = await sms_account_api.get_all(
        owner_tg_id=call.message.chat.id,
        mailing_system=mailing_system,
    )

    await CreateSmsSending.choose_account.set()
    await call.answer()
    await call.message.edit_text(
        text="Выберите аккаунт для шлюза {name}".format(
                name=mailing_system,
            ),
        reply_markup=await inline.select_account_menu(account_records),
    )


@dp.callback_query_handler(
    ctypes.select_template_menu.filter(action="template"),
    state=CreateSmsSending.choose_template,
)
async def select_template_menu(
    call: types.CallbackQuery,
    callback_data: dict,
    state: FSMContext,
):
    template = await tempalte_api.get_one(int(callback_data['id']))
    async with state.proxy() as data:
        account_name = data['account_name']
        access_key = data['access_key']
        file_path = data['file_path']
        mailing_system = data['mailing_system']
        alpha_name = data['alpha_name']

    if mailing_system == "sms-fly": alpha_name = "none" 

    # Запуск скрипта рассылки
    template_content = template.content.replace("'", '\'')
    template_content = template.content.replace('"', '\"')

    logger.debug(f"SEND SMS {mailing_system}, {access_key}, {template_content}, {file_path}")
    if mailing_system == "sms-sms":
        # В шлюзе sms-sms.com.ua, для авторизации используется номер телефона и 
        # Пароль от аккаунта
        os.system(f"nohup /home/sithsms/venv/bin/python3 /home/sithsms/sms_sender.py {mailing_system} {access_key} \"{template_content}\" {file_path} {account_name} \"{alpha_name}\" &")

    else:
        os.system(f"nohup /home/sithsms/venv/bin/python3 /home/sithsms/sms_sender.py {mailing_system} {access_key} \"{template_content}\" {file_path} None \"{alpha_name}\" &")


    sender = SmsSender(phones_file_path=file_path)
    count_valid_phones = len(sender.phones_list)

    current_data = datetime.now()
    current_data = current_data.strftime("%m/%d/%Y %H:%M:%S")

    await call.answer()
    await state.finish()
    await call.message.answer(
        text="ℹ️ <b>Массовая рассылка SMS:</b>\n\n" +\
            f"👤 <b>Кол-во номеров:</b> {count_valid_phones}\n" +\
            f"📅 <b>Дата:</b> {current_data}\n" +\
            f"🖥 <b>Система отправки:</b> {mailing_system}\n" +\
            f"🔑 <b>Данные системы:</b> {account_name}\n" +\
            f"📑 <b>Сообщение:</b> {template_content}\n" +\
            "✅ <b>Рассылка успешно запущена!</b>",
    )


@dp.message_handler(state=CreateSmsSending.choose_template)
async def get_fast_template(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        template_content = message.text
        access_key = data['access_key']
        file_path = data['file_path']
        mailing_system = data['mailing_system']
        account_name = data['account_name']
        alpha_name = data['alpha_name']
    
    # Запуск скрипта рассылки
    template_content = template_content.replace("'", '\'')
    template_content = template_content.replace('"', '\"')

    if mailing_system == "sms-fly": alpha_name = "none" 

    logger.debug(f"SEND SMS {mailing_system}, {access_key}, {template_content}, {file_path}, {alpha_name}")
    
    if mailing_system == "sms-sms":
        # В шлюзе sms-sms.com.ua, для авторизации используется номер телефона и 
        # Пароль от аккаунта
        os.system(f"nohup /home/sithsms/venv/bin/python3 sms_sender.py {mailing_system} {access_key} \"{template_content}\" {file_path} {account_name} \"{alpha_name}\" &")

    else:
        os.system(f"nohup /home/sithsms/venv/bin/python3 sms_sender.py {mailing_system} {access_key} \"{template_content}\" {file_path} None \"{alpha_name}\" &")


    sender = SmsSender(phones_file_path=file_path)
    count_valid_phones = len(sender.phones_list)

    current_data = datetime.now()
    current_data = current_data.strftime("%m/%d/%Y %H:%M:%S")

    await state.finish()
    await message.answer(
        text="ℹ️ <b>Массовая рассылка SMS:</b>\n\n" +\
            f"👤 <b>Кол-во номеров:</b> {count_valid_phones}\n" +\
            f"📅 <b>Дата:</b> {current_data}\n" +\
            f"🖥 <b>Система отправки:</b> {mailing_system}\n" +\
            f"🔑 <b>Данные системы:</b> {account_name}\n" +\
            f"📑 <b>Сообщение:</b> {template_content}\n" +\
            "✅ <b>Рассылка успешно запущена!</b>",
    )