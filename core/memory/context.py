import re
from core.memory.manager import search_memories


STOPWORDS = {
    "the", "a", "an", "is", "am", "are", "was", "were",
    "my", "me", "i", "you", "your", "to", "of", "and",
    "or", "in", "on", "for", "with", "about", "tell",
    "what", "who", "how", "why", "when", "where", "do",
    "does", "did", "can", "could", "would", "should",
    "please", "give", "show", "describe"
}


def build_memory_context(user_message, limit=5):
    words = re.findall(r"[a-zA-Z0-9_]+", user_message.lower())

    keywords = [
        word for word in words
        if len(word) >= 2 and word not in STOPWORDS
    ]

    if not keywords:
        return ""

    found = []
    seen = set()

    for keyword in keywords:
        memories = search_memories(keyword, limit)

        for memory in memories:
            memory_id = (memory["key"], memory["value"])

            if memory_id not in seen:
                seen.add(memory_id)
                found.append(memory)

            if len(found) >= limit:
                break

        if len(found) >= limit:
            break

    if not found:
        return ""

    lines = ["Relevant memories:"]

    for memory in found:
        lines.append(f"- {memory['key']}: {memory['value']}")

    return "\n".join(lines)
