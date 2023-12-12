import json
from typing import Optional

from Blu.Utils.Utils import readMarkdownFile
from Blu.LLM.LLMConversation import LLMConvo
from Blu.OpenAI.OAIConvo import OAIConvo1_3_8
from Blu.Core.Information import InformationFragment
from abc import ABC

condenseFragmentCommand = readMarkdownFile(
	"/home/naitry/Dev/GAIT/Packages/Blu/resources/TextFragments/Commands/condenseFragment.md")
reflectCommand = readMarkdownFile("/home/naitry/Dev/GAIT/Packages/Blu/resources/TextFragments/Commands/selfReflect.md")
sayToCommand1 = readMarkdownFile("/home/naitry/Dev/GAIT/Packages/Blu/resources/TextFragments/Commands/sayTo.md")
sayToCommand2 = readMarkdownFile("/home/naitry/Dev/GAIT/Packages/Blu/resources/TextFragments/Commands/sayToPt2.md")
selfImageFunctionalDescription = readMarkdownFile(
	"/home/naitry/Dev/GAIT/Packages/Blu/resources/TextFragments/FunctionalDescriptions/selfImage.md")


class PersonaComponent(InformationFragment):
	def __init__(self,
				 body: str = "",
				 name: str = "",
				 functionalDescription: str = "",
				 embedding: list[float] = None):
		super().__init__(body=body,
						 embedding=embedding)
		self.name: str = name
		self.functionalDescription: str = functionalDescription


class Persona(ABC):
	def __init__(self,
				 convo: LLMConvo = OAIConvo1_3_8()):
		self.name: str = ""
		self.primaryInstruction: str = ""
		self.selfImage: PersonaComponent = PersonaComponent(functionalDescription=selfImageFunctionalDescription)
		self.unconsciousBody: PersonaComponent = PersonaComponent()
		self.thoughtRecord: list[InformationFragment] = []
		self.actionRecord: list[InformationFragment] = []
		self.convo: LLMConvo = convo
		self.thoughtDepth: int = 4
		self.freshThoughts: int = 0

	def loadFromFile(self,
					 file_path: str) -> None:
		with open(file_path, 'r', encoding='utf-8') as file:
			data = json.load(file)
			self.__dict__ = self.convertDictToObjects(data)

	def saveToFile(self,
				   file_path: str) -> None:
		with open(file_path, 'w', encoding='utf-8') as file:
			# Serialize a dict that excludes non-serializable attributes
			data_to_serialize = {k: v for k, v in self.__dict__.items() if k != 'client'}
			json.dump(data_to_serialize, file, default=self.custom_json_serializer, ensure_ascii=False, indent=4)

	def custom_json_serializer(self,
							   obj):
		if hasattr(obj, '__dict__'):
			# Return a dict that excludes non-serializable attributes
			return {k: v for k, v in obj.__dict__.items() if k != 'client'}
		elif isinstance(obj, bytes):
			return obj.decode('utf-8')
		else:
			return str(obj)

	def convertDictToObjects(self,
							 data: dict) -> dict:
		for key, value in data.items():
			if isinstance(value, dict):
				if key == "convo":
					# Properly instantiate the convo object
					# Assuming you have a method or logic to convert a dict to an LLMConvo object
					data[key] = self.convertDictToConvo(value)
				else:
					# Handle other dicts as PersonaComponent objects
					valid_keys = ['body', 'name', 'functionalDescription', 'embedding']
					filtered_value = {k: v for k, v in value.items() if k in valid_keys}
					data[key] = PersonaComponent(**filtered_value)
		return data

	def convertDictToConvo(self,
						   convo_data: dict) -> LLMConvo:
		convo = OAIConvo1_3_8()

		for message in convo_data.get("messages", []):
			role = message.get("role")
			content = message.get("content")

			if role == "system":
				convo.addSystemMessage(content)
			elif role == "user":
				convo.addUserMessage(content)
			elif role == "assistant":
				convo.addAssistantMessage(content)

		return convo

	def buildConvo(self):
		self.convo.clearMessages()
		self.convo.addSystemMessage("Your name is " + self.name)
		self.convo.addSystemMessage(self.primaryInstruction)
		self.convo.addSystemMessage("Your concept of self is:: " + self.selfImage.body)
		self.convo.addSystemMessage("Your recent record of thought is:: " + self.concatenateThoughts(self.thoughtDepth))

	def condenseFragment(self,
						 inputFragment: InformationFragment) -> InformationFragment:
		self.buildConvo()
		self.convo.addSystemMessage(condenseFragmentCommand)
		self.convo.addUserMessage(inputFragment.body)
		return InformationFragment(self.convo.requestResponse())

	def sayTo(self,
			  name: Optional[str] = None,
			  inputFragment: InformationFragment = InformationFragment()) -> InformationFragment:
		self.buildConvo()

		self.convo.addSystemMessage(sayToCommand1)
		userMessage: str = name + " says: " + inputFragment.body if name else "Someone says: " + inputFragment.body
		self.convo.addUserMessage(userMessage)
		self.actionRecord.append(InformationFragment(userMessage))
		responseThought: InformationFragment = InformationFragment(self.convo.requestResponse(addToConvo=True))

		self.thoughtRecord.append(responseThought)
		self.freshThoughts += 1
		thoughtAsAction: InformationFragment = InformationFragment("You think: " + responseThought.body)
		self.actionRecord.append(thoughtAsAction)

		self.convo.addSystemMessage(sayToCommand2)
		self.convo.addUserMessage("**RESPOND**")
		response: InformationFragment = InformationFragment(self.convo.requestResponse(addToConvo=True))
		responseAsAction: InformationFragment = InformationFragment("You say: " + response.body)
		self.actionRecord.append(responseAsAction)
		if self.freshThoughts >= 3:
			self.selfReflect()
		return response

	def selfReflect(self) -> None:
		self.buildConvo()
		self.convo.addSystemMessage(reflectCommand)
		self.convo.addUserMessage(self.selfImage.body)
		self.selfImage.body = self.convo.requestResponse()
		self.freshThoughts = 0

	def concatenateThoughts(self, depth: int) -> str:
		last_n_thoughts = self.thoughtRecord[-depth:] if len(self.thoughtRecord) >= depth else self.thoughtRecord

		return '\n'.join(fragment.body for fragment in last_n_thoughts)
