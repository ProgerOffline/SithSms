# -*- coding: utf-8 -*-

from aiogram import types
from loader import dp
from aiogram.dispatcher import FSMContext
from database import sms_account_api, tempalte_api
from keyboards import inline
from statesgroup import (CreateAccount, EditAccount, 
        SettingsMenu, CreateTemplate, EditTemplate)


@dp.message_handler(state=CreateAccount.get_name)
async def get_account_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['account_name'] = message.text
    
    await CreateAccount.get_access_key.set()
    await message.answer(
        text="Введите ключ доступа от аккаунта",
    )


@dp.message_handler(state=CreateAccount.get_access_key)
async def get_account_access_key(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        mailing_system = data['mailing_system']
        account_name = data['account_name']
        account_access_key = message.text
    
    await sms_account_api.create(
        owner_tg_id=message.from_user.id,
        name=account_name,
        access_key=account_access_key,
        mailing_system=mailing_system,
    )

    account_records = await sms_account_api.get_all(
        owner_tg_id=message.from_user.id,
        mailing_system=mailing_system,
    )
    
    await SettingsMenu.edit_accounts.set()
    await message.answer(
        text="Выберите аккаунт",
        reply_markup=await inline.accounts_menu(account_records)
    )


@dp.message_handler(state=EditAccount.edit_name)
async def edit_account_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        account_id = int(data['account_id'])
    
    await sms_account_api.update_name(
        record_id=account_id,
        new_name=message.text,
    )

    account = await sms_account_api.get_one(account_id)

    await SettingsMenu.edit_accounts.set()
    await message.answer(
        text=f"<b>Название аккаунта: </b> {account.name}\n" +\
            f"<b>Ключ доступа: </b> {account.access_key}\n",
        reply_markup=await inline.edit_account_menu(
            account.id,
            account.mailing_system,
        )
    )


@dp.message_handler(state=EditAccount.edit_access_key)
async def edit_account_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        account_id = int(data['account_id'])
    
    await sms_account_api.update_access_key(
        record_id=account_id,
        new_access_key=message.text,
    )

    account = await sms_account_api.get_one(account_id)

    await SettingsMenu.edit_accounts.set()
    await message.answer(
        text=f"<b>Название аккаунта: </b> {account.name}\n" +\
            f"<b>Ключ доступа: </b> {account.access_key}\n",
        reply_markup=await inline.edit_account_menu(
            account.id,
            account.mailing_system,
        )
    )


@dp.message_handler(state=CreateTemplate.get_name)
async def get_template_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['template_name'] = message.text

    await CreateTemplate.get_content.set()
    await message.answer(
        text="Введите текст шалона",
    )


@dp.message_handler(state=CreateTemplate.get_content)
async def createa_tempalte(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        template_name = data['template_name']
        template_content = message.text

    await tempalte_api.create(
        owner_tg_id=message.from_user.id,
        name=template_name,
        content=template_content,
    )

    templates_records = await tempalte_api.get_all(message.from_user.id)
    await state.finish()
    await message.answer(
        text="Выберите шаблон",
        reply_markup=await inline.templates_menu(templates_records)
    )


@dp.message_handler(state=EditTemplate.edit_name)
async def get_new_teamplate_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        template_id = int(data['template_id'])
        template_name = message.text
    
    template_record = await tempalte_api.update_name(
        record_id=template_id,
        new_name=template_name
    )

    await state.finish()
    await message.answer(
        text=f"<b>Название шаблона: </b>{template_record.name}\n" +\
            f"<b>Текст шаблона: </b>{template_record.content}\n",
        reply_markup=await inline.edit_template_menu(template_record.id),
    )


@dp.message_handler(state=EditTemplate.edit_content)
async def get_new_template_content(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        template_id = int(data['template_id'])
        template_content = message.text
    
    template_record = await tempalte_api.update_content(
        record_id=template_id,
        new_content=template_content,
    )

    await state.finish()
    await message.answer(
        text=f"<b>Название шаблона: </b>{template_record.name}\n" +\
            f"<b>Текст шаблона: </b>{template_record.content}\n",
        reply_markup=await inline.edit_template_menu(template_record.id),
    )