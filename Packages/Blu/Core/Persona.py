import json
from Blu.Utils.Utils import readMarkdownFile
from Blu.LLM.LLMConversation import LLMConvo
from Blu.OpenAI.OAIConvo import OAIConvo1_3_8
from Blu.Core.Information import InformationFragment
from abc import ABC

condenseFragmentCommand = readMarkdownFile("../resources/")
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
		self.selfImage: PersonaComponent = PersonaComponent()
		self.unconsciousBody: PersonaComponent = PersonaComponent()
		self.thoughtRecord: list[InformationFragment] = []
		self.convo = convo

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
		self.convo.addSystemMessage("Your recent record of thought is:: " + self.concentrateThought())

	def condenseFragment(self,
						 inputFragment: InformationFragment) -> InformationFragment:
		self.buildConvo()
		self.convo.addSystemMessage(condenseFragmentCommand)
		self.convo.addUserMessage(inputFragment.body)
		return InformationFragment(self.convo.requestResponse())

	def concentrateThought(self) -> str:
		return '\n'.join(fragment.body for fragment in self.thoughtRecord)
