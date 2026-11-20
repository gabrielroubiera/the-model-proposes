# Experiment backlog

Open questions raised by phase 1 exercises, collected as input for phase 2. Each one comes
from something an exercise wrote down or measured with a few runs. None of them is answered
yet.

When a question becomes an experiment, it gets a folder in the
[experiment format](../templates/experiment.md) and a link here. Where a question overlaps a
planned experiment in [`to-do.md`](../to-do.md), the id is noted.

## From [01 · Raw API call](../exercises/llm-fundamentals/01-raw-api-call/)

- What share of completion tokens goes to reasoning across many calls of the same question? One call gave 128 of 158.
- How often does OpenRouter switch providers between identical calls when none is pinned?
- How much time passes before the first answer token in a stream, and how does it relate to the reasoning tokens?

## From [02 · Sampling](../exercises/llm-fundamentals/02-sampling/)

- Are `temperature` and `top_p` applied to this model while it thinks, on this provider? DeepSeek's docs say no for its own API; it was not checked for Reka.
- With thinking turned off, does temperature change the number of distinct answers?
- Why did temperature 0 give 3 and 4 distinct answers of 5 with the provider fixed, and how stable is that count over more runs?
- Does a measure of how far answers are from each other show differences that exact match hides?

## From [03 · Structured output](../exercises/llm-fundamentals/03-structured-output/)

- How often does each way (JSON mode, tool calling, strict schema) return a reply that `parse_ticket` rejects, over many tickets and runs? Overlaps E31.
- How often is a valid object wrong? `product` differed between ways in one run.
- Does the strict schema behave the same across the providers that served it?

## From [04 · Parameter layer](../exercises/llm-fundamentals/04-parameter-layer/)

- Does reasoning effort change the number of reasoning tokens in a consistent direction? In one run `high` used 36 and `low` used 54.
- Does the model reason on every call when no effort is set?
- Does sending `temperature` together with reasoning get rejected, ignored or applied?

## From [05 · Prompt caching](../exercises/llm-fundamentals/05-prompt-caching/)

- With the provider pinned and the same prefix, how often is the cache missed?
- Does a cache hit lower latency with a longer prefix? No gain was detected at about 3000 tokens.
- How long does a cached prefix last?
- What block size does each provider cache in?

## From [06 · Prompt rewrite](../exercises/context-engineering/06-prompt-rewrite/)

- Do the `<ticket>` delimiters lower the rate at which injected instructions are obeyed? Overlaps E41.
- How often does the rewritten prompt break its two-line format over many tickets and runs?
- How much does each piece (role, delimiters, format, few-shot) contribute? Overlaps E02.
