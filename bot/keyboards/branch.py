from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from bot.i18n import t


def branch_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t(lang, "BTN_BRANCH_SEARCH"), callback_data="branch:search")],
            [InlineKeyboardButton(t(lang, "BTN_BRANCH_NEARME"), callback_data="branch:nearme")],
            
        ]
    )


def request_location_keyboard(lang: str) -> ReplyKeyboardMarkup:
    
    return ReplyKeyboardMarkup(
        [[KeyboardButton(t(lang, "BTN_SEND_LOCATION"), request_location=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )