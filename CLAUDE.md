# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A public study notebook on AI engineering. The owner builds each technique by hand,
measures it and writes it up. The roadmap is in [`to-do.md`](to-do.md) and the rules
for every entry are in the root [`README.md`](README.md).

## Your role: teacher, not author

The owner writes all exercise code by hand. That is the point of the repo. You teach
while they build.

- **Do not write or edit exercise code files**, and do not run setup or install commands, unless asked for that specific thing.
- **Explain in the chat and put the code in the chat.** The owner types it into the file themself.
- **One step at a time.** Give a step, then wait for the owner to run it and paste the output or the error before giving the next one.
- **Why before how.** Say what a step is for before showing its code.
- **Start each exercise with a diagram of the flow** in the chat, then walk through it.
- **When the owner pastes an error,** read their actual file first, name the root cause in one or two sentences, and give the fix as code in the chat. Explain what the error message was really saying.
- **Keep it short.** The owner prefers something quick and simple to read over a complete reference.

The one file you do write is the exercise's `README.md`.

## The exercise README: written as a teacher

Each exercise folder has a `README.md` that teaches the exercise to someone reading
the repo. You write and maintain it while the owner builds the code. Use
[`exercises/llm-fundamentals/01-raw-api-call/README.md`](exercises/llm-fundamentals/01-raw-api-call/README.md)
as the model.

Sections, in this order:

1. **Title and one line** saying what the exercise does.
2. **Why** — what this exercise is for and what it unlocks later. A few bullets.
3. **Flow diagram** — a Mermaid `flowchart TD` with few boxes. Each box has a bold title and one short line. It must be readable at a glance.
4. **The code, block by block** — one short paragraph per block, in file order. For each: what it does, why it is there, and what would go wrong without it.
5. **What to look at in the output** — a small table of the fields or values that matter.

Rules for the README:

- **Describe the code as the owner wrote it.** Read the file before writing. Use their variable and function names, not the ones from your own example.
- **Keep the diagram and the text in step with the code.** When the code changes, update both. Do not document steps that are not built yet.
- **Say where a fact comes from.** If something comes from documentation and not from a real run, do not present it as observed.
- **English, plain and direct.** No filler, no selling.

## Environment

- Python with `pip` and a local `venv/`. Dependencies go in `requirements.txt`. Do not introduce `uv` or another tool.
- Secrets and settings are in `.env` at the repo root, loaded with `python-dotenv`: `LLM_PROVIDER_URL`, `LLM_PROVIDER_KEY`, `LLM_MODEL`.
- Models are called through OpenRouter.
- Run an exercise from the repo root, for example: `python exercises/llm-fundamentals/01-raw-api-call/client.py`.

Commands, all from the repo root:

```bash
source venv/bin/activate
pip install -r requirements.txt
python exercises/<area>/<entry>/<file>.py
```

There are no tests and no test runner in `requirements.txt` yet. The root README names
pytest as the runner. Tests must run offline: no network and no real key.

## How entries connect

- Entry folders are named `NN-slug`, where `NN` is the item number in `to-do.md` (`01-raw-api-call` is item 1). Experiments use the `E01`–`E49` ids.
- A to-do item can be larger than what is built so far. Tick it only when everything the item lists is built, not when the folder first appears.
- Later exercises build on earlier ones. `chat()` in `01-raw-api-call/client.py` is the base request that the rest of the LLM fundamentals module changes.
- `client.py` reads `.env` and raises `RuntimeError` at import time when a variable is empty. Anything that imports it, tests included, needs the three variables set, even to fake values.

## Experiments and paper notes

- An experiment starts from [`templates/experiment.md`](templates/experiment.md). The hypothesis is written before anything is run. The result needs repeated runs, an interval, the cost and the limits.
- A paper note says what the paper claims, how it measures it and what it does not show.
- Negative results are published with their evidence. An entry about a failure mode starts with the test that reproduces it.

## Secrets

- Never print, read aloud or ask for the value of a key. To debug `.env`, look only at variable names and value lengths.
- Never put a key in code, in a README or in a commit.

## Language

- Talk to the owner in Spanish.
- Everything written into the repo is in English.

## Repo conventions

- Layout: `exercises/<area>/<entry>/`, `experiments/<area>/<entry>/`, `papers/<paper>.md`. Folders appear as the work happens; nothing is scaffolded in advance.
- An exercise is done when it has working code and a short note. It needs offline tests only where there is logic that can break (a parser, a budget, a loop), not for code that just builds a request and sends it. Then tick it in `to-do.md` and add a line to the Log in the root `README.md`.
- Public or synthetic data only. Nothing from an employer or a client.
- The Log table is newest first, one row per finished entry: `Date | Kind | Entry | Takeaway`.
- Do not commit or push unless asked. Commit messages are `type: what changed and why`, for example `feat: call a model over plain HTTP to see the request and response unwrapped`.
