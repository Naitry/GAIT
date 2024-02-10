from typing import Dict
import Blu.OpenAI.OAIConvo as convo
from enum import Enum
from Blu.Core.Persona import Persona
from Blu.Core.Information import InformationFragment


class AppState(Enum):
	STANDARD = "standard"


promptStrings: Dict[AppState, str] = {
	AppState.STANDARD: "please input the ", }


def main():
	running: bool = True
	state: AppState = AppState.STANDARD
	welcomeText: str = ""
	magi: Persona = Persona()

	magi.loadFromFile()

	while running:
		userInput = input("")
		pass


if __name__ == "__main__":
	main()