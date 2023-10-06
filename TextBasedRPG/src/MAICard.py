from enum import Enum
from typing import Dict, Any, List, Union, Optional
import json


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
        self.name = name
        self.color = color
        self.resource = resource
        self.description = description
        self.card_type = CardType.LAND

    def display(self) -> None:
        """Display the details of the Land card."""
        print(f"Name: {self.name}, Type: {self.card_type.value}, Color: {self.color}, Resource: {self.resource}")
        print(f"Description: {self.description}")


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
