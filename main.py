import logging
import os
import requests
from aiogram import Bot, Dispatcher
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.executor import start_webhook
from config import TOKEN_API
from markups.reply_mrkps import *
from markups.reply_mrkps import markup_language
from messages import *
from states import ProfileStatesGroup
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

storage = MemoryStorage()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

dp = Dispatcher(bot,
                storage=storage)

#Google sheets
spreadsheet_id = '1FTuj1tq0Gy7GP3bP78K6UGMLltRU8DO3YSB7hCehgm0'
RANGE_NAME_1 = 'Статистика нажатий'
credentials = Credentials.from_service_account_file('beelinc-19f9d07341fe.json')
service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)
#Google sheets
range_name = 'Статистика нажатий!A2'
range_name1 = 'Статистика нажатий!B2'
range_name2 = 'Статистика нажатий!C2'
range_name3 = 'Статистика нажатий!D2'
range_name4 = 'Статистика нажатий!E2'
range_name5 = 'Статистика нажатий!F2'
range_name6 = 'Статистика нажатий!G2'
range_name7 = 'Статистика нажатий!H2'
range_name8 = 'Статистика нажатий!I2'


async def select_number(rang):
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=rang
    ).execute()
    return result['values'][0][0]
async def update_number(item1, rang):
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=rang,
        valueInputOption='RAW',
        body={'values': [[item1]]}
    )
    request.execute()


@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text="Xizmat ko'rsatish tilini tanlang\n\nВыберите язык обслуживания",
                           reply_markup=markup_language)
    if state is None:
        return
    await state.finish()

@dp.message_handler(content_types=['text'])
async def lang_choose(message: types.Message, state: FSMContext) -> None:
    try:
        async with state.proxy() as data:
            data['lang'] = message.text
            markup_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(lang_dict['kard'][data['lang']])
            btn2 = types.KeyboardButton(lang_dict['paid'][data['lang']])
            btn3 = types.KeyboardButton(lang_dict['transactions'][data['lang']])
            btn4 = types.KeyboardButton(lang_dict['registration'][data['lang']])
            btn5 = types.KeyboardButton(lang_dict['monitoring_pays'][data['lang']])
            btn6 = types.KeyboardButton(lang_dict['beep'][data['lang']])
            btn7 = types.KeyboardButton(lang_dict['my_home'][data['lang']])
            btn8 = types.KeyboardButton(lang_dict['bonus'][data['lang']])
            btn9 = types.KeyboardButton(lang_dict['connect'][data['lang']])
            btn10 = types.KeyboardButton(lang_dict['back'][data['lang']])
            markup_buttons.row(btn1, btn2, btn3).row(btn4).row(btn5, btn6).row(btn7, btn8).row(btn9).row(btn10)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['cat'][data['lang']],
                                   reply_markup=markup_buttons)
            await ProfileStatesGroup.razdel.set()
    except KeyError:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Выберите вариант кнопкой!")
