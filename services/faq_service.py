from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass(frozen=True)
class FaqItem:
    id: str
    q: Dict[str, str]  # lang -> question
    a: Dict[str, str]  # lang -> answer


@dataclass(frozen=True)
class FaqCategory:
    id: str
    title: Dict[str, str]  # lang -> title
    items: List[FaqItem]


class FaqRepository:
    """
    JSON-backed FAQ repository (Phase 2).
    Later we will swap implementation to DB without changing handler logic.
    """

    def __init__(self, json_path: str = "data/faq.json") -> None:
        self.json_path = Path(json_path)
        self._categories: List[FaqCategory] = []
        self._loaded: bool = False

    def load(self) -> None:
        if self._loaded:
            return

        raw = json.loads(self.json_path.read_text(encoding="utf-8"))
        categories_raw = raw.get("categories", [])
        if not isinstance(categories_raw, list):
            raise ValueError("faq.json: 'categories' must be a list")

        cats: List[FaqCategory] = []
        for c in categories_raw:
            cid = str(c.get("id", "")).strip()
            title = c.get("title", {})
            items_raw = c.get("items", [])

            if not cid:
                raise ValueError("faq.json: category missing 'id'")
            if not isinstance(title, dict):
                raise ValueError(f"faq.json: category '{cid}' title must be an object")
            if not isinstance(items_raw, list):
                raise ValueError(f"faq.json: category '{cid}' items must be a list")

            items: List[FaqItem] = []
            for it in items_raw:
                iid = str(it.get("id", "")).strip()
                q = it.get("q", {})
                a = it.get("a", {})

                if not iid:
                    raise ValueError(f"faq.json: category '{cid}' has item missing 'id'")
                if not isinstance(q, dict) or not isinstance(a, dict):
                    raise ValueError(f"faq.json: item '{cid}/{iid}' q/a must be objects")

                items.append(FaqItem(id=iid, q=q, a=a))

            cats.append(FaqCategory(id=cid, title=title, items=items))

        self._categories = cats
        self._loaded = True

    def list_categories(self) -> List[FaqCategory]:
        self.load()
        return self._categories

    def get_category(self, category_id: str) -> Optional[FaqCategory]:
        self.load()
        for c in self._categories:
            if c.id == category_id:
                return c
        return None

    def get_item(self, category_id: str, item_id: str) -> Optional[FaqItem]:
        cat = self.get_category(category_id)
        if not cat:
            return None
        for it in cat.items:
            if it.id == item_id:
                return it
        return None


def pick_lang_text(d: Dict[str, str], lang: str) -> str:
    """
    Return localized text with fallback.
    """
    if lang in d and d[lang].strip():
        return d[lang].strip()
    if "en" in d and d["en"].strip():
        return d["en"].strip()
    # last resort: first available
    for v in d.values():
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""