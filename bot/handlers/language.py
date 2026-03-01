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

    await query.answer()  # acknowledge callback

    user = update.effective_user
    if not user:
        return

    data = query.data or ""

    # Expected: lang:am
    parts = data.split(":", maxsplit=1)
    if len(parts) != 2:
        await query.edit_message_text(
            text=t("en", "UNKNOWN")
        )
        return

    lang = parts[1].strip()

    if lang not in SUPPORTED:
        await query.edit_message_text(
            text=t("en", "UNKNOWN")
        )
        return

    # Save language preference
    set_language(user.id, lang)

    # Edit current message into Main Menu (clean UI)
    await query.edit_message_text(
        text=f"{t(lang, 'LANG_SAVED')}\n\n{t(lang, 'MAIN_MENU')}",
        reply_markup=main_menu_keyboard(lang),
    )