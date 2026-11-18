import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER_URL = os.environ.get("LLM_PROVIDER_URL")
LLM_PROVIDER_KEY = os.environ.get("LLM_PROVIDER_KEY")
LLM_MODEL = os.environ.get("LLM_MODEL")

if not LLM_PROVIDER_KEY or not LLM_PROVIDER_URL or not LLM_MODEL:
    raise RuntimeError("One or more required environment variables are empty: set them in .env")

def chat(
    model: str, 
    system_prompt: str, 
    user_prompt: str,
    **params
) -> dict:
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        **params
    }

    headers = {
        "Authorization": f"Bearer {LLM_PROVIDER_KEY}"
    }

    response = httpx.post(
        LLM_PROVIDER_URL,
        json=payload,
        headers=headers,
        timeout=60
    )
    response.raise_for_status()
    return response.json()

def chat_stream(
    model: str,
    system_prompt: str,
    user_prompt: str
) -> dict | None:
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            },
        ],
        "stream": True,
    }

    headers = {
        "Authorization": f"Bearer {LLM_PROVIDER_KEY}"
    }

    with httpx.stream(
        "POST",
        LLM_PROVIDER_URL,
        json=payload,
        headers=headers,
        timeout=60
    ) as response:
        response.raise_for_status()
        usage = None
        for line in response.iter_lines():
            if not line.startswith("data: "):
                continue
            data = line[len("data: "):]
            if data == "[DONE]":
                break
            chunk = json.loads(data)
            if chunk.get("usage"):
                usage = chunk["usage"]
            for choice in chunk["choices"]:
                text = choice["delta"].get("content")
                if text:
                    print(text, end="", flush=True)
        print()
        return usage

if __name__ == "__main__":
    body = chat(
        model=LLM_MODEL,
        system_prompt="Response with one phrase.",
        user_prompt="What is a token in LLM context?",
        temperature=0
    )

    print(json.dumps(body, indent=2, ensure_ascii=False))
    print("\nResponse:", body["choices"][0]["message"]["content"])
    print("Usage:", body["usage"])

    print("\n --- stream ---")
    usage = chat_stream(
        model=LLM_MODEL,
        system_prompt="Response with one phrase.",
        user_prompt="What is a token in LLM context?"
    )
    print("Usage: ", usage)