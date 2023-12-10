from typing import Optional, List
import openai
from openai import OpenAI
import torch


key: str = LLMConversation.readMarkdownFile("../markdown/key.md")
key = key.strip()

Client: openai.OpenAI = OpenAI(api_key=key)


class StringEmbedding:
    def __init__(self,
                 inputString: Optional[str]):
        self.inputString: str = inputString
        self.embeddingVector: List[float] = []

    def retrieveEmbedding(self,
                          client: openai.OpenAI):
        self.embeddingVector = client.embeddings.create(
            input="Tyler Steffen",
            model="text-embedding-ada-002"
        ).data[0].embedding

    def printEmbedding(self):
        print(self.embeddingVector)
        print("Length: " + str(len(self.embeddingVector)))
        print("Max: " + str(max(self.embeddingVector)))
        print("Min: " + str(min(self.embeddingVector)))



embedding: StringEmbedding = StringEmbedding(inputString="Tyler Steffen")
embedding.retrieveEmbedding(client=Client)
embedding.printEmbedding()





def normalize_vectors(vectors):
    """ Normalize a batch of vectors to unit length using PyTorch. """
    norms = torch.norm(vectors, p=2, dim=1, keepdim=True)
    return vectors / norms

def apca_reduction_torch(vectors, n_components=3):
    """
    Apply Angular PCA using PyTorch to reduce vectors to n_components dimensions.

    Args:
        vectors (torch.Tensor): A tensor of shape (n_samples, n_features).
        n_components (int): The number of components to keep.

    Returns:
        torch.Tensor: A tensor of shape (n_samples, n_components).
    """
    # Normalize the vectors
    normalized_vectors = normalize_vectors(vectors)
    # Compute SVD
    U, S, V = torch.linalg.svd(normalized_vectors, full_matrices=False)
    # Select the top n_components
    return torch.matmul(normalized_vectors, V[:, :n_components])