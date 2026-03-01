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
    """
    2 columns x 2 rows main menu for a cleaner UI.
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(t(lang, "BTN_FAQ"), callback_data="menu:faq"),
                InlineKeyboardButton(t(lang, "BTN_BRANCH"), callback_data="menu:branch"),
            ],
            [
                InlineKeyboardButton(t(lang, "BTN_SUPPORT"), callback_data="menu:support"),
                InlineKeyboardButton(t(lang, "BTN_ABOUT"), callback_data="menu:about"),
            ],
        ]
    )


def nav_keyboard(lang: str, include_back: bool = True, include_lang: bool = True) -> InlineKeyboardMarkup:
    """
    Global navigation buttons used across all submenus:
    - Back to Main Menu
    - Change Language
    """
    rows = []

    nav_row = []
    if include_back:
        nav_row.append(InlineKeyboardButton(t(lang, "BTN_BACK_MAIN"), callback_data="nav:main"))
    if include_lang:
        nav_row.append(InlineKeyboardButton(t(lang, "BTN_CHANGE_LANG"), callback_data="nav:lang"))

    if nav_row:
        rows.append(nav_row)

    return InlineKeyboardMarkup(rows)