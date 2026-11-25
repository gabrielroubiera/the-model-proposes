# To-do

Everything planned for this repo. Tick an item when its folder has code, a short note, and tests where there is logic that can break.
★ = priority. Build items are numbered 1–116; experiments are E01–E49.

## Part I — Build

### 01 · LLM fundamentals

- [x] 1. Call a provider API with no framework: messages, system, streaming, tokens and cost per call.
- [x] 2. Compare temperature and `top_p` on the same question and record the variation.
- [x] 3. ★ Structured output three ways (JSON mode, tool calling, strict schema), forcing and handling failures.
- [x] 4. Parameter layer: do not send temperature when reasoning effort is set.
- [x] 5. Prompt caching: measure cost and latency with and without a cached prefix.

**Study:** BPE tokenization, logits and sampling, causes of hallucination, reasoning models, why temperature 0 is not deterministic.

### 02 · Context engineering

- [x] 6. Rewrite a bad prompt with role, few-shot, delimiters and output format.
- [x] 7. ★ Window budget: per-tool caps, accumulated cap per turn, and an error before calling the model when the base prompt does not fit.
- [x] 8. History compaction: sliding window, incremental summary and mixed; compare what is lost.
- [ ] 9. Pre-LLM gates: gibberish detector and greetings that skip RAG.
- [ ] 10. Query rewriting with history, degrading to the raw message.
- [ ] 11. Prompt composition from fragments, never `.format()` over the full text.

**Study:** Lost in the middle, context ordering, prefix caching, when more context hurts.

### 03 · Harness (the agent loop)

- [ ] 12. ★ Hand-written tool-calling loop: round cap, parallel calls, errors returned to the model.
- [ ] 13. Five tools with a good `args_schema`; measure how often the model picks wrong.
- [ ] 14. ★ Dynamic tool loading: out of 50, offer only the relevant ones by search or by turn state.
- [ ] 15. Forced `tool_choice` on the first round, free afterwards.
- [ ] 16. LCEL: `prompt | model | parser`, parallels, fallbacks and retries.
- [ ] 17. Custom callbacks for tokens and latency.
- [ ] 18. `StateGraph` with typed state, reducers, conditional edges and `Command`.
- [ ] 19. ReAct agent from scratch, then with the prebuilt one.
- [ ] 20. ★ Checkpointer: threads, resume, time travel and forking.
- [ ] 21. ★ Human-in-the-loop with `interrupt`: approve, edit or reject.
- [ ] 22. Subgraphs with private and shared state.
- [ ] 23. Multi-agent: supervisor, handoffs and `Send` for fan-out.
- [ ] 24. Streaming of tokens, state updates and custom events.
- [ ] 25. Nodes as module-level functions, tested alone with a fake turn.
- [ ] 26. Degradation helper: build, invoke, extract text, fall back.
- [ ] 27. Per-tool progress messages during the turn.

**Study:** What `bind_tools` does underneath, token cost of schemas, per-node durability and retries, recursion limits.

### 04 · State and memory

- [ ] 28. Short-term: history in thread state with trimming and summary.
- [ ] 29. ★ Long-term with the LangGraph Store: per-user namespaces and semantic search.
- [ ] 30. Semantic, episodic and procedural memory, one implementation of each.
- [ ] 31. Memory writes in the hot path versus in the background.
- [ ] 32. ★ Per-conversation state with compare-and-set, persisting empties too.
- [ ] 33. Agent that rebuilds its state from history with a capped extract node.
- [ ] 34. Memoized extract: one call per turn for both progress and graph.
- [ ] 35. Memory that clears itself: a search with no results wipes carried criteria.

**Study:** What to store and what to forget, stale or conflicting memories, isolation between users, checkpointer versus custom state.

### 05 · Design patterns

