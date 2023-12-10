import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any

import openai
from openai import OpenAI

from Blu.LLM.LLMConversation import LLMConvo
from Blu.Utils.Utils import readMarkdownFile


class OAIConvo1_3_8(LLMConvo):
    def __init__(self) -> None:
        super().__init__()
        key: str = readMarkdownFile("/home/naitry/Dev/GAIT/3Magi/markdown/key.md")
        # print("key: " + key)
        self.client: openai.Client = OpenAI(api_key=key)

    def addSystemMessage(self,
                         message: str) -> None:
        self.messages.append({
            "role": "system",
            "content": message,
            "DT": super().currentDateTime()
        })

    def addAssistantMessage(self,
                            message: str) -> None:
        self.messages.append({
            "role": "assistant",
            "content": message,
            "DT": super().currentDateTime()
        })

    def addUserMessage(self,
                       message: str) -> None:
        self.messages.append({
            "role": "user",
            "content": message,
            "DT": super().currentDateTime()
        })

    def formattedMessages(self) -> List[Dict[str, str]]:
        return [{"role": msg["role"], "content": msg["content"]} for msg in self.messages]

    def requestResponse(self,
                        addToConvo: bool = False) -> str:
        response: Any = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.formattedMessages(),
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        assistantMessage = response.choices[0].message.content
        if addToConvo:
            self.addAssistantMessage(assistantMessage)
        return assistantMessage
