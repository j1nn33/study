"""
структура пакета
fincalc
|-- _init__.py
|-- simper.py
|-- compper.py
|-- annuity.py
Пакет fincal содержит в себе модули
simper.py, compper.py annuity.py.
Для использования функции из модуля  можно
использовать один из следующих вариантов:
"""
import fincalc.simper
fv = fincalc.simper.fv(pv, i, n)

import fincalc.simper as sp
fv = sp.fv(pv, i, n)

from fincalc import simper
fv = simper.fv(pv, i, n)

"""
Файл _init__.py может быть пустым или может содержать переменную _all__,
хранящую список модулей, который импортируется при загрузке через 
конструкциюfrom имя_пакета import *
Например для нашего случая содержимое _init__.py может быть вот таким:
"""
__all__ = ["simper", "compper", "annuity"]


"""         ООП         """

имя_объекта = имя_класса()

class Rectangle:
    color = "green"
    width = 100
    height = 100
    def square(self):
        return self.width * self.height

"Доступ к атрибуту класса имя_объекта.атрибут"
rect1 = Rectangle()
print(rect1.color)
print(rect1.square())

"""
Конструктор класса позволяет задать определенные параметры 
объекта при его создании. Таким образом появляется возможность 
создавать объекты с уже заранее заданными атрибутами.
Конструктором класса является метод:
_init__(self)
Например, для того, чтобы иметь возможность задать цвет, длину и ширину
прямоугольника при его создании,
добавим к классу Rectangle следующий конструктор:
"""
class Rectangle:
    def __init__(self, color = "green", width = 100, height = 100):
        self.color = color
        self.width = width
        self.height = height
    def square(self):
        return self.width * self.height

rect1 = Rectangle()
print(rect1.color)
print(rect1.square())
rect1 = Rectangle("yellow", 23, 34)
print(rect1.color)
print(rect1.square())
"""
green
10000
yellow
782
"""
"""
ДВА И БОЛЕЕ РОДИТЕЛЕЙ:
class имя_класса(имя_родителя1, [имя_родителя2,…, имя_родителя_n])
"""
class Figure:
    def __init__(self, color):
        self.color = color
    def get_color(self):
        return self.color

class Rectangle (Figure):
    def __init__ (self, color, width = 100, height = 100):
        super().__init__(color)
        self.width = width
        self.height = height
    def square(self):
        return self.width * self.height

rect1 = Rectangle( "blue" )
print(rect1.get_color())
print(rect1.square())
rect2 = Rectangle("red", 25, 70)
print(rect2.get_color())
print(rect2.square())

""""
blue
10000
red
1750
"""
"""
полиморфизм, используется с позиции переопределения методов базового класса в классе
наследнике.
"""

class Figure:
    def __init__(self,color):
        self.color = color
    def get_color(self):
        return self.color
    def info(self):
        print("Figure")
        print("Color: "+ self.color)

class Rectangle ( Figure ):
    def __init__ ( self , color , width = 100 , height = 100 ):
        super ().__init__(color)
        self .width = width
        self .height = height
    def square ( self ):
        return self .width * self .height
    def info ( self ):
        print ( "Rectangle" )
        print ( "Color: " + self .color)
        print ( "Width: " + str ( self .width))
        print ( "Height: " + str ( self .height))
        print ( "Square: " + str ( self .square()))
fig1 = Figure( "green" )
print (fig1.info())
rect1 = Rectangle( "red" , 24 , 45 )
print (rect1.info())
"""
Figure
Color: green
None
Rectangle
Color: red
Width: 24
Height: 45
Square: 1080
None
"""

