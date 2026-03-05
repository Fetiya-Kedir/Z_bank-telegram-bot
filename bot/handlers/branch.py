from __future__ import annotations

import logging

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes

from bot.i18n import t
from bot.keyboards.branch import branch_menu_keyboard, request_location_keyboard
from bot.keyboards.inline import main_menu_keyboard, nav_keyboard
from bot.state import get_language, get_pending_action, set_pending_action
from services.branch_service import BranchRepository, format_branch, nearest_branches, search_branches

logger = logging.getLogger(__name__)
repo = BranchRepository("data/branches.json")


async def show_branch_menu(update: Update, lang: str) -> None:
    text = f"{t(lang, 'BRANCH_TITLE')}\n\n{t(lang, 'BRANCH_PROMPT')}"
    kb = branch_menu_keyboard(lang)

    merged_rows = kb.inline_keyboard + nav_keyboard(lang, include_back=True, include_lang=True).inline_keyboard
    markup = type(kb)(merged_rows)

    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=markup)
    elif update.message:
        await update.message.reply_text(text=text, reply_markup=markup)


async def branch_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()
    user = update.effective_user
    lang = get_language(user.id) if user else "en"

    data = query.data or ""
    parts = data.split(":", maxsplit=1)
    if len(parts) != 2:
        await query.edit_message_text(t(lang, "UNKNOWN"), reply_markup=main_menu_keyboard(lang))
        return

    action = parts[1].strip()

    if action == "search":
        # Set state so the next user text will be treated as a branch query
        if user:
            set_pending_action(user.id, "branch_search")

        await query.edit_message_text(
            text=f"{t(lang, 'BRANCH_SEARCH_TITLE')}\n\n{t(lang, 'BRANCH_SEARCH_INSTR')}",
            reply_markup=nav_keyboard(lang, include_back=True, include_lang=True),
        )
        return

    if action == "nearme":
        # Ask user to send location (reply keyboard)
        if user:
            set_pending_action(user.id, "branch_nearme")

        await query.edit_message_text(
            text=f"{t(lang, 'BRANCH_NEARME_TITLE')}\n\n{t(lang, 'BRANCH_NEARME_INSTR')}",
            reply_markup=nav_keyboard(lang, include_back=True, include_lang=True),
        )

        # Send a separate message with the location request button (best UX)
        # This is a controlled additional message (one-time) and worth it.
        if query.message:
            await query.message.reply_text(
                t(lang, "BRANCH_SEND_LOCATION_PROMPT"),
                reply_markup=request_location_keyboard(lang),
            )
        return

    await query.edit_message_text(t(lang, "UNKNOWN"), reply_markup=main_menu_keyboard(lang))


async def branch_text_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Returns True if this message was handled as part of branch flow.
    Otherwise returns False so other handlers can respond.
    """
    if not update.message:
        return False

    user = update.effective_user
    if not user:
        return False

    lang = get_language(user.id) or "en"
    pending = get_pending_action(user.id)

    if pending != "branch_search":
        return False

    query_text = (update.message.text or "").strip()
    set_pending_action(user.id, None)

    branches = repo.all()
    results = search_branches(branches, query_text, limit=5)

    if not results:
        await update.message.reply_text(
            t(lang, "BRANCH_NO_RESULTS"),
            reply_markup=main_menu_keyboard(lang),
        )
        return True

    msg = [t(lang, "BRANCH_RESULTS_TITLE")]
    for b in results:
        msg.append("")
        msg.append(format_branch(b))

    await update.message.reply_text("\n".join(msg), reply_markup=main_menu_keyboard(lang))
    return True


async def branch_location_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Handle location messages when user chose 'near me'.
    """
    if not update.message or not update.message.location:
        return False

    user = update.effective_user
    if not user:
        return False

    lang = get_language(user.id) or "en"
    pending = get_pending_action(user.id)

    if pending != "branch_nearme":
        return False

    set_pending_action(user.id, None)

    lat = update.message.location.latitude
    lon = update.message.location.longitude

    branches = repo.all()
    nearest = nearest_branches(branches, lat, lon, limit=5)

    msg = [t(lang, "BRANCH_NEAREST_TITLE")]
    for b, d in nearest:
        msg.append("")
        msg.append(f"{format_branch(b)}\n📏 {d:.2f} km")

    # Remove reply keyboard after location
    await update.message.reply_text(
        "\n".join(msg),
        reply_markup=ReplyKeyboardRemove(),
    )
    await update.message.reply_text(
        t(lang, "BRANCH_DONE"),
        reply_markup=main_menu_keyboard(lang),
    )
    return True