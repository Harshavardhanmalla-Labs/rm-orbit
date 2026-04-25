import httpx

BASE_URL = "https://api.crossref.org"
HEADERS = {
    "User-Agent": "Research-Platform/1.0 (mailto:research@freedomlabs.in)",
}


async def verify_doi(doi: str) -> dict | None:
    if not doi:
        return None
    doi_clean = doi.strip().removeprefix("https://doi.org/").removeprefix("http://doi.org/")
    try:
        async with httpx.AsyncClient(timeout=15, headers=HEADERS) as client:
            r = await client.get(f"{BASE_URL}/works/{doi_clean}")
            if r.status_code != 200:
                return None
            data = r.json().get("message", {})
            authors = []
            for a in data.get("author", []):
                name = f"{a.get('family', '')} {a.get('given', '')}".strip()
                if name:
                    authors.append(name)
            issued = data.get("issued", {}).get("date-parts", [[None]])[0]
            year = str(issued[0]) if issued and issued[0] else ""
            title_list = data.get("title", [])
            title = title_list[0] if title_list else ""
            journal_list = data.get("container-title", [])
            journal = journal_list[0] if journal_list else ""
            return {
                "title": title,
                "authors": authors,
                "year": year,
                "journal": journal,
                "doi": doi_clean,
                "verified": True,
            }
    except Exception:
        return None


async def search(query: str, rows: int = 5) -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=15, headers=HEADERS) as client:
            r = await client.get(
                f"{BASE_URL}/works",
                params={"query": query, "rows": rows, "select": "title,author,published,DOI,container-title"},
            )
            if r.status_code != 200:
                return []
            items = r.json().get("message", {}).get("items", [])
            results = []
            for item in items:
                authors = []
                for a in item.get("author", []):
                    name = f"{a.get('family', '')} {a.get('given', '')}".strip()
                    if name:
                        authors.append(name)
                issued = item.get("published", {}).get("date-parts", [[None]])[0]
                year = str(issued[0]) if issued and issued[0] else ""
                title_list = item.get("title", [])
                title = title_list[0] if title_list else ""
                journal_list = item.get("container-title", [])
                journal = journal_list[0] if journal_list else ""
                results.append({
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "journal": journal,
                    "doi": item.get("DOI", ""),
                    "verified": True,
                })
            return results
    except Exception:
        return []
