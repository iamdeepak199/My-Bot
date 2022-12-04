
class Bot:
    import json as json
    from os import path as path

    DIRECTORY = path.dirname(__file__)
    COMANDS = {
        'save': lambda: bot1.save(),
        'save the json': lambda: bot1.save(),
        'save, please': lambda: bot1.save(),
    }

    def __init__(self, name):
        self.name = name
        self.data = {
            'hello': f"{self.name}: Hi, I'am {self.name}!",
            'hi': f"{self.name}: Hi, I'am {self.name}!",
        }


    def talk(self, talk):
        if Bot.COMANDS.get(talk.lower()) is not None:
            return Bot.COMANDS[talk]()

        if self.data.get(talk.lower()) is not None:
            return self.data[talk]
            

        print(f"{self.name}: I don't know this expression yet, can you teach me?")
        answer = input("answer here: ").lower()

        if answer == 'no':
            return f"{self.name}: Sorry, just wanted to learn!"
            
            
        print(f'{self.name}: What do you expect me to answer?')
        learning = input("answer here: ")
        self.data.setdefault(talk, f"{self.name}: {learning}")
        return f'{self.name}: Thank you for teaching me!'


    def save(self):
        jsonName = Bot.path.join(Bot.DIRECTORY, f'{self.name}.json')
        
        with open(jsonName, 'w') as file:
            Bot.json.dump(self.data, file, indent=2)
        return "I'am save!"


    def load(self, name):
        jsonName = Bot.path.join(Bot.DIRECTORY, f'{name}.json')
        with open(jsonName, 'r') as file:
            self.data = Bot.json.load(file)



bot1 = Bot('Richard')
while True:
    talk = input("answer here: ")
    print(bot1.talk(talk))