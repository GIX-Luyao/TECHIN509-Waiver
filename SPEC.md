# `ribot` — Behavior Specification

This document is the authority. Where the code disagrees with this document, the code is wrong.

---

## 1. `ribot.chunking.chunk_text(text, size, overlap) -> list[str]`

Splits a string into overlapping character windows.

1. `size` must be an `int` >= 1. Otherwise raise `ValueError`.
2. `overlap` must be an `int` with `0 <= overlap < size`. Otherwise raise `ValueError`.
   Arguments are validated **before** `text` is examined.
3. Let `normalized = text.strip()`. If `normalized` is empty, return `[]`.
4. Let `step = size - overlap`.
5. Chunks are cut from `normalized` starting at index `0`, then `step`, then `2 * step`, and
   so on. Each chunk is at most `size` characters long.
6. The chunk whose end index first reaches or passes `len(normalized)` is the **last** chunk.
   No chunk is emitted after it. This means the final chunk may be shorter than `size`, and no
   chunk is ever wholly contained inside the one before it.
7. Chunks are returned as a `list`, in the order they appear in `normalized`. Duplicate
   chunks are kept.

---

## 2. `ribot.similarity.cosine_similarity(a, b) -> float`

1. Raise `ValueError` if `a` and `b` have different lengths.
2. If either vector has zero magnitude, return `0.0`.
3. Otherwise return the cosine of the angle between them: the dot product divided by the
   product of the two vectors' magnitudes. The result is always in `[-1.0, 1.0]`.

`cosine_similarity([3.0, 0.0], [3.0, 0.0])` is `1.0`, not `9.0`.

---

## 3. `ribot.similarity.top_k_indices(scores, k) -> list[int]`

1. Raise `ValueError` if `k < 0`.
2. Return the indices of the `k` highest values in `scores`, **highest score first**.
3. **Ties are broken by lowest index first.** `top_k_indices([0.5, 0.9, 0.9, 0.1], 2)` is
   `[1, 2]`.
4. If `k` exceeds `len(scores)`, return every index, ordered by rule 2.

---

## 4. `ribot.retriever.Retriever.search(query, k=3) -> list[Hit]`

The retriever is constructed with `chunks`, an `embed_fn`, and a `min_score` threshold
(default `0.0`).

1. Embed `query` with `embed_fn` and score every chunk against it with `cosine_similarity`.
2. **Discard every chunk whose score is strictly less than `min_score`.**
3. Return at most `k` of the surviving chunks as `Hit(text, score, index)`, **highest score
   first**, ties broken by lowest chunk index.
4. `index` is the chunk's position in the original `chunks` list.
5. Raise `ValueError` if `k < 1`.

---

## 5. `ribot.harness.run_agent(llm, tools, question, max_tool_calls=3) -> AgentResult`

A bounded tool-calling loop.

1. Repeatedly ask `llm.next_step(question, transcript)` for the next `Step`.
2. If the step's `kind` is `"answer"`, return
   `AgentResult(answer=step.text, tool_calls=<number dispatched so far>, capped=False)`.
3. If the step's `kind` is `"tool"`, call `tools[step.tool_name](step.tool_input)`, append the
   returned string to the transcript, and count one tool call.
4. **When the number of dispatched tool calls reaches `max_tool_calls`, stop immediately.**
   Do not ask the model again. Return
   `AgentResult(answer=CAPPED_ANSWER, tool_calls=max_tool_calls, capped=True)`,
   where `CAPPED_ANSWER` is the module-level constant in `ribot/harness.py`.
5. Raise `ValueError` if `max_tool_calls < 1`.
6. `run_agent` must terminate for every `llm`, including one that asks for a tool forever.