- [ ] 36. ★ Model extracts, code decides: code verification of what the model transcribes (Luhn, MRZ).
- [ ] 37. ★ Bounded agent cascade: if one cedes, move to the next without calling the router again.
- [ ] 38. Code vetoes and claims (no LLM) versus rewording agent descriptions.
- [ ] 39. ★ Propose, confirm, apply: of two concurrent "yes" only one writes.
- [ ] 40. Confirmation that can only restrict: validated against the user's actual text.
- [ ] 41. Fail-open: no session or a storage error never fails the turn.
- [ ] 42. References, not data: the model names an id and code composes the output.
- [ ] 43. Sequence in code with an LLM per stage.
- [ ] 44. Closed triage: the model picks one intent and code builds the output, with a safe default on failure.
- [ ] 45. Tell "off-topic" apart from "extraction failed".
- [ ] 46. A router that never raises: a failure means "no agent".
- [ ] 47. Links and files built by code, never by the model.

**Study:** When a coded flow beats an agent, where each guarantee belongs (prompt, schema or code), the cost of every extra call.

### 06 · Vector search services

- [ ] 48. Qdrant collection with payload, metadata filters and per-tenant filters.
- [ ] 49. ★ Dense, sparse and hybrid search with RRF fusion.
- [ ] 50. Named vectors and multivector (ColBERT).
- [ ] 51. Scalar and binary quantization: memory, latency and recall loss.
- [ ] 52. Compare three embedding models in Spanish on your own documents.
- [ ] 53. ★ Cross-encoder reranker after retrieval.
- [ ] 54. Fixed, recursive, semantic and structure-aware chunking; compare.
- [ ] 55. Ingestion of PDF, Word and tables with source metadata.
- [ ] 56. Contextual retrieval and parent-document.
- [ ] 57. ★ 30-question set with expected document: recall@k, MRR and nDCG before and after each change.
- [ ] 58. Fine-tune an embedding model on question-document pairs and measure the gain.
- [ ] 59. Reindexing when the model or dimensions change.

**Study:** HNSW (`m`, `ef_construct`, `ef`), cosine versus dot product, Matryoshka, payload indexes, score thresholds.

### 07 · RAG

- [ ] 60. Basic RAG with verifiable citations.
- [ ] 61. Honest answer when there is no context; a retrieval failure does not break the chat.
- [ ] 62. Multi-query, HyDE and query decomposition.
- [ ] 63. Agentic RAG: the agent decides when and what to search.
- [ ] 64. ★ Document allowlist: the model reads only what retrieval brought in that conversation.
- [ ] 65. Isolate whether a failure is retrieval or generation.

**Study:** GraphRAG, long context versus RAG, common RAG failure modes.

### 08 · MCP

- [ ] 66. Server with tools, resources and prompts over stdio and HTTP.
- [ ] 67. Consume it from LangGraph through the adapters.
- [ ] 68. Read-only guardrails and call auditing.
- [ ] 69. OAuth authentication.

**Study:** Elicitation and sampling, tool poisoning, MCP versus a plain API.

### 09 · Voice and vision

- [ ] 70. Batch transcription with timestamps and diarization.
- [ ] 71. Streaming transcription with voice activity detection.
- [ ] 72. Streaming TTS while the LLM is still generating.
- [ ] 73. ★ Voice agent STT → LLM → TTS with barge-in, measuring latency per stage.
- [ ] 74. The same agent with a speech-to-speech model; compare.
- [ ] 75. ★ Image to query: describe the image and search Qdrant.
- [ ] 76. Multimodal search with image and text embeddings in one collection.
- [ ] 77. Visual documents: pages as images (ColPali) versus OCR plus text.
- [ ] 78. Structured extraction from a scan with code verification.
- [ ] 79. Image generation and editing from an agent.

**Study:** WebRTC versus WebSocket, end-of-turn detection, WER, token cost of an image, dedicated OCR versus a vision model.

### 10 · Security

