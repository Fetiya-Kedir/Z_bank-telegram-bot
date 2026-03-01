from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.i18n import t
from bot.keyboards.inline import language_keyboard, main_menu_keyboard
from bot.state import get_language


async def nav_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()

    user = update.effective_user
    lang = get_language(user.id) if user else "en"

    data = query.data or ""
    # Expected: nav:main or nav:lang
    parts = data.split(":", maxsplit=1)
    if len(parts) != 2:
        await query.edit_message_text(t(lang, "UNKNOWN"))
        return

    action = parts[1].strip()

    if action == "main":
        await query.edit_message_text(
            text=t(lang, "MAIN_MENU"),
            reply_markup=main_menu_keyboard(lang),
        )
        return

    if action == "lang":
        # Edit message to language selection to keep chat clean
        name = (user.first_name if user and user.first_name else "there").strip()
        await query.edit_message_text(
            text=t("en", "WELCOME_NAME").format(name=name),
            reply_markup=language_keyboard(),
        )
        return

    await query.edit_message_text(t(lang, "UNKNOWN"))