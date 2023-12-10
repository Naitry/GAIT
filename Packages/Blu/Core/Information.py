from abc import ABC


class InformationFragment(ABC):
	def __init__(self,
				 body: str = "",
                 embedding: list[float] = None):
		self.body: str = body
		self.embedding = embedding if embedding is not None else []
		pass
