_____CLASS_______
class A:
    def g(self): # self - обязательный аргумент, содержащий в себе экземпляр
                 # класса, передающийся при вызове метода,
                 # поэтому этот аргумент должен присутствовать
                 # во всех методах класса.
    return 'hello world'
    

создание экземпляров класса

a = A()
b = A()

a.arg = 1 # у экземпляра a появился атрибут arg, равный 1


print(a.arg)

# 1

print (a.g())

# 'hello world'

Инкапсуляция — ограничение доступа к составляющим объект компонентам (методам и
переменным). Инкапсуляция делает некоторые из компонент доступными только внут-
ри класса.

class Example(object):
    def __init__(self):
        self.a = 1
        self._b = 2
        self.__c = 3
        print('{} {} {}'.format(
            self.a, self._b, self.__c))

    def call(self):
        print('Called!')

    def _protected_method(self):
        pass

    def __private_method(self):
        pass


class Inh(Example):
    def nnn(self):
        self._b = 5
        self.__c = 6



example = Example()
print(example.a)
print(example._b)


try:
    print(example.__c)
except AttributeError as ex:
    print(ex)


"""
1 2 3
1
2
'Example' object has no attribute '__c'
"""

Наследование подразумевает то, что дочерний класс содержит все атрибуты родитель-
ского класса, при этом некоторые из них могут быть переопределены или добавлены в
дочернем. 

class Parent(object):
    def __init__(self):
        print('Parent inited')
        self.value = 'Parent'

    def do(self):
        print('Parent do(): {}'.format(self.value))


class Child(Parent):
    def __init__(self):
        print('Child inited')
        self.value = 'Child'


parent = Parent()
parent.do()

child = Child()
child.do()

"""
Parent inited
Parent do(): Parent
Child inited
Parent do(): Child


"""



Полиморфизм - разное поведение одного и того же метода в разных классах. Например,
мы можем сложить два числа, и можем сложить две строки. При этом получим разный
результат, так как числа и строки являются разными классами.

class Parent(object):
    def call(self):
        print('Parent')


class Child(Parent):
    def call(self):
        print('Child')


class Example(object):
    def call(self):
        print('Ex')


def call_obj(obj):
    obj.call()


def sum_two_objects(one, two):
    return one + two


call_obj(Child())
call_obj(Parent())


"""
Child
Parent

"""

