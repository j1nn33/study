"""
  ЗАДАЧИ НА ДЕКОРАТОРЫ
+ Написать декоратор, который отменяет выполнение любой декорированной функций и будет писать в консоль: ИМЯ_ФУНКЦИИ is canceled!
+ Реализовать декоратор, который измеряет скорость выполнения функций.
+ Реализовать декоратор, который будет считать, сколько раз выполнялась функция
+ Реализовать декоторатор, который будет логгировать процесс выполнения функции: создан декоратор, начато выполнение функции, закончено выполнение функции

"""
#-------------------------- 1 --------------------------
# Написать декоратор, который отменяет выполнение любой декорированной функций и будет писать в консоль: ИМЯ_ФУНКЦИИ is canceled!
print ('task 1')
def decorator_funck(funck):
	def cansel_funck():
		funck()									# вывод оригинальной функции 
		print (funck.__name__, 'is canceled!')  # вывод декорированной функции
	return cansel_funck

@ decorator_funck
def main_funck():
	print ('main funck')

main_funck()									# вызов оригинальной функции под декоратором


#-------------------------- 2 --------------------------
# Реализовать декоратор, который измеряет скорость выполнения функций.
print ('task 2')
import time, datetime

def decorator_funck(funck):
	def timer():
		start_time = datetime.datetime.now()
		funck()									# вывод оригинальной функции 
		finish_time = datetime.datetime.now()
		print (finish_time - start_time)
	return timer

@ decorator_funck
def main_funck():
	print ('main funck')
	time.sleep(0.01)

main_funck()									# вызов оригинальной функции под декоратором

#-------------------------- 3 --------------------------
# Реализовать декоратор, который будет считать, сколько раз выполнялась функция
print ('task 3')

main_count=0

def decorator_funck(funck):
	
	def count_funck():
		global main_count     # указать внутри функции, что мы хотим использовать глобальную переменную вместо локальной
		# print ('-------', main_count)
		funck()									# вывод оригинальной функции 
		main_count=main_count+1
		
	return count_funck

@ decorator_funck
def main_funck():
	pass
	
main_funck()
main_funck()	
main_funck()
main_funck()			
print ('main_count', main_count)

#-------------------------- 4 --------------------------
# Реализовать декоторатор, который будет логгировать процесс выполнения функции: создан декоратор, начато выполнение функции, закончено выполнение функции
print ('task 4')
def decorator_funck(funck):
	print ('создан декоратор')
	def log_funck():
		print ('начато выполнение функции')
		funck()									# вывод оригинальной функции 
		print ('закончено выполнение функции')  # вывод декорированной функции
	return log_funck

@ decorator_funck
def main_funck():
	print ('main funck')

main_funck()									# вызов оригинальной функции под декоратором

