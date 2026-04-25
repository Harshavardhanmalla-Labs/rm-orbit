import httpx

BASE_URL = "https://api.openalex.org"
PARAMS_BASE = {"mailto": "research@freedomlabs.in"}


async def search_works(query: str, limit: int = 10) -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"{BASE_URL}/works",
                params={**PARAMS_BASE, "search": query, "per-page": limit,
                        "select": "title,authorships,publication_year,primary_location,doi,abstract_inverted_index"},
            )
            if r.status_code != 200:
                return []
            results = []
            for w in r.json().get("results", []):
                authors = [
                    a.get("author", {}).get("display_name", "")
                    for a in w.get("authorships", [])[:3]
                ]
                venue = w.get("primary_location", {}) or {}
                source = venue.get("source") or {}
                abstract = _reconstruct_abstract(w.get("abstract_inverted_index"))
                results.append({
                    "title": w.get("title", ""),
                    "authors": [a for a in authors if a],
                    "year": str(w.get("publication_year", "")),
                    "venue": source.get("display_name", ""),
                    "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                    "abstract": abstract,
                    "verified": True,
                })
            return results
    except Exception:
        return []


def _reconstruct_abstract(inverted_index: dict | None) -> str:
    if not inverted_index:
        return ""
    words = {}
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words[i] for i in sorted(words))


async def get_related(doi: str, limit: int = 5) -> list[dict]:
    if not doi:
        return []
    clean_doi = doi.replace("https://doi.org/", "")
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"{BASE_URL}/works/https://doi.org/{clean_doi}",
                params={**PARAMS_BASE, "select": "related_works"},
            )
            if r.status_code != 200:
                return []
            related_ids = r.json().get("related_works", [])[:limit]
            if not related_ids:
                return []
            filter_str = "|".join(related_ids)
            r2 = await client.get(
                f"{BASE_URL}/works",
                params={**PARAMS_BASE, "filter": f"openalex:{filter_str}",
                        "select": "title,authorships,publication_year,doi"},
            )
            if r2.status_code != 200:
                return []
            results = []
            for w in r2.json().get("results", []):
                authors = [
                    a.get("author", {}).get("display_name", "")
                    for a in w.get("authorships", [])[:3]
                ]
                results.append({
                    "title": w.get("title", ""),
                    "authors": [a for a in authors if a],
                    "year": str(w.get("publication_year", "")),
                    "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                    "verified": True,
                })
            return results
    except Exception:
        return []
