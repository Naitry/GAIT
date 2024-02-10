from Blu.Core.Persona import Persona
from Blu.Utils.Utils import readMarkdownFile
magi: Persona = Persona()

primaryMagi = readMarkdownFile("/home/naitry/Dev/GAIT/Packages/Blu/resources/TextFragments/Commands/primaryMagi.md")
magiImageBase = readMarkdownFile("/home/naitry/Dev/GAIT/Packages/Blu/resources/TextFragments/PersonaFragments/MagiImageBases/CasparImageBase001.md")

magi.name = "Caspar"
magi.selfImage.body = magiImageBase
magi.primaryInstruction = primaryMagi


magi.saveToFile("../markdown/personalities/" + magi.name + ".md")