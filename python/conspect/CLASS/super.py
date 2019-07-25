# -*- coding: utf-8 -*-
# метод super явное обращение к родительскому методу

# родительский класс со своей логикой
# def __init__(self, value):
# def count(self):
class Calc(object):
    def __init__(self, value):
        print('Calc constructor is called')
        self.value = value

    def count(self):
        return self.value * 8 + 9


c = Calc(1.4)
print(c.count())

# class ExtendedCalc(Calc) наследуется от Calc
# super() - позволяет обращаться к методу родителя 
#

class ExtendedCalc(Calc):
    def __init__(self, value, k=1):   # определен свой метод init для ExtendedCalc добавили  k=1
        super().__init__(value)       # позволяет инициализировать  value как в родительском классе
        print('Extender', self.value)

        self.k = k

    def count(self):
        a = self.k + 1
        # previous = super() позволяет использовать код из родителя Calc
        # чтобы не писать его  
        previous = super().count()    
        #  previous = self.value * 8 + 9
        return -1 * self.k * previous

e = ExtendedCalc(8, k=1.2)
print(e.count())
