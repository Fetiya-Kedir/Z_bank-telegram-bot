from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class UserState:
    language: str  # "am", "om", "en"
    pending_action: Optional[str] = None  # e.g., "branch_search"


USER_STATE: Dict[int, UserState] = {}


def get_language(telegram_user_id: int) -> Optional[str]:
    state = USER_STATE.get(telegram_user_id)
    return state.language if state else None


def set_language(telegram_user_id: int, language: str) -> None:
    st = USER_STATE.get(telegram_user_id)
    if st:
        st.language = language
    else:
        USER_STATE[telegram_user_id] = UserState(language=language)


def set_pending_action(telegram_user_id: int, action: Optional[str]) -> None:
    st = USER_STATE.get(telegram_user_id)
    if not st:
        # default to English if not set yet
        USER_STATE[telegram_user_id] = UserState(language="en", pending_action=action)
        return
    st.pending_action = action


def get_pending_action(telegram_user_id: int) -> Optional[str]:
    st = USER_STATE.get(telegram_user_id)
    return st.pending_action if st else None