from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.i18n import t
from bot.keyboards.inline import language_keyboard
from bot.state import get_language


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Allow user to change language at any time.
    We send a language selection keyboard.
    """
    if not update.message:
        return

    user = update.effective_user
    lang = get_language(user.id) if user else "en"

    name = (user.first_name if user and user.first_name else "there").strip()
    # Show language selection (new message is acceptable for commands)
    await update.message.reply_text(
        t("en", "WELCOME_NAME").format(name=name),
        reply_markup=language_keyboard(),
    )