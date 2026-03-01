from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class UserState:
    language: str  # "am", "om", "en"


# In-memory state (Phase 1 only). We'll replace this with DB in Phase 3.
USER_STATE: Dict[int, UserState] = {}


def get_language(telegram_user_id: int) -> Optional[str]:
    state = USER_STATE.get(telegram_user_id)
    return state.language if state else None


def set_language(telegram_user_id: int, language: str) -> None:
    USER_STATE[telegram_user_id] = UserState(language=language)