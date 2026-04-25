import httpx

LT_URL = "http://localhost:8072"

ACADEMIC_RULE_IDS = {
    "PASSIVE_VOICE", "SENTENCE_WHITESPACE", "COMMA_PARENTHESIS_WHITESPACE",
    "DOUBLE_PUNCTUATION", "UPPERCASE_SENTENCE_START",
}

BANNED_PHRASES = [
    "leverage", "leveraging", "leveraged", "innovative solution",
    "cutting-edge", "in conclusion,", "as we can see", "it is worth noting that",
    "needless to say", "of course,", "it goes without saying",
    "state of the art" , "bleeding edge", "robust solution",
    "synergy", "paradigm shift", "holistic approach",
]


async def is_alive() -> bool:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{LT_URL}/v2/languages")
            return r.status_code == 200
    except Exception:
        return False


async def check(text: str, language: str = "en-US") -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(
                f"{LT_URL}/v2/check",
                data={"text": text, "language": language},
            )
            if r.status_code != 200:
                return []
            data = r.json()
            return data.get("matches", [])
    except Exception:
        return []


async def get_issues(text: str) -> list[str]:
    matches = await check(text)
    issues = []
    for m in matches:
        rule_id = m.get("rule", {}).get("id", "")
        msg = m.get("message", "")
        if rule_id or msg:
            issues.append(f"[{rule_id}] {msg}")
    return issues[:20]  # cap at 20 issues


def find_banned_phrases(text: str) -> list[str]:
    text_lower = text.lower()
    return [p for p in BANNED_PHRASES if p in text_lower]


def replace_banned_phrases(text: str) -> tuple[str, list[str]]:
    replacements = {
        "leverage": "use",
        "leveraging": "using",
        "leveraged": "used",
        "innovative solution": "approach",
        "cutting-edge": "advanced",
        "as we can see": "",
        "it is worth noting that": "",
        "needless to say": "",
        "of course,": "",
        "bleeding edge": "advanced",
        "robust solution": "effective approach",
        "synergy": "combination",
        "paradigm shift": "significant change",
        "holistic approach": "comprehensive approach",
    }
    fixed = []
    for phrase, replacement in replacements.items():
        if phrase in text.lower():
            import re
            text = re.sub(re.escape(phrase), replacement, text, flags=re.IGNORECASE)
            fixed.append(phrase)
    return text, fixed
