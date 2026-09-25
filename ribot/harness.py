"""A tool-calling loop. See SPEC.md section 5."""

from collections.abc import Callable
from dataclasses import dataclass

CAPPED_ANSWER = "Stopped: tool call limit reached."


@dataclass(frozen=True)
class AgentResult:
    """What the agent produced, and how much work it took to get there."""

    answer: str
    tool_calls: int
    capped: bool


def run_agent(
    llm,
    tools: dict[str, Callable[[str], str]],
    question: str,
    max_tool_calls: int = 3,
) -> AgentResult:
    """Ask the model for steps, dispatching tools until it answers."""
    transcript: list[str] = []
    calls = 0

    while True:
        step = llm.next_step(question, transcript)
        if step.kind == "answer":
            return AgentResult(answer=step.text, tool_calls=calls, capped=False)

        tool = tools[step.tool_name]
        transcript.append(tool(step.tool_input))
        calls += 1
