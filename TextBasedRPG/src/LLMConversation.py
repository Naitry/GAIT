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
        # openai.api_key = "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"
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

    def requestResponse(self) -> str:
        response: Any = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=self.messages,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        assistantMessage = response['choices'][0]['message']['content']
        self.addAssistantMessage(assistantMessage)
        return assistantMessage



def chatWithGPT(conversation: List[Dict[str, str]], newMessage: str) -> str:
    """
    A function to continue a conversation with GPT-3.5 Turbo.

    Args:
        conversation (List[Dict[str, str]]): Existing conversation messages.
        newMessage (str): New message from the user to add to the conversation.

    Returns:
        str: The GPT-3.5 Turbo response.
    """
    # Append the new user message to the conversation
    conversation.append({
        "role": "user",
        "content": newMessage
    })

    # Make the API call
    response: Any = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the assistant's message and add it to the conversation
    assistantMessage = response['choices'][0]['message']['content']
    conversation.append({
        "role": "assistant",
        "content": assistantMessage
    })

    return assistantMessage


# Initialize the conversation
initialConversation = [
    {
        "role": "system",
        "content": readMarkdownFile("../prompts/MAIInit1.md")
    }
]
