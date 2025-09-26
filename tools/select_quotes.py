#!/usr/bin/env python3
import argparse
import json
import os
from typing import List, Dict, Any

try:
    from sentence_transformers import SentenceTransformer, util  # type: ignore
    _HAS_ST = True
except Exception:
    _HAS_ST = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
    from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
    _HAS_SK = True
except Exception:
    _HAS_SK = False


def load_quotes(paths: List[str]) -> List[Dict[str, Any]]:
    quotes: List[Dict[str, Any]] = []
    for path in paths:
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                quotes.extend(data)
    return quotes


def filter_by_tags(quotes: List[Dict[str, Any]], tags: List[str], match_all: bool) -> List[Dict[str, Any]]:
    if not tags:
        return quotes
    tags_lower = [t.lower() for t in tags]
    filtered = []
    for q in quotes:
        qt = [t.lower() for t in q.get("tags", [])]
        if match_all:
            if all(t in qt for t in tags_lower):
                filtered.append(q)
        else:
            if any(t in qt for t in tags_lower):
                filtered.append(q)
    return filtered


def search_semantic(quotes: List[Dict[str, Any]], query: str, top_k: int) -> List[Dict[str, Any]]:
    corpus = [q.get("text", "") for q in quotes]
    if not corpus:
        return []

    if _HAS_ST:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        q_emb = model.encode([query], convert_to_tensor=True)
        c_emb = model.encode(corpus, convert_to_tensor=True)
        scores = util.cos_sim(q_emb, c_emb).cpu().numpy()[0]
    elif _HAS_SK:
        vec = TfidfVectorizer(stop_words="english")
        X = vec.fit_transform(corpus + [query])
        cX, qX = X[:-1], X[-1]
        scores = cosine_similarity(qX, cX)[0]
    else:
        # Basic keyword overlap fallback
        q_tokens = set(query.lower().split())
        scores = []
        for text in corpus:
            toks = set(text.lower().split())
            overlap = len(q_tokens & toks)
            scores.append(float(overlap))

    ranked = sorted(zip(scores, quotes), key=lambda x: x[0], reverse=True)
    return [q for _, q in ranked[:top_k]]


def main() -> None:
    parser = argparse.ArgumentParser(description="Select quotes by tags or semantic similarity.")
    parser.add_argument("--files", nargs="*", default=[
        os.path.join(os.path.dirname(__file__), "..", "data", "quotes.json"),
        os.path.join(os.path.dirname(__file__), "..", "data", "stoic_quotes.json"),
    ], help="JSON files to load quotes from")
    parser.add_argument("--tags", nargs="*", default=[], help="Tags to filter by")
    parser.add_argument("--match-all", action="store_true", help="Require all tags to match (default: any)")
    parser.add_argument("--query", type=str, default="", help="Semantic search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of quotes to return")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of pretty text")

    args = parser.parse_args()

    files = [os.path.abspath(p) for p in args.files]
    quotes = load_quotes(files)

    if args.tags:
        quotes = filter_by_tags(quotes, args.tags, args.match_all)

    if args.query:
        quotes = search_semantic(quotes, args.query, args.top_k)
    else:
        quotes = quotes[: args.top_k]

    if args.json:
        print(json.dumps(quotes, ensure_ascii=False, indent=2))
    else:
        for i, q in enumerate(quotes, 1):
            author = q.get("author", "Unknown")
            tags = ", ".join(q.get("tags", []))
            print(f"{i}. {q.get('text', '').strip()}\n   — {author}{' | ' + tags if tags else ''}\n")


if __name__ == "__main__":
    main()


