import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "llm-fundamentals" / "01-raw-api-call"))
from client import chat, LLM_MODEL  # type: ignore

KEEP_LAST = 4  # messages the window keeps verbatim

HISTORY = [
    {
        "role": "user",
        "content": "Hi, my order number is A-7731 and it arrived damaged."
    },
    {
        "role": "assistant",
        "content": "Sorry about that. What was damaged?"
    },
    {
        "role": "user",
        "content": "The lid of the blender is cracked."
    },
    {
        "role": "assistant",
        "content": "Thanks. Do you want a refund or a replacement?"
    },
    {
        "role": "user",
        "content": "A replacement, please."
    },
    {
        "role": "assistant",
        "content": "Done. Anything else I can help with?"
    },
    {
        "role": "user",
        "content": "Can you ship it to my office instead of home?"
    },
    {   "role": "assistant",
        "content": "Sure. What is the office address?"
    },
    {
        "role": "user",
        "content": "Calle Duarte 45, second floor."
    },
    {
        "role": "assistant",
        "content": "Got it, the replacement goes to Calle Duarte 45, second floor."
    },
]

SUMMARY_SYSTEM = (
    "You keep a running summary of a support conversation. "
    "You get the current summary and new messages. Return the updated summary only, "
    "in a few short sentences. Keep identifiers, names, numbers, addresses exactly as written"
)

AGENT_SYSTEM = (
    "You are a support agent. Answer only from the conversation context below. "
    "If something is not in it, say you do not know."
)

QUESTION = "Which order is being replaced, what part was damaged, and where does the replacement ship?"


def ask(context):
    user = f"Conversation context:\n{context}\n\nQuestion: {QUESTION}"
    reply = chat(LLM_MODEL, AGENT_SYSTEM, user)
    return reply["choices"][0]["message"]["content"].strip()


def render(messages):
    return "\n".join(f"{m['role']}: {m['content']}" for m in messages)


def sliding_window(history, keep=KEEP_LAST):
    return history[-keep:]

def update_summary(summary, messages):
    user = f"Current summary:\n{summary or '(empty)'}\nNew messages:\n{render(messages)}"
    reply = chat(LLM_MODEL, SUMMARY_SYSTEM, user)
    return reply["choices"][0]["message"]["content"].strip()

def compact(history, keep):
    old = history[:-keep] if keep else history
    recent = history[-keep:] if keep else []
    summary = ""
    for i in range(0, len(old), 2):
        summary = update_summary(summary, old[i : i + 2])
    return summary, recent

def ask(context):
    user = f"Conversation context:\n{context}\n\nQuestion: {QUESTION}"
    reply = chat(LLM_MODEL, AGENT_SYSTEM, user)
    return reply["choices"][0]["message"]["content"].strip()

if __name__ == "__main__":
    summary_only, _ = compact(HISTORY, 0)
    mixed_summary, recent = compact(HISTORY, KEEP_LAST)

    contexts = {
        "window": render(sliding_window(HISTORY)),
        "summary": f"Summary of earlier conversation:\n{summary_only}",
        "mixed": f"Summary of earlier conversation:\n{mixed_summary}\n\nRecent messages:\n{render(recent)}",
    }
    for name, context in contexts.items():
        print(f"[{name}] context is {len(context)} chars")
        print("  answer:", ask(context), "\n")