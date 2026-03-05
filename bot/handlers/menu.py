from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from bot.i18n import t
from bot.keyboards.inline import nav_keyboard
from bot.state import get_language

from bot.handlers.faq import show_faq_categories
from bot.handlers.branch import show_branch_menu


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

    # ✅ Route FAQ to real FAQ flow
    if choice == "faq":
        await show_faq_categories(update, lang)
        return

    # ✅ Route Branch Finder to real Branch menu
    if choice == "branch":
        await show_branch_menu(update, lang)
        return

    # Placeholder pages (still future phases)
    page_title = {
        "support": "Contact Support",
        "about": "About the Bank",
    }.get(choice, choice)

    await query.edit_message_text(
        text=f"{page_title}\n\n(Feature coming in next phase.)",
        reply_markup=nav_keyboard(lang, include_back=True, include_lang=True),
    )