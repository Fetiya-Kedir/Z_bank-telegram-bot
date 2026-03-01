from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.i18n import t
from bot.state import get_language


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()

    user = update.effective_user
    lang = get_language(user.id) if user else "en"

    data = query.data or ""
    # Expected: "menu:faq" etc.
    parts = data.split(":", maxsplit=1)
    if len(parts) != 2:
        await query.edit_message_text(t(lang, "UNKNOWN"))
        return

    choice = parts[1].strip()

    # Phase 1 placeholder
    await query.edit_message_text(f"{t(lang, 'MAIN_MENU')}\n\nSelected: {choice}\n(Feature coming in next phase.)")