from typing import Any, Dict, List
from typing import Optional
from LLMConversation import readMarkdownFile
from openai import OpenAI
import openai
import subprocess
import time
scriptPath:str = '../shell/setAPI.sh'

subprocess.call(f'source {scriptPath}', shell=True, executable='/bin/bash')

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

print(run)

time.sleep(10)

messages: List[openai.beta.threads.messages] = client.beta.threads.messages.list(
  thread_id=thread.id
)

print()
print(len(list(messages)))

for m in messages:
    print()
    print(m)
