from ribot.harness import run_agent
from ribot.llm import FakeToolLLM


def _tools():
    return {"search": lambda query: f"result for {query}"}


def test_agent_returns_the_model_answer():
    llm = FakeToolLLM(answer_after=0, answer="hello")
    result = run_agent(llm, _tools(), "what is up?")
    assert result.answer == "hello"
    assert result.tool_calls == 0
    assert result.capped is False


def test_agent_dispatches_a_tool_before_answering():
    llm = FakeToolLLM(answer_after=1, answer="grounded")
    result = run_agent(llm, _tools(), "what is up?")
    assert result.answer == "grounded"
    assert result.tool_calls == 1
