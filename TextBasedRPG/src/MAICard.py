from enum import Enum
from typing import Dict, Any, List, Union, Optional
import json
from LLMConversation import LLMConvo
from LLMConversation import readMarkdownFile
from PIL import Image
from MAIImageGeneration import generateSDXLImage

class CardType(Enum):
    """Enum for card types."""
    CREATURE = "Creature"
    LAND = "Land"
    SPELL = "Spell"
    INSTANT = "Instant"


class MAICard:
    """Base class for MAI cards."""

    def __init__(self,
                 name: str,
                 cardType: CardType) -> None:
        self.name: str = name
        self.cardType: CardType = cardType

    def toString(self) -> str:
        """Display card details."""
        return f"Name: {self.name}, Type: {self.cardType.value}"


class CreatureCard(MAICard):
    """Derived class for creature cards."""

    def __init__(self,
                 name: str,
                 power: int,
                 toughness: int) -> None:
        super().__init__(name,
                         CardType.CREATURE)
        self.power = power
        self.toughness = toughness

    def toString(self) -> str:
        """Override to display creature details."""
        return f"Name: {self.name}, Type: {self.cardType.value}, Power: {self.power}, Toughness: {self.toughness}"


class SpellCard(MAICard):
    """Derived class for spell cards."""

    def __init__(self,
                 name: str,
                 effect: str) -> None:
        super().__init__(name,
                         CardType.SPELL)
        self.effect = effect

    def toString(self) -> str:
        """Override to display spell details."""
        return f"Name: {self.name}, Type: {self.cardType.value}, Effect: {self.effect}"


class LandCard:
    """Class to represent a Land card in Magic: The Gathering."""

    def __init__(self,
                 name: str,
                 color: str,
                 resource: str,
                 description: str) -> None:
        self.name: str = name
        self.color: str = color
        self.resource: str = resource
        self.description: str = description
        self.cardType: CardType = CardType.LAND
        self.imageString: str = ''
        self.image: Image = None

    def display(self) -> None:
        """Display the details of the Land card."""
        print(f"Name: {self.name}, Type: {self.cardType.value}, Color: {self.color}, Resource: {self.resource}")
        print(f"Description: {self.description}")

    def toDict(self) -> Dict[str, str]:
        """
        Convert the LandCard object to a dictionary.

        :return: Dictionary representation of the LandCard object.
        """
        return {
            "name": self.name,
            "color": self.color,
            "resource": self.resource,
            "description": self.description,
            "card_type": "LAND"
        }

    def landCardToJson(self) -> str:
        """
        Converts a LandCard object to a JSON-formatted string.

        :return: A JSON-formatted string representing the LandCard object.
        """
        landCardDict = self.toDict()
        jsonString = json.dumps(landCardDict, indent=4)
        return jsonString

    def generateImageString(self, worldDescription: str):
        generationConvo: LLMConvo = LLMConvo()

        generationConvo.addSystemMessage(readMarkdownFile("../Prompts/WorldPrompts/LandPrompts/LandToImagePrompt.md") +
                                         worldDescription)

        generationConvo.addUserMessage(self.landCardToJson())

        self.imageString = cutStringToLength(generationConvo.requestResponse(), 70) + "--style Fine Art, Painted, Color, Intricate"
        return self.imageString

    def generateImage(self) -> Image:
        return generateSDXLImage(self.imageString)



def parseLandCard(data: Union[str, Dict[str, Any]]) -> Optional[LandCard]:
    """Parse a dictionary or JSON string into a LandCard object.

    Parameters:
        data (Union[str, Dict[str, Any]]): Dictionary or JSON string containing the Land card details.

    Returns:
        Optional[LandCard]: The parsed LandCard object or None if parsing failed.
    """
    try:
        if isinstance(data,
                      str):
            data = json.loads(data)

        return LandCard(
            name=data["Name"],
            color=data["Color"],
            resource=data["Resource"],
            description=data["Description"]
        )
    except (json.JSONDecodeError, KeyError):
        print("Failed to parse land card. Please try again.")
        return None


def cutStringToLength(inputStr: str, numWords: int) -> Optional[str]:
    """
    Cut the input string to a certain number of words.

    :param input_str: The input string to be cut.
    :param num_words: The number of words to keep.
    :return: The resulting string with only `num_words` words, or None if `input_str` is empty.
    """
    if not inputStr:
        return None

    words = inputStr.split()

    if len(words) <= numWords:
        return inputStr

    return ' '.join(words[:numWords])
def landCardDescriptorList(land_cards: List[Optional[LandCard]]) -> List[str]:
    """Generate a list of basic descriptors for each LandCard object.

    Parameters:
        land_cards (List[Optional[LandCard]]): A list of LandCard objects or None.

    Returns:
        List[str]: A list of basic descriptors for each LandCard.
    """
    descriptors = []
    for card in land_cards:
        if card:
            descriptor = f"({card.name}:{card.color}:{card.resource})"
            descriptors.append(descriptor)
    return descriptors
