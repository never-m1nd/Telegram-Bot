import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import keyboard as kb
import bank_handler as bh
import datetime

logging.basicConfig(level=logging.DEBUG)
token = "1075506655:AAFsrraNqUXYyC8DFTrIn2Yy4Uh7bR1Uhho"

bot = Bot(token=token)
dp = Dispatcher(bot)

exchange_rate = bh.ExchangeRate()


def get_text():
    text = f"Самый популярный курс {exchange_rate.currency} в отделениях Беларусбанка " \
           f"в городе {exchange_rate.city} на {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}" \
           f"\n{exchange_rate.get_output(exchange_rate.get_exchange_rate())}"
    return text


@dp.message_handler(commands=["start"])
async def process_start(message: types.Message):
    await message.reply(get_text(), reply_markup=kb.get_main_keyboard())


@dp.callback_query_handler(lambda c: c.data == 'settings')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text('Настройки', chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=kb.get_setting_keyboard())


@dp.callback_query_handler(lambda c: c.data == 'cities')
async def process_callback_button2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    kb.get_first_letter_of_city_keyboard()
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=kb.get_first_letter_of_city_keyboard())


@dp.callback_query_handler(lambda c: 'change' in c.data)
async def process_callback_button2(callback_query: types.CallbackQuery):
    data = callback_query.data
    if "city" in data:
        exchange_rate.change_city(data[12:])
        text = "Город измненён."
    elif "currency" in data:
        exchange_rate.change_currency(data[16:])
        text = "Валюта изменена."
    await bot.answer_callback_query(callback_query.id, text=text)
    await bot.edit_message_text(text=get_text(), chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=kb.get_main_keyboard())


@dp.callback_query_handler(lambda c: c.data == 'currency')
async def process_callback_button3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_reply_markup(chat_id=callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=kb.get_currency_list())


@dp.callback_query_handler(lambda c: c.data == 'update')
async def process_callback_button3(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(get_text(), chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=kb.get_main_keyboard())


@dp.callback_query_handler(lambda c: c.data == 'back')
async def process_callback_button4(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(get_text(), chat_id=callback_query.from_user.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=kb.get_main_keyboard())


@dp.callback_query_handler(lambda c: len(c.data) == 1)
async def process_callback_button5(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    data = callback_query.data
    await bot.edit_message_reply_markup(callback_query.from_user.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=kb.get_cities_list(data))


if __name__ == '__main__':
    executor.start_polling(dp)
