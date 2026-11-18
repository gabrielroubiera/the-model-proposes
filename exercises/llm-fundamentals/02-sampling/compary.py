import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "01-raw-api-call"))

from client import chat, LLM_MODEL

SYSTEM = "Response with one phrase."
QUESTION = "What is a token in LLM context?"
PROVIDER = {
    "order": ["Reka"],
    "allow_fallbacks": False
}
RUNS = 5
CONFIGS = [
    {
        "temperature": 0
    },
    {
        "temperature": 0.7
    },
    {
        "temperature": 1.5
    },
    {
        "temperature": 1,
        "top_p": 0.1
    },
    {
        "temperature": 1,
        "top_p": 1
    },

]

def sample(
    runs: int,
    **params
) -> list[str]:
    asnwers = []
    for _ in range(runs):
        body = chat(
            LLM_MODEL,
            SYSTEM,
            QUESTION,
            provider=PROVIDER,
            **params
        )
        print(body["provider"], "|", body["choices"][0]["message"]["content"])
        asnwers.append(body["choices"][0]["message"]["content"])
    return asnwers

if __name__ == "__main__":
    results = []
    for config in CONFIGS:
        print("\n", config)
        answers = sample(RUNS, **config)
        results.append((config, len(set(answers))))

    print("\nconfig | distinct")
    for config, distinct in results:
        print(config, "|", distinct, "of", RUNS)