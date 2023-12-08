from typing import Optional
import openai
import LLMConversation
from openai import OpenAI

key: str = LLMConversation.readMarkdownFile("../markdown/key.md")
key = key.strip()

client: openai.OpenAI = OpenAI(api_key=key)

class StringEmbedding:
	def __init__(self,
				 inputString: Optional[str],
				 ):
		self.inputString: str = inputString
		self.

	def retrieveEmbedding(self):



responses: list[openai.types.CreateEmbeddingResponse] = []

responses.append(client.embeddings.create(
	input="Tyler Steffen",
	model="text-embedding-ada-002"
))

responses.append(client.embeddings.create(
	input="Tyler Steffen",
	model="text-embedding-ada-002"
))


for response in responses:
	print(response.data[0].embedding)
	print(response)
	print("Length: " + str(len(response.data[0].embedding)))
