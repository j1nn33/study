Декоратор пример
Класс Person принимает два значения и ему надо их передать как одно в виде списка
@classmethod (заменяте стандартный метод) принимает на вход класс и список

class Person:
    
    def __init__(self, name, last_name):
        self.name = name
        self.last_name = last_name

     @classmethod
     def person_creator(cls, data):
         name, last_name = data
         return "Name : {0}. Last name: {1}".format(self.name, self.last_name)

     def print_info(self):
         return "Name : {0}. Last name: {1}".format(self.name, self.last_name)    

     @staticmethod
     def print_static_info(self):
         return self.name

 p = Person.person_creator(['Alex', 'Ivanov'])
 print(p.name, p.last_name)
 print(p.print_info())
 print(p.print_staic_info(p))        