import re
import unicodedata
import sys

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "llm-fundamentals" / "01-raw-api-call"))
from client import chat, LLM_MODEL  # type: ignore

GREETINGS = {
    "hi", "hello", "hey", "good", "morning", "afternoon", "evening",
    "hola", "buenas", "buenos", "dias", "tardes", "noches", "saludos",
}
CONSONANT_RUN = re.compile(r"[bcdfghjklmnpqrstvwxz]{5,}")
REPEAT = re.compile(r"(.)\1{3,}")
GREETING_REPLY = "Hi! How can I help you with your order?"
REPHRASE_REPLY = "Sorry, I could not understand that. Could you rephrase it?"
SYSTEM = "You are a support agent. Answer in one short sentence."

def normalize(text):
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", text)

def is_greeting(text):
    words = normalize(text)
    return bool(words) and all(w in GREETINGS for w in words)

def is_gibberish(text):
    stripped = "".join(text.split())
    if not stripped:
        return True
    words = normalize(text)
    alnum = sum(len(w) for w in words)
    if alnum / len(stripped) < 0.5:
        return True
    odd = [w for w in words if CONSONANT_RUN.search(w) or REPEAT.search(w)]
    return len(odd) / len(words) > 0.5

def route(text):
    if is_greeting(text):
        return "greeting", GREETING_REPLY
    if is_gibberish(text):
        return "gibberish", REPHRASE_REPLY
    return "rag", None


if __name__ == "__main__":
    messages = [
        "Hola!",
        "Buenos días",
        "asdkjh qwrtz",
        "",
        "holaaaa",
        "hey there",
        "¿Dónde está mi pedido A-7731?",
        "strengths",
    ]
    calls = 0
    for msg in messages:
        gate, reply = route(msg)
        if reply is None:
            calls += 1
            reply = chat(LLM_MODEL, SYSTEM, msg)["choices"][0]["message"]["content"].strip()
        print(f"[{gate:9}] {msg!r}\n  -> {reply}\n")
    print(f"model calls: {calls} of {len(messages)} messages")
