from MAICard import CardType
import MAICard
from typing import List, Optional
from LLMConversation import LLMConvo
from LLMConversation import readMarkdownFile


class MAIWorld:
    def __init__(self, description: str = ""):
        self.name: str = ""
        self.userDescription: str = description
        self.gptDescription: str = ""
        self.Lands: List[MAICard.LandCard] = []
        self.numLands: int = 5

    def generateGPTDescription(self) -> str:
        generationConvo: LLMConvo = LLMConvo()
        generationConvo.addSystemMessage(readMarkdownFile("../Prompts/WorldPrompts/GenerateWorld.md"))

        generationConvo.addUserMessage(self.userDescription)

        self.gptDescription = generationConvo.requestResponse()
        return self.gptDescription

    def generateImagePrompt(self) -> str:
        generationConvo: LLMConvo = LLMConvo()
        generationConvo.addSystemMessage(readMarkdownFile("../Prompts/WorldPrompts/WorldToImagePrompt.md"))

        generationConvo.addUserMessage(self.userDescription)

        self.gptDescription = generationConvo.requestResponse()
        return self.gptDescription

    def generateLandCard(self) -> MAICard.LandCard:
        print("generating land card")
        response: str
        parsedCard: Optional[MAICard.LandCard]  # Assuming MAICard.parseLandCard returns Optional[LandCard]

        generationConvo: LLMConvo = LLMConvo()
        prompt: str = readMarkdownFile("../Prompts/WorldPrompts/LandPrompts/GenerateLand.md") + self.gptDescription

        if self.Lands:
            prompt += "\n The following land cards have already been defined, make sure not to create something which " \
                      "overlaps in theme or color \n"

            for land in self.Lands:
                prompt += land.landCardToJson() + "\n"

        generationConvo.addSystemMessage(prompt)
        generationConvo.addUserMessage("[CREATE_LAND]")

        while True:
            response = generationConvo.requestResponse()

            parsedCard = MAICard.parseLandCard(response)  # Replace with your parsing function if different
            if parsedCard:
                print("Successfully parsed the Land Card!")
                # parsedCard.display()
                break  # Exit the loop
            else:
                print("Parsing failed. Please try again.")
                print("failed parse:: " + response)

        self.Lands.append(parsedCard)
        return parsedCard


world: MAIWorld = MAIWorld("Mobile Suit Gundam: Universal Century Timeline")
world.generateGPTDescription()

for i in range(5):
    card: MAICard.LandCard = world.generateLandCard()
    print(card.generateImageString(world.gptDescription))
    (card.generateImage()).show()
