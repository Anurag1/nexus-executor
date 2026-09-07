from dataclasses import dataclass, field
from itertools import combinations
import re

STOP = set("the a an and or to of in for with on is are was were this that how what why if we our your their it be as from into by about could would should".split())

@dataclass
class Chat:
    id: str
    text: str
    tags: set[str] = field(default_factory=set)

@dataclass
class Relation:
    a: str
    b: str
    score: float
    shared: list[str]
    kind: str

class UnifiedDiscoveryEngine:
    """Deterministic baseline for discovering relationships between conversations.

    Lexical overlap is only a prioritization signal; it is not proof of semantic
    complementarity. This makes the MVP reproducible and easy to benchmark.
    """
    def _tokens(self, text: str) -> set[str]:
        words = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", text.lower())
        return {w for w in words if w not in STOP}

    def relate(self, chats: list[Chat]) -> list[Relation]:
        tokens = {c.id: self._tokens(c.text) for c in chats}
        out = []
        for x, y in combinations(chats, 2):
            shared = sorted(tokens[x.id] & tokens[y.id])
            union = tokens[x.id] | tokens[y.id]
            score = len(shared) / len(union) if union else 0.0
            kind = "complementary" if 0.08 <= score < 0.30 else ("overlapping" if score >= 0.30 else "weak")
            out.append(Relation(x.id, y.id, round(score, 3), shared, kind))
        return sorted(out, key=lambda r: r.score, reverse=True)

    def graph(self, chats: list[Chat]) -> dict:
        relations = self.relate(chats)
        nodes = {c.id: {"tokens": sorted(self._tokens(c.text)), "degree": 0} for c in chats}
        for r in relations:
            if r.score >= 0.08:
                nodes[r.a]["degree"] += 1
                nodes[r.b]["degree"] += 1
        return {"nodes": nodes, "relations": [r.__dict__ for r in relations if r.score >= 0.08]}

    def hypotheses(self, chats: list[Chat]) -> list[dict]:
        ranked = [r for r in self.relate(chats) if r.kind == "complementary"][:10]
        return [{"pair": [r.a, r.b],
                 "hypothesis": f"Conversation {r.a} may supply context that makes {r.b} more actionable.",
                 "signal": r.score, "shared_terms": r.shared} for r in ranked]

    def contradictions(self, chats: list[Chat]) -> list[dict]:
        positive = {"works", "beneficial", "possible", "increase", "improve", "useful", "yes", "strong"}
        negative = {"fails", "harmful", "impossible", "decrease", "worse", "useless", "no", "weak"}
        result = []
        for c in chats:
            tokens = self._tokens(c.text)
            p, n = len(tokens & positive), len(tokens & negative)
            if p and n:
                result.append({"chat": c.id, "positive_signals": p, "negative_signals": n})
        return result
