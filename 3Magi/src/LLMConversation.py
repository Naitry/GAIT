from typing import Any, Dict, List
from typing import Optional
from openai import OpenAI
from Utils import readMarkdownFile

key: string = readMarkdownFile("../markdown/key.md")
os.environ["OPENAI_API_KEY"] = key

myVar = os.environ.get("OPENAI_API_KEYi")
print(myVar)  # Outputs: value

client = OpenAI()

class LLMConvo:
    def __init__(self) -> None:
        self.messages: List[Dict[str, str]] = []

    def addSystemMessage(self, message: str):
        self.messages.append({
            "role": "system",
            "content": message
        })

    def addAssistantMessage(self, message: str):
        self.messages.append({
            "role": "assistant",
            "content": message
        })

    def addUserMessage(self, message: str):
        self.messages.append({
            "role": "user",
            "content": message
        })

    def requestResponse(self, addToConvo: bool = False) -> str:
        response: Any = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        assistantMessage = response['choices'][0]['message']['content']
        if addToConvo:
            self.addAssistantMessage(assistantMessage)
        return assistantMessage
