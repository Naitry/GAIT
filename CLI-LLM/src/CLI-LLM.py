# Typing
from typing import Dict
from enum import Enum

# Blu
from Blu.Core.Persona import Persona
from Blu.Color.TermColor import printC, paintStr, setColor


class AppState(Enum):
	STARTUP = 1
	STANDARD = 2


promptStrings: Dict[AppState, str] = {AppState.STANDARD: "please input the ", }


def main():
	running: bool = True
	state: AppState = AppState.STANDARD
	magi: Persona

	while running:
		match state:
			case AppState.STARTUP:
				setColor("sky blue")
				print("Select an existing persona or create a new one:")


				userResponse: str = input()
				pass
			case AppState.STANDARD:
				pass
			case _:
				pass


def processInput(string: str) -> str:


if __name__ == "__main__":
	main()
