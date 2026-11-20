import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "01-raw-api-call"))

from client import chat, LLM_MODEL  # type: ignore


def build_params(
    temperature: float | None = None,
    effort: str | None = None
) -> dict:
    params = {}

    if effort is not None:
        params["reasoning"] = { "effort": effort}
        if temperature is not None:
            print(f"dropping temperature={temperature}: reasoning effort is set")
    elif temperature is not None:
        params["temperature"] = temperature
    return params


if __name__ == "__main__":
    question = "In one sentence: why is the sky blue?"

    for temperature, effort in [(0.7, None), (0.7, "low"), (None, "high")]:
        params = build_params(temperature=temperature, effort=effort)
        body = chat(LLM_MODEL, "Answer briefly.", question, **params)
        usage = body["usage"]
        reasoning = (usage.get("completion_tokens_details") or {}).get("reasoning_tokens")

        print(f"\n--- temperature={temperature} effort={effort} ---")
        print("sent: ", params)
        print("reasoning tokens: ", reasoning, "| completions tokens: ", usage["completion_tokens"])
        print(body["choices"][0]["message"]["content"])