"""      
button_text = 'Хотите связаться с оператором?'
button_options = ['Связаться']
message_btn = {
    'text': button_text,
    'buttons': button_options
}
"""
@dp.message_handler(content_types=types.ContentType.TEXT, state=ProfileStatesGroup.razdel)
async def menu(message: types.Message, state: FSMContext) -> None:
    try:
        async with state.proxy() as data:
            if message.text == lang_dict['kard'][data['lang']]:
                num = await select_number(range_name)
                markup_card = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn1 = types.KeyboardButton(lang_dict['how_add'][data['lang']])
                btn2 = types.KeyboardButton(lang_dict['foreighn_kard'][data['lang']])
                btn3 = types.KeyboardButton(lang_dict['cant_add'][data['lang']])
                btn4 = types.KeyboardButton(lang_dict['main_card'][data['lang']])
                btn5 = types.KeyboardButton(lang_dict['back'][data['lang']])
                markup_card.row(btn1).row(btn2).row(btn3).row(btn4).row(btn5)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['chapter'][data['lang']],
                                       reply_markup=markup_card)
                updated_num = int(num) + 1
                await update_number(updated_num, range_name)
                await ProfileStatesGroup.kard.set()




            if message.text == lang_dict['paid'][data['lang']]:
                num = await select_number(range_name1)
                markup_paid = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn1 = types.KeyboardButton(lang_dict['what_paid'][data['lang']])
                btn2 = types.KeyboardButton(lang_dict['monitoring'][data['lang']])
                btn3 = types.KeyboardButton(lang_dict['choosen_paid'][data['lang']])
                btn4 = types.KeyboardButton(lang_dict['autopay'][data['lang']])
                btn5 = types.KeyboardButton(lang_dict['autopay_reject'][data['lang']])
                btn6 = types.KeyboardButton(lang_dict['pay_reject'][data['lang']])
                btn7 = types.KeyboardButton(lang_dict['back'][data['lang']])
                markup_paid.row(btn1).row(btn2).row(btn3).row(btn4).row(btn5).row(btn6).row(btn7)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['chapter'][data['lang']],
                                       reply_markup=markup_paid)
                updated_num = int(num) + 1
                await update_number(updated_num, range_name1)
                await ProfileStatesGroup.paid.set()

            if message.text == lang_dict['transactions'][data['lang']]:
                num = await select_number(range_name2)
                markup_transactions = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn1 = types.KeyboardButton(lang_dict['transact_to_card'][data['lang']])
                btn2 = types.KeyboardButton(lang_dict['number_transaction'][data['lang']])
                btn3 = types.KeyboardButton(lang_dict['request'][data['lang']])
                btn4 = types.KeyboardButton(lang_dict['transact_reject'][data['lang']])
                btn5 = types.KeyboardButton(lang_dict['back'][data['lang']])
                markup_transactions.row(btn1).row(btn2).row(btn3).row(btn4).row(btn5)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['chapter'][data['lang']],
                                       reply_markup=markup_transactions)
                updated_num = int(num) + 1
                await update_number(updated_num, range_name2)
                await ProfileStatesGroup.transactions.set()

            if message.text == lang_dict['registration'][data['lang']]:
                num = await select_number(range_name3)
                markup_reg = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn1 = types.KeyboardButton(lang_dict['kod_password'][data['lang']])
                btn2 = types.KeyboardButton(lang_dict['forgot_password'][data['lang']])
                btn3 = types.KeyboardButton(lang_dict['invasion'][data['lang']])
                btn4 = types.KeyboardButton(lang_dict['how_delete'][data['lang']])
                btn5 = types.KeyboardButton(lang_dict['conf_kod'][data['lang']])
                btn6 = types.KeyboardButton(lang_dict['not_come'][data['lang']])
                btn7 = types.KeyboardButton(lang_dict['cant_enter'][data['lang']])
                btn8 = types.KeyboardButton(lang_dict['back'][data['lang']])
                markup_reg.row(btn1).row(btn2).row(btn3).row(btn4).row(btn5).row(btn6).row(btn7).row(btn8)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['chapter'][data['lang']],
                                       reply_markup=markup_reg)
                updated_num = int(num) + 1
                await update_number(updated_num, range_name3)
                await ProfileStatesGroup.registration.set()

            if message.text == lang_dict['monitoring_pays'][data['lang']]:
                num = await select_number(range_name4)
                markup_mon = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn1 = types.KeyboardButton(lang_dict['pays_story'][data['lang']])
                btn2 = types.KeyboardButton(lang_dict['monitoring_cost'][data['lang']])
                btn3 = types.KeyboardButton(lang_dict['check'][data['lang']])
                btn4 = types.KeyboardButton(lang_dict['back'][data['lang']])
                markup_mon.row(btn1).row(btn2).row(btn3).row(btn4)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['chapter'][data['lang']],
                                       reply_markup=markup_mon)
                updated_num = int(num) + 1
                await update_number(updated_num, range_name4)
                await ProfileStatesGroup.monitoring_pays.set()

            if message.text == lang_dict['beep'][data['lang']]:
                num = await select_number(range_name5)
                markup_beep = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn1 = types.KeyboardButton(lang_dict['what_is_beep'][data['lang']])
                btn2 = types.KeyboardButton(lang_dict['exchange'][data['lang']])
                btn3 = types.KeyboardButton(lang_dict['cant_exchange'][data['lang']])
                btn4 = types.KeyboardButton(lang_dict['back'][data['lang']])
                markup_beep.row(btn1).row(btn2).row(btn3).row(btn4)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['chapter'][data['lang']],
                                       reply_markup=markup_beep)
                updated_num = int(num) + 1
                await update_number(updated_num, range_name5)
                await ProfileStatesGroup.beep.set()

            if message.text == lang_dict['my_home'][data['lang']]:
                num = await select_number(range_name6)
                markup_home = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn1 = types.KeyboardButton(lang_dict['what_is_my_home'][data['lang']])
                btn2 = types.KeyboardButton(lang_dict['back'][data['lang']])
                markup_home.row(btn1).row(btn2)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['chapter'][data['lang']],
                                       reply_markup=markup_home)
                updated_num = int(num) + 1
                await update_number(updated_num, range_name6)
                await ProfileStatesGroup.my_home.set()

            if message.text == lang_dict['bonus'][data['lang']]:
                num = await select_number(range_name7)
                markup_bonus = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn1 = types.KeyboardButton(lang_dict['welcome_bonus'][data['lang']])
                btn2 = types.KeyboardButton(lang_dict['bonus_4g'][data['lang']])
                btn3 = types.KeyboardButton(lang_dict['bonus_50'][data['lang']])
                btn4 = types.KeyboardButton(lang_dict['back'][data['lang']])
                markup_bonus.row(btn1).row(btn2).row(btn3).row(btn4)
                await bot.send_message(chat_id=message.from_user.id,
                                       text=lang_dict['chapter'][data['lang']],
                                       reply_markup=markup_bonus)
                updated_num = int(num) + 1
                await update_number(updated_num, range_name7)
                await ProfileStatesGroup.bonus.set()

            """  if message.text == lang_dict['connect'][data['lang']]:
                button_text = 'Хотите связаться с оператором?'
                button_options = ['Связаться']
                message_btn = {
                    'text': button_text,
                    'buttons': button_options
                }
                LIVETEX_TOKEN = '6:0b3f3c77-de6c-4338-b860-8846bee8329d'
                response = requests.post(f'https://bot-api.livetex.ru/bot/v1/{LIVETEX_TOKEN}/message_btn', json=message_btn)

                # Проверьте статус ответа
                if response.status_code == 200:
                    print('Сообщение с кнопками успешно отправлено')
                else:
                    print('Ошибка при отправке сообщения с кнопками')"""
            if message.text == lang_dict['back'][data['lang']]:
                await state.finish()
                await bot.send_message(chat_id=message.from_user.id,
                                       text="Xizmat ko'rsatish tilini tanlang\n\nВыберите язык обслуживания",
                                       reply_markup=markup_language)
    except KeyError:
        await bot.send_message(chat_id=message.from_user.id,
                           text="Выберите вариант кнопкой!")



