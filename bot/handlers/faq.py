from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import ContextTypes

from bot.i18n import t
from bot.keyboards.faq import faq_answer_keyboard, faq_categories_keyboard, faq_questions_keyboard
from bot.keyboards.inline import main_menu_keyboard, nav_keyboard
from bot.state import get_language
from services.faq_service import FaqRepository, pick_lang_text

logger = logging.getLogger(__name__)

faq_repo = FaqRepository("data/faq.json")


async def show_faq_categories(update: Update, lang: str) -> None:
    categories = faq_repo.list_categories()
    options = [(c.id, pick_lang_text(c.title, lang)) for c in categories]

    text = f"{t(lang, 'FAQ_TITLE')}\n\n{t(lang, 'FAQ_CHOOSE_CATEGORY')}"
    kb = faq_categories_keyboard(lang, options)

    # Attach global nav under categories (Main + Language)
    # We combine by creating a new keyboard markup (Telegram doesn't support merging markups automatically)
    # So we will instead show nav as a separate row using the same message edit.
    merged_rows = kb.inline_keyboard + nav_keyboard(lang, include_back=False, include_lang=True).inline_keyboard
    markup = type(kb)(merged_rows)

    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=markup)
    elif update.message:
        await update.message.reply_text(text=text, reply_markup=markup)


async def faq_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()

    user = update.effective_user
    lang = get_language(user.id) if user else "en"

    data = query.data or ""

    # Patterns:
    # faq:cat:<category_id>
    # faq:q:<category_id>:<item_id>
    # faq:back:cats
    # faq:back:cat:<category_id>
    try:
        parts = data.split(":")
        if len(parts) < 3:
            await query.edit_message_text(t(lang, "UNKNOWN"), reply_markup=main_menu_keyboard(lang))
            return

        action = parts[1]

        if action == "cat" and len(parts) == 3:
            category_id = parts[2]
            cat = faq_repo.get_category(category_id)
            if not cat:
                await query.edit_message_text(t(lang, "UNKNOWN"), reply_markup=main_menu_keyboard(lang))
                return

            questions = [(it.id, pick_lang_text(it.q, lang)) for it in cat.items]
            text = f"{pick_lang_text(cat.title, lang)}\n\n{t(lang, 'FAQ_CHOOSE_QUESTION')}"

            kb = faq_questions_keyboard(lang, category_id, questions)
            # add global nav row
            merged_rows = kb.inline_keyboard + nav_keyboard(lang, include_back=True, include_lang=True).inline_keyboard
            markup = type(kb)(merged_rows)

            await query.edit_message_text(text=text, reply_markup=markup)
            return

        if action == "q" and len(parts) == 4:
            category_id = parts[2]
            item_id = parts[3]
            item = faq_repo.get_item(category_id, item_id)
            cat = faq_repo.get_category(category_id)
            if not item or not cat:
                await query.edit_message_text(t(lang, "UNKNOWN"), reply_markup=main_menu_keyboard(lang))
                return

            q_text = pick_lang_text(item.q, lang)
            a_text = pick_lang_text(item.a, lang)

            text = f"{pick_lang_text(cat.title, lang)}\n\n❓ {q_text}\n\n{t(lang, 'FAQ_ANSWER')}\n{a_text}"

            kb = faq_answer_keyboard(lang, category_id)
            merged_rows = kb.inline_keyboard + nav_keyboard(lang, include_back=True, include_lang=True).inline_keyboard
            markup = type(kb)(merged_rows)

            await query.edit_message_text(text=text, reply_markup=markup)
            return

        if action == "back" and len(parts) >= 3:
            dest = parts[2]
            if dest == "cats":
                await show_faq_categories(update, lang)
                return

            if dest == "cat" and len(parts) == 4:
                category_id = parts[3]
                cat = faq_repo.get_category(category_id)
                if not cat:
                    await show_faq_categories(update, lang)
                    return

                questions = [(it.id, pick_lang_text(it.q, lang)) for it in cat.items]
                text = f"{pick_lang_text(cat.title, lang)}\n\n{t(lang, 'FAQ_CHOOSE_QUESTION')}"

                kb = faq_questions_keyboard(lang, category_id, questions)
                merged_rows = kb.inline_keyboard + nav_keyboard(lang, include_back=True, include_lang=True).inline_keyboard
                markup = type(kb)(merged_rows)

                await query.edit_message_text(text=text, reply_markup=markup)
                return

        # Unknown FAQ action
        await query.edit_message_text(t(lang, "UNKNOWN"), reply_markup=main_menu_keyboard(lang))

    except Exception as e:
        logger.exception("FAQ callback error: %s", e)
        await query.edit_message_text(t(lang, "UNKNOWN"), reply_markup=main_menu_keyboard(lang))