from __future__ import annotations

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes

from bot.keyboards.inline import main_menu_keyboard
from bot.state import get_language
from bot.handlers.branch import branch_location_router


async def location_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Entry point for all location messages.
    If the user is in 'branch_nearme' flow, branch_location_router will handle it.
    Otherwise, we just remove the reply keyboard (if any) and show main menu.
    """
    handled = await branch_location_router(update, context)
    if handled:
        return

    user = update.effective_user
    lang = get_language(user.id) if user else "en"

    # Not in branch flow: clean up and show menu
    await update.message.reply_text(
        "Location received.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await update.message.reply_text(
        "Please use the menu below.",
        reply_markup=main_menu_keyboard(lang),
    )