- [ ] 80. Attack your own RAG with indirect injection, then defend it.
- [ ] 81. ★ Random sentinel around untrusted content, with the attack against a fixed marker.
- [ ] 82. Routing over sanitized history: an attachment cannot claim the turn.
- [ ] 83. ★ Scope-based authorization by ids: view and manage separated, no identity means deny.
- [ ] 84. A resource id is valid only if it is in the turn's list, also when the list is empty.
- [ ] 85. Double permission check: when offering the tool and again when running it.
- [ ] 86. Security rules always composed, with a test that walks every prompt.
- [ ] 87. Identity sanitization before entering the system block.
- [ ] 88. PII redaction before tracing.
- [ ] 89. Automated red-team battery.

**Study:** OWASP Top 10 for LLM, exfiltration through links or images, the lethal trifecta.

### 11 · Evals and observability

- [ ] 90. ★ Golden set with a rubric LLM judge plus deterministic metrics.
- [ ] 91. Calibrate the judge against your own labels.
- [ ] 92. Routing and trajectory accuracy: tool, arguments and steps.
- [ ] 93. Lower bound of the confidence interval as the threshold.
- [ ] 94. Comparison against a baseline.
- [ ] 95. ★ From failure to case: failed conversation → regression test → set.
- [ ] 96. Trace every call with purpose, user and session.
- [ ] 97. Per-turn metrics: calls, rounds, time to first text; p50/p90 report.
- [ ] 98. Privacy-preserving tracing: shape and tokens only.
- [ ] 99. Cost reduction: cheap model for auxiliary tasks and routing by difficulty.

**Study:** Online versus offline evals, judge bias, simulated users, OpenTelemetry for LLM.

### 12 · AI product (user-facing features)

- [ ] 100. ★ Attachments by mode (inline, tabular, snippets) with an honest per-file notice and deduplication.
- [ ] 101. ★ Tabular analysis: the model queries a spreadsheet with read-only SQL.
- [ ] 102. A real chart from data, with highlighted figures computed by code.
- [ ] 103. A generated spreadsheet whose rows come from a query.
- [ ] 104. Two-step flow: review with alerts, confirm, generate.
- [ ] 105. Cards and suggestions composed by code.
- [ ] 106. Multi-turn data capture that is not resent on close.
- [ ] 107. Answer in the user's language and hand off to a human on sentiment.
- [ ] 108. Streaming the text field of a JSON output.
- [ ] 109. Capability list generated from the active tools.
- [ ] 110. Writing assistant: code composes the delivery.

**Study:** When to decline, how to communicate uncertainty, perceived latency.

### 13 · Models and core ML

- [ ] 111. Run an open model locally behind an OpenAI-compatible API.
- [ ] 112. Fine-tune a small model with LoRA and compare it with few-shot.
- [ ] 113. Classic classifier (embeddings plus logistic regression) versus an LLM on the same task.

**Study:** Transformer and attention, quantization, distillation, when to fine-tune and when RAG is enough.

### 14 · Serving with FastAPI

- [ ] 114. OpenAI-compatible endpoint, with and without SSE streaming.
- [ ] 115. Cancellation, timeouts and retries.
- [ ] 116. OpenAI-shaped errors and provider degradation.

## Part II — Measure (continuous study)

### A · Experimental method

- [ ] E01. Measure variance: run the same eval 10 times and report mean and interval, not one number.
- [ ] E02. Ablations: remove one piece at a time and measure what each contributes.
- [ ] E03. Significance with few cases: bootstrap and paired tests between two variants on the same set.
- [ ] E04. Always report cost: quality against tokens, latency and dollars.
- [ ] E05. Replicate a published result on your own Spanish data and document where it does not hold.
- [ ] E06. Publish negative results, with the evidence.

### B · Agent reliability

