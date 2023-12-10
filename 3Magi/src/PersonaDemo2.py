from Blu.Core.Persona import Persona
from Blu.Core.Information import InformationFragment

john: Persona = Persona()
john.loadFromFile("../markdown/personalities/john.md")

originalFragment: str ="Farming chickens involves various aspects that contribute to the health and productivity of the chickens."

print(originalFragment)
print(john.condenseFragment(InformationFragment(originalFragment)).body)