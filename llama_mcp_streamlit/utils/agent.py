import json
from typing import List
from openai import AsyncOpenAI
from config import DEFAULT_MODEL_ID, SYSTEM_PROMPT

async def agent_loop(query: str, tools: dict, client: AsyncOpenAI, messages: List[dict] = None, model: str = DEFAULT_MODEL_ID):
    messages = (
        [
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(
                    tools="\n- ".join(
                        [
                            f"{t['name']}: {t['schema']['function']['description']}"
                            for t in tools.values()
                        ]
                    )
                ),
            },
            {"role": "user", "content": query},
        ]
        if messages is None
        else messages
    )

    first_response = await client.chat.completions.create(
        model=model,
        messages=messages,
        tools=([t["schema"] for t in tools.values()] if len(tools) > 0 else None),
        max_tokens=4096,
        temperature=0,
    )

    stop_reason = (
        "tool_calls"
        if first_response.choices[0].message.tool_calls is not None
        else first_response.choices[0].finish_reason
    )

    if stop_reason == "tool_calls":
        for tool_call in first_response.choices[0].message.tool_calls:
            arguments = (
                json.loads(tool_call.function.arguments)
                if isinstance(tool_call.function.arguments, str)
                else tool_call.function.arguments
            )
            tool_result = await tools[tool_call.function.name]["callable"](**arguments)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": json.dumps(tool_result),
                }
            )

        new_response = await client.chat.completions.create(
            model=model,
            messages=messages,
        )

    elif stop_reason == "stop":
        new_response = first_response

    else:
        raise ValueError(f"Unknown stop reason: {stop_reason}")

    messages.append(
        {"role": "assistant", "content": new_response.choices[0].message.content}
    )

    return new_response.choices[0].message.content, messages