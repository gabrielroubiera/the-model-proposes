import os
from extract import parse_ticket
from extract import parse_ticket, extract_with_retry

for var in ("LLM_PROVIDER_URL", "LLM_PROVIDER_KEY", "LLM_MODEL"):
    os.environ.setdefault(var, "fake")

import pytest
from extract import parse_ticket

def test_valid_ticket():
    raw = '{"name": "A", "product": "B", "urgency": "low"}'
    assert parse_ticket(raw) == {"name": "A", "product": "B", "urgency": "low"}

def test_formatting_does_not_matter():
    raw = '{\n  "name": "A",\n  "product": "B",\n  "urgency": "low"\n}'
    assert parse_ticket(raw)["urgency"] == "low"

def fake_extract(replies):
    calls = []
    def extract(user):
        calls.append(user)
        return replies[len(calls) - 1]
    return extract, calls

def test_retry_fixes_bad_reply():
    extract, calls = fake_extract(['{"name": "A"}', '{"name": "A", "product": "B", "urgency": "low"}'])
    assert extract_with_retry(extract, "ticket")["urgency"] == "low"
    assert len(calls) == 2
    assert "missing keys" in calls[1]

def test_retry_gives_up():
    extract, calls = fake_extract(["bad", "still bad", "never called"])
    with pytest.raises(ValueError, match="gave up after 2 attempts"):
        extract_with_retry(extract, "ticket")
    assert len(calls) == 2

@pytest.mark.parametrize("raw, message", [
    (None, "empty response"),
    ('```json\n{"name": "A"}\n```', "not valid JSON"),
    ("[1, 2]", "expected a JSON object"),
    ('{"name": "A", "product": "B"}', "missing keys"),
    ('{"name": "A", "product": "B", "urgency": "low", "x": 1}', "unexpected keys"),
    ('{"name": "A", "product": "B", "urgency": "urgent"}', "urgency must be one of"),
])
def test_rejects_bad_output(raw, message):
    with pytest.raises(ValueError, match=message):
        parse_ticket(raw)