#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Person:
    def __init__(self, name, job=None, pay=0 ): # Конструктор принимает 3 аргумента
        self.name = name                        # Заполняет поля при создании
        self.job = job                          # self – новый экземпляр класса
        self.pay = pay
    
    # Методы, реализующие поведение экземпляров
    def lastName(self):
        return self.name.split()[-1]        # self – подразумеваемый экземпляр
    
    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))
    
    def __str__(self):
        return '[Person: %s, %s]' % (self.name, self.pay) 

class Manager(Person):                          # Наследует атрибута класса Person
    
    def __init__(self, name, pay):              # Переопределенный конструктор
        Person.__init__(self, name, 'mgr', pay)
    
    def giveRaise(self, percent, bonus=.10):
        Person.giveRaise(self, percent + bonus) 
    
    def thomeElse(self, name):
        print ('Fuck you',name)




if __name__ == '__main__':
    # Тестирование класса
    # ----------------------------simple test
    bob = Person('Bob Smith')                          
    sue = Person('Sue Jones', job='dev', pay=100000)    # Запустит __init__ автоматически
    print(bob.name, bob.pay)                            # Извлечет атрибуты
    print(sue.name, sue.pay)                            # Атрибуты в объектах sue и отличаются
    print(bob.name.split()[-1])                         # Извлечь фамилию
    sue.pay *= 1.10                                     # Повысить зарплату
    print(sue.pay)
   
    print(bob.lastName(), sue.lastName())               
    sue.giveRaise(.10)                      
    print(sue.pay)
    print(sue)
    # ----------------------------advanced test
    
    print ('')
    print ('advanced test')
    print ('')
    testuser = Person('Testname Testlastname')
    
    if ('Testname Testlastname' is testuser.name and
        (testuser.job is None) and
        (testuser.pay == 0)
    ):
        print ('Init Class Person --- OK')
        #print (testuser)
        #print (testuser.job)
        #print (testuser.pay)
    else:
        print ('Init Class Person --- NOT OK')
        print (testuser)
        print (testuser.job)
        print (testuser.pay)
    
    test1user = Person('Testname1 Lastname1', pay=100)
    print ('до увеличения зп',test1user.pay)
    test1user.giveRaise(.10)  # увеличение оплаты на 10%
    print ('после увеличения зп',test1user.pay)
    #print (test1user.giveRaise(.10))
    if ('Lastname1' == test1user.lastName() and
        test1user.pay == 110
    ):
        print ('Method Class Person --- OK')
    else:
        print ('Method Class Person --- NOT OK')
        
        
    # -----------------------WORK with Manager
    print ()
    print ('WORK with Manager')
    
    tom = Manager('Tom Jones', 'mgr', 50000)            # Экземпляр Manager: __init__
    tom.giveRaise(.10)                                  # Вызов адаптированной версии
    print(tom.lastName())                               # Вызов унаследованного метода
    print(tom) 
    tom.pay=50000
    print (tom.pay)
    print (tom.thomeElse(tom.lastName()))