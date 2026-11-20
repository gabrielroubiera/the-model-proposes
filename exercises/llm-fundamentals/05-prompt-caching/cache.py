import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "01-raw-api-call"))
from client import chat, LLM_MODEL  # type: ignore

PREFIX = "You are a support agent for a fictional store. \n" + "\n".join(
    f"Rule {i}: answer in one short sentence and never invent order numbers."
    for i in range(1, 201)
)

def timed_call(
    system: str,
    user: str,
    **params
) -> None:
    start = time.perf_counter()
    body = chat(LLM_MODEL, system, user, **params)
    seconds = time.perf_counter() - start
    usage = body["usage"]
    cached = (usage.get("prompt_tokens_details") or {}).get("cached_tokens")
    print(f"{seconds:.2f}s | prompt: {usage["prompt_tokens"]} | cached: {cached} "
          f"| cost: {usage.get("cost")} | provider: {body.get("provider")}")

if __name__ == "__main__":
    pin = {
        "provider": {
            "order": ["Alibaba"],
            "allow_fallbacks": False
        } 
    }

    print("--- same prefix ---")
    for _ in range(3):
        timed_call(PREFIX, "what is your return policy?", **pin)

    print("--- changing prefix ---")
    for i in range(3):
        timed_call(f"Session {time.time_ns()}-{i}.\n" + PREFIX, "What is your return policy?", **pin)