@dp.message_handler(content_types=types.ContentType.TEXT, state=ProfileStatesGroup.kard)
async def number_send(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text == lang_dict['how_add'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['how_add_text'][data['lang']])
        if message.text == lang_dict['foreighn_kard'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['foreighn_kard_text'][data['lang']])
        if message.text == lang_dict['cant_add'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['cant_add_text'][data['lang']])
        if message.text == lang_dict['main_card'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['main_card_text'][data['lang']])
        if message.text == lang_dict['back'][data['lang']]:
            markup_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(lang_dict['kard'][data['lang']])
            btn2 = types.KeyboardButton(lang_dict['paid'][data['lang']])
            btn3 = types.KeyboardButton(lang_dict['transactions'][data['lang']])
            btn4 = types.KeyboardButton(lang_dict['registration'][data['lang']])
            btn5 = types.KeyboardButton(lang_dict['monitoring_pays'][data['lang']])
            btn6 = types.KeyboardButton(lang_dict['beep'][data['lang']])
            btn7 = types.KeyboardButton(lang_dict['my_home'][data['lang']])
            btn8 = types.KeyboardButton(lang_dict['bonus'][data['lang']])
            btn9 = types.KeyboardButton(lang_dict['connect'][data['lang']])
            btn10 = types.KeyboardButton(lang_dict['back'][data['lang']])
            markup_buttons.row(btn1, btn2, btn3).row(btn4).row(btn5, btn6).row(btn7, btn8).row(btn9).row(btn10)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['cat'][data['lang']],
                                   reply_markup=markup_buttons)
            await ProfileStatesGroup.razdel.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=ProfileStatesGroup.paid)
