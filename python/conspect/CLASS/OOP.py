
class Person:
	def __init__(self, name, age, pay=0, job=None):
		self.name = name
		self.age = age
		self.pay = pay
		self.job = job

	def lastName(self):
		return self.name.split()[-1]
    
	def giveRaise(self, percent):
		self.pay = self.pay+self.pay*0.1
class Manager(Person):
	def giveRaise(self, percent, bonus=5):
		Person.giveRaise(self,percent)
		# повторное использование кода
		# Person.giveRaise(self,percent) - использование 
		# функции родителя по исполнеию которого код помещается
		# в  self.pay
		# 		# 
		# 2 вариант всего этого self.pay = self.pay+self.pay*0.1
		print ('self.pay ', self.pay)
		self.pay=self.pay+bonus*7  

if __name__ == '__main__':
	bob = Person('Bob Smith', 42, 300, 'software')
	sue = Person('Sue Jones', 45, 400, 'hardware')
	print(bob.name, sue.pay)
	print(bob.lastName())
	sue.giveRaise(.10)
	print(sue.pay)
	print('====== inharited ======')
	tom = Manager(name='Tom Doe', age=50, pay=500)
	print(tom.lastName())
	tom.giveRaise(.10,5)
	print(tom.pay)