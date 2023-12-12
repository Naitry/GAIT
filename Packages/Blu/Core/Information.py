from abc import ABC

import openai


class InformationFragment(ABC):
	def __init__(self,
				 body: str = "",
				 embedding: list[float] = None):
		self.body: str = body
		self.embedding = embedding if embedding is not None else []
		pass

	def embed(self,
			  client: openai.OpenAI):
		self.embedding = client.embeddings.create(
			input=self.body,
			model="text-embedding-ada-002"
		).data[0].embedding
