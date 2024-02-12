from Blu.Core.Persona import Persona
from Blu.Utils.Utils import readMarkdownFile
magi: Persona = Persona()

primaryMagi = readMarkdownFile("/Blu/Core/TextFragments/Commands/primaryMagi.md")
magiImageBase = readMarkdownFile("/Blu/Core/TextFragments/PersonaFragments/MagiImageBases/CasparImageBase001.md")

magi.name = "Caspar"
magi.selfImage.body = magiImageBase
magi.primaryInstruction = primaryMagi


magi.saveToFile("../markdown/personalities/" + magi.name + ".md")