async def number_send(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text == lang_dict['what_paid'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['what_paid_text'][data['lang']])
        if message.text == lang_dict['monitoring'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['monitoring_text'][data['lang']])
        if message.text == lang_dict['choosen_paid'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['choosen_paid_text'][data['lang']])
        if message.text == lang_dict['autopay'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['autopay_text'][data['lang']])
        if message.text == lang_dict['autopay_reject'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['autopay_reject_text'][data['lang']])
        if message.text == lang_dict['pay_reject'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['pay_reject_text'][data['lang']])
        if message.text == lang_dict['back'][data['lang']]:
            markup_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(lang_dict['kard'][data['lang']])
            btn2 = types.KeyboardButton(lang_dict['paid'][data['lang']])
            btn3 = types.KeyboardButton(lang_dict['transactions'][data['lang']])
            btn4 = types.KeyboardButton(lang_dict['registration'][data['lang']])
            btn5 = types.KeyboardButton(lang_dict['monitoring_pays'][data['lang']])
            btn6 = types.KeyboardButton(lang_dict['beep'][data['lang']])
            btn7 = types.KeyboardButton(lang_dict['my_home'][data['lang']])
            btn8 = types.KeyboardButton(lang_dict['bonus'][data['lang']])
            btn9 = types.KeyboardButton(lang_dict['connect'][data['lang']])
            btn10 = types.KeyboardButton(lang_dict['back'][data['lang']])
            markup_buttons.row(btn1, btn2, btn3).row(btn4).row(btn5, btn6).row(btn7, btn8).row(btn9).row(btn10)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['cat'][data['lang']],
                                   reply_markup=markup_buttons)
            await ProfileStatesGroup.razdel.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=ProfileStatesGroup.transactions)
async def number_send(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text == lang_dict['transact_to_card'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['transact_to_card_text'][data['lang']])
        if message.text == lang_dict['number_transaction'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['number_transaction_text'][data['lang']])
        if message.text == lang_dict['request'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['request_text'][data['lang']])
        if message.text == lang_dict['transact_reject'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['transact_reject_text'][data['lang']])
        if message.text == lang_dict['back'][data['lang']]:
            markup_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(lang_dict['kard'][data['lang']])
            btn2 = types.KeyboardButton(lang_dict['paid'][data['lang']])
            btn3 = types.KeyboardButton(lang_dict['transactions'][data['lang']])
            btn4 = types.KeyboardButton(lang_dict['registration'][data['lang']])
            btn5 = types.KeyboardButton(lang_dict['monitoring_pays'][data['lang']])
            btn6 = types.KeyboardButton(lang_dict['beep'][data['lang']])
            btn7 = types.KeyboardButton(lang_dict['my_home'][data['lang']])
            btn8 = types.KeyboardButton(lang_dict['bonus'][data['lang']])
            btn9 = types.KeyboardButton(lang_dict['connect'][data['lang']])
            btn10 = types.KeyboardButton(lang_dict['back'][data['lang']])
            markup_buttons.row(btn1, btn2, btn3).row(btn4).row(btn5, btn6).row(btn7, btn8).row(btn9).row(btn10)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['cat'][data['lang']],
                                   reply_markup=markup_buttons)
            await ProfileStatesGroup.razdel.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=ProfileStatesGroup.registration)
