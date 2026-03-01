from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.i18n import t
from bot.keyboards.inline import nav_keyboard
from bot.state import get_language


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()

    user = update.effective_user
    lang = get_language(user.id) if user else "en"

    data = query.data or ""
    parts = data.split(":", maxsplit=1)
    if len(parts) != 2:
        await query.edit_message_text(t(lang, "UNKNOWN"))
        return

    choice = parts[1].strip()

    # Phase 1 placeholder pages (later we replace with real FAQ/Branch)
    page_title = {
        "faq": "FAQ",
        "branch": "Branch Finder",
        "support": "Contact Support",
        "about": "About the Bank",
    }.get(choice, choice)

    await query.edit_message_text(
        text=f"{page_title}\n\n(Feature coming in next phase.)",
        reply_markup=nav_keyboard(lang, include_back=True, include_lang=True),
    )