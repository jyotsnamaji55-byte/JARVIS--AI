import re

from core.memory.manager import save_memory


MEMORY_PATTERNS = [
    r"\bmy name is (.+)",
    r"\bmy project is (.+)",
    r"\bmy project name is (.+)",
    r"\bthe project name is (.+)",
    r"\bi am working on (.+)",
    r"\bmy goal is (.+)",
    r"\bmy favorite (.+?) is (.+)",
]


def extract_memories(text):
    text = text.strip()
    memories = []

    patterns = [
        ("user_name", MEMORY_PATTERNS[0]),
        ("project", MEMORY_PATTERNS[1]),
        ("project_name", MEMORY_PATTERNS[2]),
        ("project_name", MEMORY_PATTERNS[3]),
        ("current_work", MEMORY_PATTERNS[4]),
        ("goal", MEMORY_PATTERNS[5]),
    ]

    for key, pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            value = match.group(1).strip().rstrip(".!?")
            if value:
                memories.append((key, value))

    match = re.search(MEMORY_PATTERNS[6], text, re.IGNORECASE)

    if match:
        category = match.group(1).strip().replace(" ", "_")
        value = match.group(2).strip().rstrip(".!?")

        if category and value:
            memories.append((f"favorite_{category}", value))

    return memories


def remember_from_text(text):
    memories = extract_memories(text)

    for key, value in memories:
        save_memory(key, value)

    return memories