- [ ] E07. Degradation curve by tool count: selection accuracy with 5, 20, 50 and 100 tools.
- [ ] E08. The same for agents: router accuracy by number of candidates and description similarity.
- [ ] E09. Consistency: success rate over k consecutive attempts, not one.
- [ ] E10. Prompt versus code: for the same rule, violation rate when it lives in the prompt, the schema or a code check.
- [ ] E11. Long-context decay: quality at 10, 50 and 150 turns, with and without compaction.
- [ ] E12. What compaction loses: questions whose answer was in the summarized part.
- [ ] E13. Sub-agent isolation: delegating a search versus running it in the main context.
- [ ] E14. Tools through code: the model writes a script calling several tools versus calling them one by one.
- [ ] E15. Error recovery: inject tool failures and measure whether the agent recovers, retries or fabricates.

### C · Calibration and uncertainty

- [ ] E16. Use logprobs to estimate confidence in a classification and plot the calibration curve.
- [ ] E17. Abstention: set a threshold to decline and measure coverage against error.
- [ ] E18. Self-consistency: sample several answers and use disagreement as a doubt signal.
- [ ] E19. Hallucination detection without a judge: verify each claim against retrieved context.
- [ ] E20. LLM judge reliability: agreement with you, position bias, sensitivity to rubric order.

### D · Retrieval in depth

- [ ] E21. Build the eval set from synthetic queries and validate that it predicts performance on real ones.
- [ ] E22. Hard-negative mining and its effect on embedding fine-tuning.
- [ ] E23. Cross-lingual retrieval: Spanish questions over English documents and the reverse.
- [ ] E24. Late chunking versus contextual chunking versus plain chunking.
- [ ] E25. Query routing: choose between vector, keyword, SQL or no search.
- [ ] E26. Tables and figures: why semantic search fails on numbers and what works instead.
- [ ] E27. Versioned documents: retrieve the current one among near-duplicates.
- [ ] E28. Text-to-SQL with verification: measure correct queries, not queries that run.
- [ ] E29. Score threshold: how to choose it from data and why it does not transfer across embedding models.

### E · Output control

- [ ] E30. Grammar-constrained decoding on a local model versus API structured output.
- [ ] E31. Structured-output failure rate by model and schema complexity.
- [ ] E32. Effect of the schema on quality: whether forcing JSON hurts reasoning and how to avoid it.
- [ ] E33. Automatic prompt optimization (DSPy-style) versus a hand-written prompt.

### F · Economics

- [ ] E34. Cost-quality frontier: a model cascade where the cheap one answers and escalates only on doubt.
- [ ] E35. Distill an expensive judge or classifier into a small model and measure the loss.
- [ ] E36. When a classic classifier over embeddings matches an LLM.
- [ ] E37. Semantic cache: hit rate against the rate of wrong answers served from cache.

### G · Data

- [ ] E38. Build a dataset from real traces with verifiable anonymization.
- [ ] E39. Synthetic data for rare cases, and proof that it does not bias the eval.
- [ ] E40. Drift detection: when user questions change or the provider updates the model.

### H · Measured security

- [ ] E41. Attack success rate: a fixed injection battery against each defense, with numbers.
- [ ] E42. Injection through tool results and file names, not only documents.
- [ ] E43. Cost of defense: how much utility each protection layer removes.

### I · Voice and Spanish

- [ ] E44. WER of several transcription models on real Dominican Spanish, proper names and code-switching.
- [ ] E45. Turn-taking evaluation: false interruptions and clipped pauses.
- [ ] E46. Perceived versus measured latency in a voice agent.

### J · Continuous reading

- [ ] E47. One paper a week, summarized in half a page: what it claims, how it measures it, what it does not show.
- [ ] E48. One paper replicated a month.
- [ ] E49. Track changes in the tools you use and note which of your practices became unnecessary.

## Research threads

Questions with production intuition behind them that still need rigorous measurement.

- [ ] Code veto versus rewording the agent description.
- [ ] State rebuilt from history versus a checkpointer: accuracy, cost, behavior under truncated history.
- [ ] Character budget versus a real tokenizer: how much error and when it matters.
- [ ] Model transcribes, code verifies: error reduction on identity documents.
- [ ] Confidence-interval lower bound as a gate on small eval sets.
- [ ] LLM systems over SAP, and Dominican Spanish.
