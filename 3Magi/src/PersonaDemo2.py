from Blu.Core.Persona import Persona
from Blu.Core.Information import InformationFragment

magi: Persona = Persona()
magi.loadFromFile("../markdown/personalities/Caspar.md")

questionList = [
    "Hi there! How's your day going?",
    "By the way, I didn't catch your name. What is it?",
    "I'm curious, what's your take on the latest happenings around the world?",
    "When you're faced with a new problem, how do you tackle it?",
    "What is your name?"
]


for question in questionList:
    print(magi.sayTo(name="Tyler", inputFragment=InformationFragment(question)).body)

magi.saveToFile("../markdown/personalities/CasparOut2_GPT4.md")