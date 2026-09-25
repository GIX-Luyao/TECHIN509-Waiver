# HMSTI 509 — Waiver Exam

**60 minutes. AI agents allowed. Graded automatically.**


---

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest                          # the suite should be green
```

Work inside the virtual environment. Do not commit `.venv/`.

---

## Read `SPEC.md` first

`SPEC.md` is the authority. Where the code and the spec disagree, **the spec is right.**

---

## Task 1 — Write the tests

`tests/test_chunking.py` is empty. Write tests for `chunk_text` (`SPEC.md` §1).

`ribot/chunking.py` is already correct. You are not writing code here — you are writing the
tests that would have caught it if it weren't.

**How it is scored:** your test file is run against 8 broken versions of `chunk_text`. You get
a point for each broken version your tests catch. Your tests must also pass against the correct
version — and against a second, differently-written correct version, so test what the function
*does*, not how it is written. Asserting on the source text of `ribot/chunking.py` scores zero.

Keep the file self-contained: no `conftest.py`, no imports from other test files. The grader
runs `tests/test_chunking.py` by itself.

Avoid editing `ribot/chunking.py`. If you do, clearly document it in  `ribot/chunking.py`.

---

## Task 2 — Debugging

`ribot/similarity.py` and `ribot/retriever.py` each contain **one function that does not do
what `SPEC.md` says**. Both have tests that pass anyway.

1. Fix the code.
2. Fix the test that let the bug through.

**How it is scored:** four checks. Each module is run against the whole of `SPEC.md`, so fixing
one function by breaking another in the same file does not count. Each repaired test must pass
on correct code and **fail** if its bug is put back.

---

## Task 3 — Bound the agent loop

`ribot/harness.py::run_agent` never stops when the model keeps asking for tools.
`SPEC.md` §5 says when it must stop and what it must return. Make it do that.

---

## AI log — required

Fill in `AI_LOG.md`. Four lines, about two minutes. **A submission without it is not graded.**

---

## Submit

```bash
git add -A
git commit -m "waiver exam"
git push
```

Your **last push before the deadline** is graded. Do not force-push or rewrite history.

---

## Rules

- Do not edit `SPEC.md` or anything in `.github/`.
- Your code must run offline: no network, no API key, standard library only.
- Any AI assistant is allowed. You still have to submit code that works.
