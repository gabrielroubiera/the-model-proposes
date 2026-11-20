import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent.parent / "01-raw-api-call"))

from client import chat, LLM_MODEL # type: ignore

TICKET = (
    "Hi, this is Gabriel. Since this morning the Pro Plan dashboard"
    "won't load and my whole team is blocked. Please help ASAP."
)

SYSTEM_JSON = (
    "Extract data from the support ticket. Reply only with JSON with these keys: "
    '"name" (string), "product" (string), "urgency" ("low", "medium" or "high").'
)

SCHEMA = {
    "type": "object",
    "properties": {
        "name": { "type": "string" },
        "product": { "type": "string" },
        "urgency": { "type": "string", "enum": ["low", "medium", "high"] }
    },
    "required": ["name", "product", "urgency"],
    "additionalProperties": False
}

SYSTEM_TOOL = "Extract data from the support ticket and save it with the tool."

KEYS = {
    "name", 
    "product", 
    "urgency"
}
URGENCIES = {
    "low",
    "medium",
    "high"
}

def parse_ticket(raw: str | None) -> dict:
    if raw is None:
        raise ValueError("empty response")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"not valid JSON: {e}") from e
    if not isinstance(data, dict):
        raise ValueError(f"expected a JSON object, got {type(data).__name__}")
    missing = KEYS - data.keys()
    if missing:
        raise ValueError(f"missing keys: {sorted(missing)}")
    extra = data.keys() - KEYS
    if extra:
        raise ValueError(f"unexpected keys: {sorted(extra)}")
    if data["urgency"] not in URGENCIES:
        raise ValueError(f"urgency must be one of {sorted(URGENCIES)}, got {data['urgency']!r}")
    return data

def extract_json_mode(user: str) -> str:
    body = chat(
        LLM_MODEL,
        SYSTEM_JSON,
        user,
        response_format={"type": "json_object"}
    )

    return body["choices"][0]["message"]["content"]

def extract_tool_calling(user: str) -> str:
    body = chat(
        LLM_MODEL,
        SYSTEM_TOOL,
        user,
        tools=[{
            "type": "function",
            "function": {
                "name": "save_ticket",
                "description": "Save the extracted ticket data.",
                "parameters": SCHEMA
            },
        }],
        tool_choice={
            "type": "function",
            "function": {
                "name": "save_ticket",
            }
        }
    )

    message = body["choices"][0]["message"]
    print("content: ", repr(message.get("content")))
    return message["tool_calls"][0]["function"]["arguments"]

def extract_strict_schema(user: str) -> str:
    body = chat(
        LLM_MODEL,
        SYSTEM_TOOL,
        user,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "ticket",
                "strict": True,
                "schema": SCHEMA
            }
        },
        provider={"require_parameters": True},
    )
    print("provider: ", body["provider"])
    return body["choices"][0]["message"]["content"]

def extract_with_retry(
    extract,
    ticket: str,
    retries: int = 1
) -> dict:
    user = ticket
    for attempt in range(1, retries + 2):
        raw = extract(user)
        try:
            return parse_ticket(raw)
        except ValueError as e:
            print(f"attempt {attempt} rejected: {e}")
            error = e
            user = f"{ticket}\n\n Your previous reply was rejected: {e}. Reply again, fixing it."
    raise ValueError(f"gave up after {retries + 1} attempts: {error}")

if __name__ == "__main__":
    print("--- json mode ---")
    print(extract_with_retry(extract_json_mode, TICKET))

    print("\n--- tool calling ---")
    print(extract_with_retry(extract_tool_calling, TICKET))

    print("\n--- strict schema ---")
    print(extract_with_retry(extract_strict_schema, TICKET))