async def number_send(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text == lang_dict['kod_password'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['kod_password_text'][data['lang']])
        if message.text == lang_dict['forgot_password'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['forgot_password_text'][data['lang']])
        if message.text == lang_dict['invasion'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['invasion_text'][data['lang']])
        if message.text == lang_dict['how_delete'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['how_delete_text'][data['lang']])
        if message.text == lang_dict['conf_kod'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['conf_kod_text'][data['lang']])
        if message.text == lang_dict['not_come'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['not_come_text'][data['lang']])
        if message.text == lang_dict['cant_enter'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['cant_enter_text'][data['lang']])
        if message.text == lang_dict['back'][data['lang']]:
            markup_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(lang_dict['kard'][data['lang']])
            btn2 = types.KeyboardButton(lang_dict['paid'][data['lang']])
            btn3 = types.KeyboardButton(lang_dict['transactions'][data['lang']])
            btn4 = types.KeyboardButton(lang_dict['registration'][data['lang']])
            btn5 = types.KeyboardButton(lang_dict['monitoring_pays'][data['lang']])
            btn6 = types.KeyboardButton(lang_dict['beep'][data['lang']])
            btn7 = types.KeyboardButton(lang_dict['my_home'][data['lang']])
            btn8 = types.KeyboardButton(lang_dict['bonus'][data['lang']])
            btn9 = types.KeyboardButton(lang_dict['connect'][data['lang']])
            btn10 = types.KeyboardButton(lang_dict['back'][data['lang']])
            markup_buttons.row(btn1, btn2, btn3).row(btn4).row(btn5, btn6).row(btn7, btn8).row(btn9).row(btn10)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['cat'][data['lang']],
                                   reply_markup=markup_buttons)
            await ProfileStatesGroup.razdel.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=ProfileStatesGroup.monitoring_pays)
async def number_send(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text == lang_dict['pays_story'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['pays_story_text'][data['lang']])
        if message.text == lang_dict['monitoring_cost'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['monitoring_cost_text'][data['lang']])
        if message.text == lang_dict['check'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['check_text'][data['lang']])
        if message.text == lang_dict['back'][data['lang']]:
            markup_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(lang_dict['kard'][data['lang']])
            btn2 = types.KeyboardButton(lang_dict['paid'][data['lang']])
            btn3 = types.KeyboardButton(lang_dict['transactions'][data['lang']])
            btn4 = types.KeyboardButton(lang_dict['registration'][data['lang']])
            btn5 = types.KeyboardButton(lang_dict['monitoring_pays'][data['lang']])
            btn6 = types.KeyboardButton(lang_dict['beep'][data['lang']])
            btn7 = types.KeyboardButton(lang_dict['my_home'][data['lang']])
            btn8 = types.KeyboardButton(lang_dict['bonus'][data['lang']])
            btn9 = types.KeyboardButton(lang_dict['connect'][data['lang']])
            btn10 = types.KeyboardButton(lang_dict['back'][data['lang']])
            markup_buttons.row(btn1, btn2, btn3).row(btn4).row(btn5, btn6).row(btn7, btn8).row(btn9).row(btn10)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['cat'][data['lang']],
                                   reply_markup=markup_buttons)
            await ProfileStatesGroup.razdel.set()


