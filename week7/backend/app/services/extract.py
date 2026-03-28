import re

ACTION_PATTERNS = (
    re.compile(r"^(todo|action)\s*:\s*", re.IGNORECASE),
    re.compile(r"\b(need to|must|please|should|follow up|assign(ed)? to|owner:)\b", re.IGNORECASE),
    re.compile(
        r"\b(by|before|due)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|\d{4}-\d{2}-\d{2})\b",
        re.IGNORECASE,
    ),
)


def _normalize_line(line: str) -> str:
    return re.sub(r"^[\-\*\d\.\)\s]+", "", line.strip())


def _is_actionable(line: str) -> bool:
    if line.endswith("!"):
        return True
    return any(pattern.search(line) for pattern in ACTION_PATTERNS)


def extract_action_items(text: str) -> list[str]:
    lines = [_normalize_line(line) for line in text.splitlines() if line.strip()]
    seen: set[str] = set()
    results: list[str] = []

    for line in lines:
        if not _is_actionable(line):
            continue
        dedupe_key = line.lower()
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        results.append(line)

    return results
