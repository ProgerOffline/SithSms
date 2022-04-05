# -*- coding: utf-8 -*-

from aiogram import types
from loader import dp
from keyboards import ctypes, inline
from aiogram.dispatcher import FSMContext
from database import sms_account_api, tempalte_api
from statesgroup import (SettingsMenu, CreateAccount, 
            EditAccount, CreateTemplate, EditTemplate)


@dp.callback_query_handler(
    ctypes.mailing_system.filter(),
    state=SettingsMenu.choose_mailing_system,
)
@dp.callback_query_handler(
    ctypes.mailing_system.filter(),
    state=SettingsMenu.edit_accounts,
)
async def get_mailing_system(
    call: types.CallbackQuery, 
    callback_data: dict,
    state: FSMContext,
):
    async with state.proxy() as data:
        data['mailing_system'] = callback_data['type']

    account_records = await sms_account_api.get_all(
        owner_tg_id=call.message.chat.id,
        mailing_system=callback_data['type']
    )

    await call.answer()
    await SettingsMenu.edit_accounts.set()
    await call.message.edit_text(
        text="Выберите аккаунт",
        reply_markup=await inline.accounts_menu(account_records)
    )


@dp.callback_query_handler(
    ctypes.accounts_menu.filter(button="back"),
    state=SettingsMenu.edit_accounts,
)
async def back_mailing_system_menu(call: types.CallbackQuery):
    await SettingsMenu.choose_mailing_system.set()
    await call.answer()
    await call.message.edit_text(
        text="❔ Выберите систему где вы хотите редактировать аккаунты:",
        reply_markup=await inline.settings_menu(),
    )


@dp.callback_query_handler(
    ctypes.accounts_menu.filter(button="create_accont"),
    state=SettingsMenu.edit_accounts,
)
async def create_account(call: types.CallbackQuery):
    await CreateAccount.get_name.set()
    await call.answer()
    await call.message.delete()
    await call.message.answer(
        text="Введите название аккаунта"
    )


@dp.callback_query_handler(
    ctypes.accounts_menu.filter(button="account"),
    state=SettingsMenu.edit_accounts,
)
async def show_account_info(call: types.CallbackQuery, callback_data: dict):
    account = await sms_account_api.get_one(int(callback_data['id']))

    await call.answer()
    await call.message.edit_text(
        text=f"<b>Название аккаунта: </b> {account.name}\n" +\
            f"<b>Ключ доступа: </b> {account.access_key}\n",
        reply_markup=await inline.edit_account_menu(
            account.id,
            account.mailing_system,
        )
    )


@dp.callback_query_handler(
    ctypes.edit_account.filter(action="edit_name"),
    state=SettingsMenu.edit_accounts,
)
async def edit_account_name(
    call: types.CallbackQuery, 
    callback_data: dict,
    state: FSMContext,
):
    async with state.proxy() as data:
        data['account_id'] = callback_data['id']

    call.answer()
    await EditAccount.edit_name.set()
    await call.message.edit_text(
        text="Введите название аккаунта",
    )


@dp.callback_query_handler(
    ctypes.edit_account.filter(action="edit_access_key"),
    state=SettingsMenu.edit_accounts,
)
async def edit_account_name(
    call: types.CallbackQuery, 
    callback_data: dict,
    state: FSMContext,
):
    async with state.proxy() as data:
        data['account_id'] = callback_data['id']

    await call.answer()
    await EditAccount.edit_access_key.set()
    await call.message.edit_text(
        text="Введите ключ доступа от аккаунта",
    )


@dp.callback_query_handler(
    ctypes.edit_account.filter(action="request_delete_account"),
    state=SettingsMenu.edit_accounts,
)
async def edit_account_name(
    call: types.CallbackQuery, 
    callback_data: dict,
    state: FSMContext,
):
    async with state.proxy() as data:
        data['account_id'] = callback_data['id']
    
    await call.answer()
    await call.message.edit_text(
        text="Вы точно хотите удалить аккаунт?",
        reply_markup=await inline.delete_account_menu(int(callback_data['id']))
    )


@dp.callback_query_handler(
    ctypes.edit_account.filter(action="confirm_delete"),
    state=SettingsMenu.edit_accounts,
) 
async def confirm_delete_account(call: types.CallbackQuery, callback_data: dict):
    account = await sms_account_api.get_one(int(callback_data['id']))
    mailing_system = account.mailing_system
    await sms_account_api.delete(int(callback_data['id']))

    await SettingsMenu.edit_accounts.set()
    account_records = await sms_account_api.get_all(
        owner_tg_id=call.message.chat.id,
        mailing_system=mailing_system,
    )

    await call.answer()
    await SettingsMenu.edit_accounts.set()
    await call.message.edit_text(
        text="Выберите аккаунт",
        reply_markup=await inline.accounts_menu(account_records)
    )


@dp.callback_query_handler(ctypes.templates_menu.filter(button="create_template"))
async def create_message_template(call: types.CallbackQuery):
    await CreateTemplate.get_name.set()
    await call.message.delete()
    await call.answer()
    await call.message.answer(
        text="Введите название шаблона",
    )


@dp.callback_query_handler(ctypes.templates_menu.filter(button="template"))
async def show_templates(call: types.CallbackQuery, callback_data: dict):
    template_record = await tempalte_api.get_one(int(callback_data['id']))
    
    await call.answer()
    await call.message.edit_text(
        text=f"<b>Название шаблона: </b>{template_record.name}\n" +\
            f"<b>Текст шаблона: </b>{template_record.content}\n",
        reply_markup=await inline.edit_template_menu(template_record.id),
    )


@dp.callback_query_handler(ctypes.edit_template.filter(action="back"))
async def back_to_list_templates(call: types.Message):
    templates_records = await tempalte_api.get_all(call.message.chat.id)

    await call.message.edit_text(
        text="Выберите шаблон",
        reply_markup=await inline.templates_menu(templates_records)
    )


@dp.callback_query_handler(ctypes.edit_template.filter(action="edit_name"))
async def edit_template_name(
    call: types.Message, 
    callback_data: dict,
    state: FSMContext
):
    await EditTemplate.edit_name.set()
    async with state.proxy() as data:
        data['template_id'] = int(callback_data['id'])

    await call.answer()
    await call.message.delete()
    await call.message.answer(
        text="Введите название шаблона",
    )


@dp.callback_query_handler(ctypes.edit_template.filter(action="edit_content"))
async def edit_template_content(
    call: types.Message,
    callback_data: dict,
    state: FSMContext,
):
    await EditTemplate.edit_content.set()
    async with state.proxy() as data:
        data['template_id'] = int(callback_data['id'])
    
    await call.answer()
    await call.message.edit_text(
        text="Введите текст шаблона",
    )


@dp.callback_query_handler(ctypes.edit_template.filter(action="request_delete_tempalte"))
async def edit_account_name(
    call: types.CallbackQuery,
    callback_data: dict,
):  
    await call.answer()
    await call.message.edit_text(
        text="Вы точно хотите удалить шаблон?",
        reply_markup=await inline.delete_template_menu(int(callback_data['id']))
    )


@dp.callback_query_handler(ctypes.edit_template.filter(action="confirm_delete"))
async def confirm_delete_tempalte(call: types.CallbackQuery, callback_data: dict):
    await tempalte_api.delete(int(callback_data['id']))
    
    templates_records = await tempalte_api.get_all(call.message.chat.id)
    await call.answer()
    await call.message.edit_text(
            text="Выберите шаблон",
            reply_markup=await inline.templates_menu(templates_records)
        )
