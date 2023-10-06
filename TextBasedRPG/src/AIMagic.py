import os
import openai
from typing import Any, Dict, List

openai.api_key = "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"

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
        model="gpt-3.5-turbo",
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
        "content": "You are a source of creative story for an RPG (Role Playing Game). You will act as the dungeon master. Any fourth wall-breaking (outside the game world) instructions for you will be given to you in curly brackets {}. Every location and room should have a description of at least a paragraph. Ensure a consistent game world; characters, locations, and items should have a constant, unchanging description, unless it makes sense for them to change.\n"
    }
]

# First interaction
response1 = chatWithGPT(initialConversation, "I enter the tavern. What do I see?")
print("First response:", response1)

# Second interaction
response2 = chatWithGPT(initialConversation, "I approach the bartender. What's his appearance?")
print("Second response:", response2)

# The conversation can be continued in the same manner
