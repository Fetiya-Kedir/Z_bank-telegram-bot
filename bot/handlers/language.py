from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot.i18n import t
from bot.keyboards.inline import main_menu_keyboard
from bot.state import set_language

logger = logging.getLogger(__name__)

SUPPORTED = {"en", "am", "om"}


async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()  # Acknowledge the callback to Telegram

    user = update.effective_user
    if not user:
        return

    data = query.data or ""
    # Expected format: "lang:am"
    parts = data.split(":", maxsplit=1)
    if len(parts) != 2:
        await query.edit_message_text(t("en", "UNKNOWN"))
        return

    lang = parts[1].strip()
    if lang not in SUPPORTED:
        await query.edit_message_text(t("en", "UNKNOWN"))
        return

    set_language(user.id, lang)
    await query.edit_message_text(t(lang, "LANG_SAVED"))
    await query.message.reply_text(t(lang, "MAIN_MENU"), reply_markup=main_menu_keyboard(lang))