@dp.message_handler(content_types=types.ContentType.TEXT, state=ProfileStatesGroup.beep)
async def number_send(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text == lang_dict['what_is_beep'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['what_is_beep_text'][data['lang']])
        if message.text == lang_dict['exchange'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['exchange_text'][data['lang']])
        if message.text == lang_dict['cant_exchange'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['cant_exchange_text'][data['lang']])
        if message.text == lang_dict['back'][data['lang']]:
            markup_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(lang_dict['kard'][data['lang']])
            btn2 = types.KeyboardButton(lang_dict['paid'][data['lang']])
            btn3 = types.KeyboardButton(lang_dict['transactions'][data['lang']])
            btn4 = types.KeyboardButton(lang_dict['registration'][data['lang']])
            btn5 = types.KeyboardButton(lang_dict['monitoring_pays'][data['lang']])
            btn6 = types.KeyboardButton(lang_dict['beep'][data['lang']])
            btn7 = types.KeyboardButton(lang_dict['my_home'][data['lang']])
            btn8 = types.KeyboardButton(lang_dict['bonus'][data['lang']])
            btn9 = types.KeyboardButton(lang_dict['connect'][data['lang']])
            btn10 = types.KeyboardButton(lang_dict['back'][data['lang']])
            markup_buttons.row(btn1, btn2, btn3).row(btn4).row(btn5, btn6).row(btn7, btn8).row(btn9).row(btn10)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['cat'][data['lang']],
                                   reply_markup=markup_buttons)
            await ProfileStatesGroup.razdel.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=ProfileStatesGroup.my_home)
async def number_send(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text == lang_dict['what_is_my_home'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['what_is_my_home_text'][data['lang']])
        if message.text == lang_dict['back'][data['lang']]:
            markup_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(lang_dict['kard'][data['lang']])
            btn2 = types.KeyboardButton(lang_dict['paid'][data['lang']])
            btn3 = types.KeyboardButton(lang_dict['transactions'][data['lang']])
            btn4 = types.KeyboardButton(lang_dict['registration'][data['lang']])
            btn5 = types.KeyboardButton(lang_dict['monitoring_pays'][data['lang']])
            btn6 = types.KeyboardButton(lang_dict['beep'][data['lang']])
            btn7 = types.KeyboardButton(lang_dict['my_home'][data['lang']])
            btn8 = types.KeyboardButton(lang_dict['bonus'][data['lang']])
            btn9 = types.KeyboardButton(lang_dict['connect'][data['lang']])
            btn10 = types.KeyboardButton(lang_dict['back'][data['lang']])
            markup_buttons.row(btn1, btn2, btn3).row(btn4).row(btn5, btn6).row(btn7, btn8).row(btn9).row(btn10)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['cat'][data['lang']],
                                   reply_markup=markup_buttons)
            await ProfileStatesGroup.razdel.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=ProfileStatesGroup.bonus)
async def number_send(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        if message.text == lang_dict['welcome_bonus'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['welcome_bonus_text'][data['lang']])
        if message.text == lang_dict['bonus_4g'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['bonus_4g_text'][data['lang']])
        if message.text == lang_dict['bonus_50'][data['lang']]:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['bonus_50_text'][data['lang']])
        if message.text == lang_dict['back'][data['lang']]:
            markup_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton(lang_dict['kard'][data['lang']])
            btn2 = types.KeyboardButton(lang_dict['paid'][data['lang']])
            btn3 = types.KeyboardButton(lang_dict['transactions'][data['lang']])
            btn4 = types.KeyboardButton(lang_dict['registration'][data['lang']])
            btn5 = types.KeyboardButton(lang_dict['monitoring_pays'][data['lang']])
            btn6 = types.KeyboardButton(lang_dict['beep'][data['lang']])
            btn7 = types.KeyboardButton(lang_dict['my_home'][data['lang']])
            btn8 = types.KeyboardButton(lang_dict['bonus'][data['lang']])
            btn9 = types.KeyboardButton(lang_dict['connect'][data['lang']])
            btn10 = types.KeyboardButton(lang_dict['back'][data['lang']])
            markup_buttons.row(btn1, btn2, btn3).row(btn4).row(btn5, btn6).row(btn7, btn8).row(btn9).row(btn10)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=lang_dict['cat'][data['lang']],
                                   reply_markup=markup_buttons)
            await ProfileStatesGroup.razdel.set()


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
async def on_shutdown(dispatcher):
    await bot.delete_webhook()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    
