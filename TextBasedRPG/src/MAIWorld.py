from MAICard import CardType
import MAICard
from typing import List, Optional
from LLMConversation import LLMConvo
from LLMConversation import readMarkdownFile

class MAIWorld:
    def __init__(self):
        self.name: str = ""
        self.userDescription: str = ""
        self.gptDescription: str = ""
        self.Lands: List[MAICard.LandCard] = []
        self.numLands: int = 5

    def generateGPTDescription(self) -> str:
        generationConvo: LLMConvo = LLMConvo()
        generationConvo.addSystemMessage(readMarkdownFile("../Prompts/MAIWorldPrompts/MAIGenerateWorld.md"))

        generationConvo.addUserMessage(self.userDescription)

        self.gptDescription = generationConvo.requestResponse()
        return self.gptDescription

    def generateImagePrompt(self) -> str:



    def generateLandCards(self) -> None:
        # Loop 5 times
        for i in range(5):
            response: str
            parsedCard: Optional[MAICard.LandCard]  # Assuming MAICard.parseLandCard returns Optional[LandCard]

            # Generate CREATE_BYOME input based on previously parsed cards
            if not self.Lands:
                byome_input = "[CREATE_BYOME]{No lands defined}"
            else:
                descriptors = MAICard.landCardDescriptorList(self.Lands)
                byome_input = "[CREATE_BYOME]{(" + ",".join(descriptors) + ")}"

            while True:
                # Replace chatWithGPT with your actual function call
                conversation.addUserMessage(byome_input)
                response = conversation.requestResponse()

                parsedCard = MAICard.parseLandCard(response)  # Replace with your parsing function if different
                if parsedCard:
                    print("Successfully parsed the Land Card!")
                    # parsedCard.display()
                    break  # Exit the loop
                else:
                    print("Parsing failed. Please try again.")