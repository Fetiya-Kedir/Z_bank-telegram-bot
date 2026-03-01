from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.i18n import t


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🇪🇹 አማርኛ", callback_data="lang:am"),
                InlineKeyboardButton("🇪🇹 Afaan Oromo", callback_data="lang:om"),
            ],
            [InlineKeyboardButton("🌍 English", callback_data="lang:en")],
        ]
    )


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(t(lang, "BTN_FAQ"), callback_data="menu:faq")],
            [InlineKeyboardButton(t(lang, "BTN_BRANCH"), callback_data="menu:branch")],
            [InlineKeyboardButton(t(lang, "BTN_SUPPORT"), callback_data="menu:support")],
            [InlineKeyboardButton(t(lang, "BTN_ABOUT"), callback_data="menu:about")],
        ]
    )