import sys
import math

from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "llm-fundamentals" / "01-raw-api-call"))
from client import chat, LLM_MODEL  # type: ignore


WINDOW = 8000           # tokens the model can see (small on purpose)
RESERVED_OUTPUT = 1000  # kept free the answer
TOOL_CAP = 1500         # max tokens for one tool result
CHARS_PER_TOKEN = 4     # rough estimate, not a real tokenizer
TURN_CAP = 3000         # max tokens for all tool resuts in one turn
OMIT_RESERVE = 20       # room kept the final "omitted" note


class ContextTooLarge(Exception):
    pass


def estimate_tokes(text):
    return math.ceil(len(text) / CHARS_PER_TOKEN)

def cap_tool_result(text, cap=TOOL_CAP):
    tokens = estimate_tokes(text)
    if tokens <= cap:
        return text
    marker = f"\n[truncated: about {tokens - cap} tokens dropped]"
    keep = cap - estimate_tokes(marker)
    return text[: keep * CHARS_PER_TOKEN] + marker

def fit_turn(results, turn_cap=TURN_CAP):
    budget = turn_cap - OMIT_RESERVE
    fitted = []
    used = 0
    for i, text in enumerate(results):
        text = cap_tool_result(text)
        left = budget - used    
        if estimate_tokes(text) > left:
            if left <= 50:
                fitted.append(f"[omitted {len(results) - i} results: turn budget used up]")
                break
            text  = cap_tool_result(text, cap=left)
        fitted.append(text)
        used += estimate_tokes(text)
    return fitted

def build_turn(system, user, results):
    base = estimate_tokes(system) + estimate_tokes(user)
    room = WINDOW - RESERVED_OUTPUT - base
    if room < 0:
        raise ContextTooLarge(
            f"base prompt is {base} tokens, only {WINDOW - RESERVED_OUTPUT} fit"
        )
    fitted = fit_turn(results, turn_cap=min(TURN_CAP, room))
    return user + "\n\n" + "\n\n".join(fitted)

if __name__ == "__main__":
    results = ["row; " * 960, "row; " * 3000, "row; " * 640, "row; " * 320]
    question = "How many tool results were omitted?"
    cases = [
        ("short system", "You answer from the tool results below.", True),
        ("long system", "rule; " * 4000, False),
        ("huge system", "rule; " * 8000, False),
    ]
    for name, system, call in cases:
        try:
            user = build_turn(system, question, results)
        except ContextTooLarge as e:
            print(f"[{name}] no call made: {e}")
            continue
        total = estimate_tokes(system) + estimate_tokes(user)
        print(f"[{name}] estimated prompt {total} of {WINDOW - RESERVED_OUTPUT}")
        if call:
            reply = chat(LLM_MODEL, system, user)
            print("  usage.prompt_tokens:", reply["usage"]["prompt_tokens"])
            print("  answer:", reply["choices"][0]["message"]["content"][:120])