from __future__ import annotations

from abc import ABC
import openai


class InformationFragment(ABC):
	def __init__(self,
				 body: str = "",
				 name: str = None,
				 embedding: list[float] = None,
				 details: list[InformationFragment] = None):
		self.body: str = body
		self.name: str = name
		self.embedding: list[float] = embedding if embedding is not None else []
		self.details: list[InformationFragment] = details

	def embed(self,
			  client: openai.OpenAI):
		self.embedding = client.embeddings.create(
			input=self.body,
			model="text-embedding-ada-002"
		).data[0].embedding
