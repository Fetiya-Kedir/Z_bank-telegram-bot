from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.i18n import t
from bot.keyboards.inline import main_menu_keyboard
from bot.state import get_language
from bot.handlers.branch import branch_text_router, branch_location_router


async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # First: allow branch flows to consume the message if needed
    handled_location = await branch_location_router(update, context)
    if handled_location:
        return

    handled_text = await branch_text_router(update, context)
    if handled_text:
        return

    # Default fallback
    if not update.message:
        return

    user = update.effective_user
    lang = get_language(user.id) if user else "en"

    await update.message.reply_text(
        t(lang, "UNKNOWN"),
        reply_markup=main_menu_keyboard(lang),
    )

async def unknown_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()

    user = update.effective_user
    lang = get_language(user.id) if user else "en"

    # Edit message to a safe menu state
    await query.edit_message_text(
        t(lang, "UNKNOWN"),
        reply_markup=main_menu_keyboard(lang),
    )