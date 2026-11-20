<div align="center">

# The Model Proposes

### Code decides. Evals judge.

A public notebook on AI engineering:<br/>
hands-on builds, measured experiments and paper notes on making LLM systems **reliable**.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/python-3.12-3776AB?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-ongoing%20study-orange)
![Data](https://img.shields.io/badge/data-public%20or%20synthetic-success)

[Why](#why-this-exists) · [The thread](#the-thread) · [What's inside](#whats-inside) · [Areas](#areas) · [Log](#log) · [Format](#experiment-format)

</div>

---

## Why this exists

I build LLM systems for a living, and I want to understand every layer of them well
enough to explain it, break it and measure it. This repo is where that study happens
in the open, with no end date:

- **Build** each technique by hand, from the basics up, until it holds under tests.
- **Measure** the questions that practice raises, instead of trusting intuition.
- **Read** the research, replicate what matters and note where it does not hold.

The long-term goal is to turn the strongest results into publishable work.

## The thread

The repo covers the whole stack, but one conviction runs through it: an LLM is a
brilliant, unreliable collaborator, and most production failures come from asking it
to *guarantee* things such as permissions, arithmetic, confirmations and identifiers.

So the guarantees go to code. The model proposes; code checks every proposal before
anything happens; evals tell you whether the system actually works.

```mermaid
flowchart LR
    U([User]) --> M
    subgraph S["What evals judge"]
        direction LR
        M["Model<br/><b>proposes</b>"] --> C{"Code<br/><b>decides</b>"}
    end
    C -- allowed --> A([Action])
    C -- denied --> R([Honest refusal])
```

> **The model** extracts, classifies and writes.<br/>
> **Code** authorizes, verifies and composes.<br/>
> **Evals** tell you whether any of it is true.

Not every entry is about this split. Retrieval, voice or fine-tuning entries are here
because you cannot decide where the model should stop without knowing what it can do.

## What's inside

Three kinds of entries, each held to its own bar.

| | Kind | What it is | The bar |
|---|---|---|---|
| 🔨 | **Exercise** | One technique built by hand | Working code, offline tests where there is logic that can break, a short note on what was learned |
| 🔬 | **Experiment** | A question with a measured answer | Hypothesis written first, repeated runs, an interval, the cost, the limits |
| 📄 | **Paper note** | A paper read or replicated | What it claims, how it measures it, what it does not show |

Rules that apply to all of them:

| Rule | What it means |
|---|---|
| **Code-level** | Small modules, not platforms. Nothing is scaffolded in advance. |
| **Reproducible** | One command, pinned versions, a fixed seed where it applies. |
| **Open data only** | Public or synthetic data. Nothing from an employer or a client. |
| **Negative results count** | What did not work is published with the evidence. |
| **Failures first** | When an entry is about a failure mode, it starts with the test that reproduces it. |

## Areas

<details open>
<summary><b>Build</b> — exercises</summary>

<br/>

| Area | Topics |
|---|---|
| **LLM fundamentals** | Sampling, structured output, caching, cost |
| **Context engineering** | Budgets, compaction, pre-LLM gates, query rewriting |
| **Harness** | Tool loops, dynamic tool loading, LangGraph, human-in-the-loop, multi-agent |
| **State and memory** | Short and long-term memory, concurrency, state rebuilt from history |
| **Design patterns** | Model extracts / code decides, cascades, propose-confirm-apply, fail-open |
| **Vector search** | Qdrant, hybrid search, reranking, chunking, retrieval metrics |
| **RAG** | Citations, honest no-answer, agentic retrieval |
| **MCP** | Servers, guardrails, auth |
| **Voice and vision** | STT, TTS, voice agents, image-to-query, visual documents |
| **Security** | Prompt injection, authorization in code, red teaming |
| **Evals and observability** | Judges, confidence intervals, tracing, latency |
| **AI product** | Attachments, tabular analysis, generated files |
| **Models and core ML** | Local models, LoRA, classic baselines |
| **Serving** | OpenAI-compatible endpoints, streaming, cancellation, degradation |

</details>

<details>
<summary><b>Measure</b> — experiments</summary>

<br/>

| Area | Questions |
|---|---|
| **Experimental method** | Variance, ablations, significance with few cases, cost reporting |
| **Agent reliability** | Tool and agent count, consistency, prompt versus code, long-context decay |
| **Calibration and uncertainty** | Confidence, abstention, self-consistency, judge reliability |
| **Retrieval in depth** | Synthetic eval sets, cross-lingual search, numbers and tables, thresholds |
| **Output control** | Constrained decoding, schema failure rates, prompt optimization |
| **Economics** | Cost-quality frontier, distillation, semantic caching |
| **Data** | Datasets from traces, synthetic cases, drift |
| **Measured security** | Attack success rate, injection channels, the cost of each defense |
| **Voice in Spanish** | Transcription accuracy on regional Spanish, turn-taking, perceived latency |

</details>

## Log

Newest first. One line per finished exercise, experiment or paper note.

| Date | Kind | Entry | Takeaway |
|---|---|---|---|
| 2026-11-19 | Exercise | [06 · Prompt rewrite](exercises/context-engineering/06-prompt-rewrite/) | A vague prompt let the model pick a different role and shape per ticket. Role, `<ticket>` delimiters, a two-line format and two examples gave the same parseable shape every time. Both prompts refused the injected instruction, so this does not show what delimiters stop |
| 2026-11-19 | Exercise | [05 · Prompt caching](exercises/llm-fundamentals/05-prompt-caching/) | A cached prefix cost 3–5 times less, but only while calls stayed on one provider, and even pinned it missed once. Latency showed no clear gain at about 3000 tokens |
| 2026-11-19 | Exercise | [04 · Parameter layer](exercises/llm-fundamentals/04-parameter-layer/) | One function drops `temperature` when reasoning effort is set, and says so. The model reasoned even with no effort, and `high` used fewer reasoning tokens than `low` in one run: effort is a hint, not a budget |
| 2026-11-19 | Exercise | [03 · Structured output](exercises/llm-fundamentals/03-structured-output/) | JSON mode, tool calling and a strict schema all returned a valid object on a clear ticket. Valid is not correct: `product` differed between ways. A tested validator with a capped retry decides what is accepted |
| 2026-11-17 | Exercise | [02 · Sampling](exercises/llm-fundamentals/02-sampling/) | Temperature 0 was not deterministic: 3 distinct answers of 5 with the provider fixed. `top_p` showed no effect. Five runs per setting show a direction, not a measured effect |
| 2026-11-17 | Exercise | [01 · Raw API call](exercises/llm-fundamentals/01-raw-api-call/) | A chat call is one POST with a list of messages. Streaming is the same request with `stream: true`, and `usage` comes in the last chunk. Reasoning took most of the completion tokens |
| 2026-11-17 | — | Repository created | Experiment template in place |

## Experiment format

Every experiment is a folder with the same shape, so results stay comparable.

| Section | Content |
|---|---|
| **Question** | One line. |
| **Hypothesis** | Written *before* running anything. |
| **Setup** | Data, models, versions, seed and number of runs. |
| **Result** | A table or chart, with an interval. |
| **Limits** | What it does not show. |
| **Reproduce** | One command. |

Start from [`templates/experiment.md`](templates/experiment.md).

## Layout

Folders appear as the work happens.

```text
the-model-proposes/
├── exercises/<area>/<entry>/      # hands-on builds
├── experiments/<area>/<entry>/    # measured experiments
├── papers/<paper>.md              # reading and replication notes
└── templates/experiment.md        # write-up template
```

## Stack

![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?logo=langgraph&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-DC244C?logo=qdrant&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?logo=pytest&logoColor=white)

---

<div align="center">

Built by [Gabriel Rodríguez Ubiera](https://github.com/gabrielroubiera) · [MIT](LICENSE)

</div>
