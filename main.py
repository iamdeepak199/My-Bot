import pyautogui
import json
from os import path, system
from sys import exit, platform
from logtool import logAppend
from abc import ABC, abstractmethod


class AbstractBot(ABC):
    DIRECTORY = path.dirname(__file__)
    JSONNAME = path.join(DIRECTORY, 'data.json')
    
    def __init__(self, name):
        self.name = name
        self._data = self.load()
        
    def save(self):
        with open(AbstractBot.JSONNAME, 'w') as file:
            json.dump(self._data, file, ensure_ascii=False, indent=2)

    def load(self):
        if not path.isfile(AbstractBot.JSONNAME):
            return {}

        with open(AbstractBot.JSONNAME, 'r') as file:
            return json.load(file)
    
    @abstractmethod
    def talk(self, talk): ...


class Bot(AbstractBot):

    def talk(self, talk):
        if platform == 'win32':
            COMMANDS = {
                'open for me': lambda: self.open_app(input(f"{self.name}: What do you want me to open?\nAnswer here: ")),
                'open for me?': lambda: self.open_app(input(f"{self.name}: What do you want me to open?\nAnswer here: ")),
                'disconnect': lambda: exit(0)   # type: ignore
            }

            if COMMANDS.get(talk.lower()) is not None:
                return f"{self.name}: {COMMANDS.get(talk.lower())()}" # type: ignore

        if self._data.get(talk.lower()) is not None:
            return f"{self.name}: {self._data.get(talk.lower())}"
            

        print(f"{self.name}: I don't know this expression yet, can you teach me?")
        while True:
            answer = input("answer here: ").lower()

            if answer in ['no', 'not', 'non', 'nay', 'nope']:
                return f"{self.name}: Sorry, just wanted to learn!"

            if answer in ['yes','yea','yep']:
                system('clear')  # type: ignore
                print(f'{self.name}: What do you expect me to answer?')
                learning = input("answer here: ")
                self._data.setdefault(talk.lower(), learning)
                self.save()
                system('clear')  # type: ignore
                return f'{self.name}: Thank you for teaching me!'

            system('clear')  # type: ignore
            print(f"{self.name}: I did not understand your answer. Will you teach me?")

    if platform == 'win32':
        def open_app(self, command) -> str:
            pyautogui.PAUSE = 1
            with pyautogui.hold('win'):
                pyautogui.press('r')
            pyautogui.write(command)
            pyautogui.press('Enter')

            return "It's opening"


bot1 = Bot('My Bot')
while True:
    talk = input("Answer here: ")
    logAppend(f'User: {talk}')
    system('clear')
    print(bot1.talk(talk))
    logAppend(bot1.talk(talk))