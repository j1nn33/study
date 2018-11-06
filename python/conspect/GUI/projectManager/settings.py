# здесь храняться обработчик файла настроек
# каталог по умолчанию где храняться проекты

import os, json
settingsFileName = 'projectManagerFileName.json'

class settingsClass(object):
    def __init__(self):
        # файл настроек храниться в каталоге пользователя в хависимости от ОС
        self.path = os.path.join(os.path.expanduser('~'), settingsFileName)
        if not os.path.exists(self.path):
            self.makeDedfault(self.path)

    def makeDedfault(self, path):
        # создает по умолчанию если нет
        defData = dict(
            path = ''
        )
        with open (path, 'w') as f:
            json.dump(defData, f, indent=4)

    def load(self):
        return json.load(open(self.path))

    def save(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f, indent=4)
