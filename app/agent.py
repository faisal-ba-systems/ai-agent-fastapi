import json
import os
from groq import Groq
from dotenv import load_dotenv
from app.tools import TOOL_SCHEMAS, execute_tool

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = (
    "You are a helpful AI automation agent. You have tools to read/write files, "
    "run shell commands, and fetch web pages. Think step by step. Use tools when "
    "needed. When the task is complete, give a clear final answer."
)


def run_agent(task: str, max_iterations: int = 10) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task},
    ]

    tool_calls_made = []

    for iteration in range(1, max_iterations + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        # No tool calls means the agent has a final answer
        if not message.tool_calls:
            return {
                "result": message.content or "",
                "iterations": iteration,
                "tool_calls_made": tool_calls_made,
            }

        # Add assistant turn (with tool calls) to history
        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in message.tool_calls
            ],
        })

        # Execute each tool and feed results back
        for tc in message.tool_calls:
            tool_name = tc.function.name
            tool_args = json.loads(tc.function.arguments)

            print(f"  [Tool] {tool_name}({tool_args})")
            result = execute_tool(tool_name, tool_args)
            tool_calls_made.append(f"{tool_name}({tool_args})")

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result,
            })

    return {
        "result": "Agent stopped: max iterations reached without a final answer.",
        "iterations": max_iterations,
        "tool_calls_made": tool_calls_made,
    }
