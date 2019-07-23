"""
Задача 1
1. Создать класс корзина, у которого можно выставить разную вместительность для разных объектов.
В объекты класса корзина можно помещать разные объекты;
2. Вам нужно создать класс пакет, в который тоже можно помещать предметы. У него тоже есть вместимость;
3. Создать любой класс, объекты которого можно было бы мощешать в корзину и пакет;
4. Если вместимости недостаточно, сказать, что объект поместить нельзя.

*ЗАДАЧА 2:
Пользователь вводит список чисел через пробел. если ввел:
1 число, строим квадрат
2 числа, строим прямоугольник
3 числа, треугольник
4 числа, многоугольник

вычисляем периметр и площадь.

"""
class Handbox():
	def __init__(self, size):     
		self.size = size
	def store(self, thing):
		if thing.size < self.size:
			print ('Вещь в корзине')
		else:
			print ('Вещь not корзине')
		

class Bag (Handbox):
	def store(self, thing):
		if thing.size < self.size:
			print ('Вещь в сумке')
		else:
			print ('Вещь not сумке')


class Thing():
	def __init__(self, size):
		self.size = size


k1 = Handbox (20)
k2 = Handbox (30)


b1 = Bag (10)
b2 = Bag (5)

t1 = Thing (3)
t2 = Thing (8)
t3 = Thing (16)
t4 = Thing (26)

l = [t1,t2,t3,t4]
for k in l:                    # цикл перебора вещей 
	print ('вещь ', k)
	b1.store(k)

# --------------------------

"""
*ЗАДАЧА 2:

"""
print ('====================================')
class Figure ():
    def __init__(self, *sides):     # передача произвольного числа параметров (длины сторон)
        self.sides = sides
        print (len(self.sides))          # вывод числа сторон
        print (self.sides)

    
    def _perimetr(self):		# делаем его приватным
    	#print (sum(self.sides))
    	if len(self.sides) == 1:
    		# подсчет периметра квадрата
    		perimetr_of_figure = self.sides[0]*2        
    	elif len(self.sides) == 2:
    		# подсчет периметра прямоугольника
    		perimetr_of_figure = self.sides[0]*2+self.sides[1]*2
    	elif len(self.sides) == 3:
    		perimetr_of_figure = (self.sides[0]+self.sides[1]++self.sides[2])
    	else:
    	    perimetr_of_figure = self.sides[0]*2+self.sides[1]*2+self.sides[2]*2+self.sides[3]*2


    	return perimetr_of_figure
  
    def print_perimetr(self):
    	print ('Периметр', self._perimetr() )
  
    def square (self):
    	return print ('метод Площадь Figure ')

    def print_square(self):
    	print ('Площадь', self.square())

class Rektange (Figure):
	def square(self):
		return self.sides[0]*self.sides[1]



class Square (Rektange):
	def square(self):
		return self.sides[0]*self.sides[0]
   

class Triangle (Figure):
	pass

class Polygon (Figure):
	pass


rect = Rektange (2,5)
rect.print_perimetr()        # вывод периметра прямоугольника
rect.print_square()
print('\n')
sqr = Square (4)
sqr.print_perimetr()
sqr.print_square()
print('\n')
trg = Triangle (5, 2, 4)
trg.print_perimetr()  
trg.print_square()
print('\n')
plgn = Polygon (5, 2, 4, 3)
plgn.print_perimetr()
plgn.print_square()  
		