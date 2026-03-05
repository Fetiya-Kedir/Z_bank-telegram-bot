from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.i18n import t


MAX_BUTTON_TEXT = 60  # prevent long question overflow


def _truncate(text: str) -> str:
    text = text.strip()
    if len(text) <= MAX_BUTTON_TEXT:
        return text
    return text[:MAX_BUTTON_TEXT - 1].rstrip() + "…"


from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def faq_categories_keyboard(lang: str, categories: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(title, callback_data=f"faq:cat:{cid}")
        for cid, title in categories
    ]

    rows = [buttons[i:i+2] for i in range(0, len(buttons), 2)]

    return InlineKeyboardMarkup(rows)

def faq_questions_keyboard(
    lang: str,
    category_id: str,
    questions: list[tuple[str, str]],
) -> InlineKeyboardMarkup:
    
    rows = [
        [
            InlineKeyboardButton(
                _truncate(q),
                callback_data=f"faq:q:{category_id}:{iid}",
            )
        ]
        for iid, q in questions
    ]

    # Back to categories
    rows.append(
        [
            InlineKeyboardButton(
                t(lang, "BTN_BACK"),
                callback_data="faq:back:cats",
            )
        ]
    )

    return InlineKeyboardMarkup(rows)


def faq_answer_keyboard(lang: str, category_id: str) -> InlineKeyboardMarkup:
    
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    t(lang, "BTN_BACK"),
                    callback_data=f"faq:back:cat:{category_id}",
                )
            ]
        ]
    )