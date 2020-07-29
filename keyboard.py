from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import bank_handler


def get_main_keyboard(language):
    if language == "ru":
        text_button_1 = "Настройки"
        text_button_2 = "Обновить"
    else:
        text_button_1 = "Settings"
        text_button_2 = "Refresh"
    inline_button_1 = InlineKeyboardButton(text_button_1, callback_data="settings")
    inline_button_2 = InlineKeyboardButton(text_button_2, callback_data="update")
    inline_kb1 = InlineKeyboardMarkup().add(inline_button_2)
    inline_kb1.add(inline_button_1)
    return inline_kb1


def get_setting_keyboard(language):
    if language == "ru":
        text_button_1 = "       Город       "
        text_button_2 = "       Валюта       "
        text_button_3 = "   Назад  "
    else:
        text_button_1 = "       City       "
        text_button_2 = "       Currency       "
        text_button_3 = "   Back  "
    inline_button_2 = InlineKeyboardButton(text_button_1, callback_data="cities")
    inline_button_3 = InlineKeyboardButton(text_button_2, callback_data="currency")
    inline_button_4 = InlineKeyboardButton(text_button_3, callback_data="back")
    inline_kb2 = InlineKeyboardMarkup(row_width=2)
    inline_kb2.add(inline_button_2, inline_button_3)
    inline_kb2.row(inline_button_4)
    return inline_kb2


def get_first_letter_of_city_keyboard():
    inline_kb3 = InlineKeyboardMarkup(row_width=5)
    first_letters = set()
    bank = bank_handler.ExchangeRate()
    cities = bank.get_cities()
    for city in cities:
        first_letters.add(city[0])
    first_letters = sorted(list(first_letters))
    for letter in first_letters:
        new_button = InlineKeyboardButton(f"  {letter}  ", callback_data=letter)
        inline_kb3.insert(new_button)
    inline_kb3.add(InlineKeyboardButton("  Назад  ", callback_data="settings"))
    return inline_kb3


def get_cities_list(first_letter):
    inline_kb4 = InlineKeyboardMarkup(row_width=3)
    bank = bank_handler.ExchangeRate()
    cities = sorted(bank.get_cities())
    for city in cities:
        if city.startswith(first_letter):
            correct_city = InlineKeyboardButton(f"{city}", callback_data=f"change_city_{city}")
            inline_kb4.insert(correct_city)
    inline_kb4.add(InlineKeyboardButton("  Назад  ", callback_data="cities"))
    return inline_kb4


def get_currency_list():
    inline_kb5 = InlineKeyboardMarkup(row_width=4)
    bank = bank_handler.ExchangeRate()
    currencies = bank.get_currencies()
    for currency in currencies:
        currency = InlineKeyboardButton(f"{currency}", callback_data=f"change_currency_{currency}")
        inline_kb5.insert(currency)
    inline_kb5.add(InlineKeyboardButton("  Назад  ", callback_data="settings"))
    return inline_kb5
