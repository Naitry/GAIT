from typing import Any, Dict, List
from typing import Optional
from Utils import readMarkdownFile
from openai import OpenAI
import openai
import time
import os

key:str = readMarkdownFile("../markdown/key.md")

print(key)

os.environ["OPENAI_API_KEY"] = key

myVar = os.environ.get("OPENAI_API_KEY")
print(myVar)  # Outputs: value

client = OpenAI()

assistant = client.beta.assistants.create(
        name="Balthazar",
        instructions=readMarkdownFile("../markdown/personalities/melchior.md"),
        tools=[{
            "type": "function",
            "function": {
                "name": "makeDecision",
                "description": "Forces the AI to make a yes no choice on the situation at hand.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "decision": {"type": "boolean",
                                     "description": "The answer to the decision, true for yes, false for no."},
                        "confidence": {"type": "number",
                                       "minimum": 0,
                                       "maximum": 1,
                                       "description": "Floating point confidence value of the decision, 1 for totally confident, 0 for not confident at all, and all percentage values inbetween"},
                        "reasoning": {
                            "type": "string",
                            "description": "The justification as to why the decision was made."}
                        },
                    "required": [
                        "decision"
                        ]
                    }
                }
            }],
        model="gpt-4-1106-preview")

thread: openai.beta.threads = client.beta.threads.create()

message: openai.beta.threads.messages = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=readMarkdownFile("../markdown/testPrompts/decisionProblems/decisionProblem1.md")
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="make a decision on the given problem"
)

while run.status != "requires_action":
    run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
            )
    time.sleep(1)
    print("waiting")
    print(run.status)

print(run.required_action)

run  = client.beta.threads.runs.submit_tool_outputs(
  thread_id=thread.id,
  run_id=run.id,
  tool_outputs=[
      {
        "tool_call_id": run.required_action.submit_tool_outputs.tool_calls[0].id,
        "output": True,
      },
    ]
)

run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
            )
time.sleep(1)
print(run.status)

while run.status != "requires_action":
    run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
            )
    time.sleep(1)
    print("waiting")
    print(run.status)

messages: List[openai.beta.threads.messages] = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(len(list(messages)))

for m in messages:
    print()
    print(m)
