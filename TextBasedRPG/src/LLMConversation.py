from typing import Any, Dict, List
from typing import Optional
import openai


def readMarkdownFile(filePath: str) -> Optional[str]:
    """
  Reads the content of a Markdown file and returns it as a single string.

  Args:
      filePath (str): The path to the Markdown file.

  Returns:
      Optional[str]: The content of the Markdown file as a single string, or None if the file could not be read.
  """
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            content: str = file.read()
        return content
    except FileNotFoundError:
        print(f"File {filePath} not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


class LLMConvo:
    def __init__(self) -> None:
        openai.api_key = "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"
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
        response: Any = openai.ChatCompletion.create(
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
