from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Branch:
    id: str
    name: str
    address: str
    plus_code: str
    city: str
    region: str
    latitude: float
    longitude: float


class BranchRepository:
    def __init__(self, json_path: str = "data/branches.json") -> None:
        self.json_path = Path(json_path)
        self._branches: List[Branch] = []
        self._loaded = False

    def load(self) -> None:
        if self._loaded:
            return

        raw = json.loads(self.json_path.read_text(encoding="utf-8"))
        branches_raw = raw.get("branches", [])
        if not isinstance(branches_raw, list):
            raise ValueError("branches.json: 'branches' must be a list")

        out: List[Branch] = []
        for b in branches_raw:
            out.append(
                Branch(
                    id=str(b.get("id", "")).strip(),
                    name=str(b.get("name", "")).strip(),
                    address=str(b.get("address", "")).strip(),
                    plus_code=str(b.get("plus_code", "")).strip(),
                    city=str(b.get("city", "")).strip(),
                    region=str(b.get("region", "")).strip(),
                    latitude=float(b.get("latitude")),
                    longitude=float(b.get("longitude")),
                )
            )

        self._branches = out
        self._loaded = True

    def all(self) -> List[Branch]:
        self.load()
        return self._branches


def normalize(text: str) -> str:
    return " ".join(text.lower().strip().split())

def score_match(query: str, branch: Branch) -> int:
    
    q = normalize(query)
    if not q:
        return 0

    name = normalize(branch.name)
    city = normalize(branch.city)
    region = normalize(branch.region)
    addr = normalize(branch.address)
    plus = normalize(branch.plus_code)

    score = 0
    if q in name:
        score += 4
    if q in city or q in region:
        score += 3
    if q in addr or q in plus:
        score += 2
    return score
def search_branches(branches: List[Branch], query: str, limit: int = 5) -> List[Branch]:
    q = normalize(query)
    scored: List[Tuple[int, Branch]] = []
    for b in branches:
        s = score_match(q, b)
        if s > 0:
            scored.append((s, b))

    scored.sort(key=lambda x: (-x[0], x[1].name))
    return [b for _, b in scored[:limit]]


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def nearest_branches(branches: List[Branch], lat: float, lon: float, limit: int = 5) -> List[Tuple[Branch, float]]:
    scored: List[Tuple[Branch, float]] = []
    for b in branches:
        d = haversine_km(lat, lon, b.latitude, b.longitude)
        scored.append((b, d))
    scored.sort(key=lambda x: x[1])
    return scored[:limit]


def maps_link(lat: float, lon: float, label: Optional[str] = None) -> str:
    # Google Maps query link (works widely)
    if label:
        return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}({label})"
    return f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"


def format_branch(branch: Branch) -> str:
    parts = [f"🏦 {branch.name}"]
    if branch.address:
        parts.append(f"📍 {branch.address}")
    if branch.plus_code:
        parts.append(f"🧭 {branch.plus_code}")
    if branch.city or branch.region:
        parts.append(f"🗺️ {branch.city} {('- ' + branch.region) if branch.region and branch.region != branch.city else ''}".strip())
    parts.append(f"🗺️ Map: {maps_link(branch.latitude, branch.longitude)}")
    return "\n".join(parts)