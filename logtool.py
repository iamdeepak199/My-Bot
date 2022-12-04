from datetime import datetime
from os import path, makedirs

dirLog = None

def logAppend(log,extension='txt', prefix='logInfo', dir='./logs/'):
    global dirLog
    fullDateTime = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    msg = f'({fullDateTime[:10]} {fullDateTime[11:]}) -> {log}\n'
    
    def logName():
        if not path.isdir(dir):
            makedirs(dir)
        logInfoName = f'{prefix}_{fullDateTime}'
        return f'{dir}{logInfoName}.{extension}'
    
    if dirLog is None:
        dirLog = logName()
            
    with open(dirLog, 'a') as logCreate:
        logCreate.write(msg)
