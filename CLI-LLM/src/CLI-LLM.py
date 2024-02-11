# Typing
from typing import Dict
from enum import Enum

# Blu
from Blu.Core.Persona import Persona


class AppState(Enum):
	STARTUP = 1
	STANDARD = 2

promptStrings: Dict[AppState, str] = {
	AppState.STANDARD: "please input the ", }


def main():
	running: bool = True
	state: AppState = AppState.STANDARD
	magi: Persona

	while running:
		match state:
			case AppState.STARTUP:

				pass
			case AppState.STANDARD:
				pass
			case _:
				pass

if __name__ == "__main__":
	main()
