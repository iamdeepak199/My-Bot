import pyautogui
import json
from os import path, system
from sys import exit, platform
from logtool import logAppend
from abc import ABC, abstractmethod
import speech_recognition as sr

def speech() -> str:
    r = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as mic:
        audio = r.listen(mic)
        track = r.recognize_google(audio, language="pt-BR")
        clear()
        return track   # type: ignore


def clear():
    match platform:
        case 'win32' | 'cygwin':
            return system('cls')
        case _:
            return clear()

class AbstractBot(ABC):
    DIRECTORY = path.dirname(__file__)
    JSONNAME = path.join(DIRECTORY, 'data.json')
    
    def __init__(self, name):
        self.name = name
        self._data = self.load()
        
    def save(self):
        with open(AbstractBot.JSONNAME, 'w') as file:
            json.dump(self._data, file, indent=2)

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
            while True:
                try:
                    answer = speech()
                    clear()
                    break
                except sr.UnknownValueError:
                    print(f"{self.name}: I don't know this expression yet, can you teach me?")
                    continue

            if answer in ['no', 'not', 'non', 'nay', 'nope', 'não']:
                return f"{self.name}: Sorry, just wanted to learn!"

            if answer in ['yes','yea','yep', 'sim', 'ok']:
                clear()
                print(f'{self.name}: What do you expect me to answer?')
                while True:
                    try:
                        learning = speech()
                        clear()
                        break
                    except sr.UnknownValueError:
                        print(f'{self.name}: What do you expect me to answer?')
                        continue
                self._data.setdefault(talk.lower(), learning)
                self.save()
                clear()
                return f'{self.name}: Thank you for teaching me!'

            clear()
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
    print('Fale...')
    while True:
        try:
            talk = speech()
            clear()
            break
        except sr.UnknownValueError:
            print('Fale...')
            continue
    logAppend(f'User: {talk}')
    clear()
    print(bot1.talk(talk))
    logAppend(bot1.talk(talk))