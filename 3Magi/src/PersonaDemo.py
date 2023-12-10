from Blu.Core.Persona import Persona
from Blu.Core.Information import InformationFragment

john: Persona = Persona()

john.name = "john"
john.selfImage.body = "a good ole farmer boy"
john.primaryInstruction = "You are a sentient being and your goal is to respond and develop accordingly. You have a concept of self which should drive a great deal of how you behave"

originalFragment: str ="Farming chickens involves various aspects that contribute to the health and productivity of the chickens."

print(originalFragment)
print(john.condenseFragment(InformationFragment(originalFragment)).body)

john.saveToFile("../markdown/personalities/john.md")