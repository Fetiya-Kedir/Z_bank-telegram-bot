from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.i18n import t
from bot.keyboards.inline import language_keyboard, main_menu_keyboard
from bot.state import get_language


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user or not update.message:
        return

    lang = get_language(user.id)

    if not lang:
        name = (user.first_name or "there").strip()
        await update.message.reply_text(
            t("en", "WELCOME_NAME").format(name=name),
            reply_markup=language_keyboard()
        )
        return

    await update.message.reply_text(t(lang, "MAIN_MENU"), reply_markup=main_menu_keyboard(lang))