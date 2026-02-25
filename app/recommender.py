import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any


DATA_PATH = Path(__file__).parent / "data" / "yojnas.json"


@dataclass
class UserProfile:
    name: str | None
    age: int
    gender: str           # "male" | "female" | "other"
    income: int           # INR per year
    state: str | None     # e.g., "KA", "MH", "DELHI"
    occupation: str | None

    def normalized(self) -> "UserProfile":
        return UserProfile(
            name=(self.name or "").strip() or None,
            age=int(self.age or 0),
            gender=(self.gender or "").strip().lower(),
            income=int(self.income or 0),
            state=(self.state or "ALL").strip().upper(),
            occupation=(self.occupation or "").strip().lower(),
        )


def load_yojnas() -> List[Dict[str, Any]]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _score_match(user: UserProfile, y: Dict[str, Any]) -> int:
    """
    Return a relevance score. Any hard fail returns -1.
    Scoring is transparent and easy to tweak.
    """
    score = 0

    # age
    age_ok = y["ageRange"][0] <= user.age <= y["ageRange"][1]
    if not age_ok:
        return -1
    score += 3

    # gender
    gender_ok = y["gender"] == "any" or y["gender"] == user.gender
    if not gender_ok:
        return -1
    score += 2

    # income (0 means no upper limit)
    income_ok = y["incomeLimit"] == 0 or user.income <= y["incomeLimit"]
    if not income_ok:
        return -1
    score += 2

    # state
    user_state = user.state or "ALL"
    states = [s.upper() for s in y.get("states", ["ALL"])]
    if "ALL" in states or user_state in states:
        score += 1

    # tags vs occupation
    occ_tokens = set((user.occupation or "").split())
    tags = set([t.lower() for t in y.get("tags", [])])
    if occ_tokens and (occ_tokens & tags):
        score += 1

    return score


def recommend_yojnas(user: UserProfile, yojnas: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
    """
    Pure function: (user, data) -> ranked list of yojnas
    """
    u = user.normalized()
    scored = []

    for y in yojnas:
        s = _score_match(u, y)
        if s >= 0:
            scored.append((s, y))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [y for s, y in scored[:top_n]]


def asdict_user(user: UserProfile) -> Dict[str, Any]:
    return asdict(user.normalized())