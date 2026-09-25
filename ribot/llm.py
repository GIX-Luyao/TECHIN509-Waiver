"""Offline stand-ins for a tool-calling model. Deterministic by construction."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Step:
    """One decision from the model: either call a tool, or answer."""

    kind: str  # "tool" or "answer"
    text: str = ""
    tool_name: str = ""
    tool_input: str = ""


@dataclass
class FakeToolLLM:
    """A model that asks for a tool until it has seen ``answer_after`` tool results.

    ``answer_after=None`` means it never stops asking — use it to check that the caller
    enforces its own limit.
    """

    answer_after: int | None = None
    tool_name: str = "search"
    answer: str = "final answer"
    seen: list[int] = field(default_factory=list)

    def next_step(self, question: str, transcript: list[str]) -> Step:
        self.seen.append(len(transcript))
        if self.answer_after is not None and len(transcript) >= self.answer_after:
            return Step(kind="answer", text=self.answer)
        return Step(kind="tool", tool_name=self.tool_name, tool_input=question)
