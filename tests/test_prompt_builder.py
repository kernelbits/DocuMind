from prompt_builder import build_prompt

REFUSAL = "I cannot find an answer in the provided documents."


def test_returns_system_and_user_messages_in_order():
    messages = build_prompt("What is Yggdrasil?", "some context")

    assert [m["role"] for m in messages] == ["system", "user"]


def test_system_prompt_restricts_answers_to_the_context():
    system = build_prompt("q", "ctx")[0]["content"]

    assert "Use ONLY the information provided in the PDF Context" in system
    assert REFUSAL in system


def test_user_message_contains_context_and_question_when_context_given():
    user = build_prompt("What is Yggdrasil?", "[Source 1]\nWorld tree")[1]["content"]

    assert "PDF Context:\n[Source 1]\nWorld tree" in user
    assert "Question: What is Yggdrasil?" in user
    assert "No PDF context was found" not in user


def test_no_context_is_flagged_in_user_message():
    user = build_prompt("What is Yggdrasil?", None)[1]["content"]

    assert "Question: What is Yggdrasil?" in user
    assert "No PDF context was found" in user
    assert "PDF Context:" not in user


def test_whitespace_only_context_counts_as_no_context():
    user = build_prompt("q", "   \n\t ")[1]["content"]

    assert "No PDF context was found" in user
