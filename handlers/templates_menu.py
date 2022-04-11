# -*- coding: utf-8 -*-

from aiogram import types
from loader import dp
from database import tempalte_api
from keyboards import inline, ctypes
from aiogram.dispatcher import FSMContext
from statesgroup import CreateTemplate, EditTemplate


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

