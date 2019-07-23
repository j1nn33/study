"""
*ЗАДАЧА 1:
Реализовать класс Person, у которого должно быть два публичных поля: age и name. 
Также у него должен быть следующий набор методов: know(person), который позволяет 
добавить другого человека в список знакомых. И метод is_known(person), который возвращает знакомы ли два человека
"""
class Person():
	def __init__(self, name, age):
		self.name = name
		self.age = age
		self.know_list =[]

	def know(self, person):
		#print ('name ', self.name)
		#print ('person', person.name)
		#print ('know_list_before', self.know_list)
		if not (person.name in self.know_list):
		    self.know_list.append(person.name)
		
		#print ('know_list_after', self.know_list)

	def is_known(self, person):
	    if person.name in self.know_list:
	        return print (self.name, ' is khow ', person.name)
	    else:
	        return print (self.name, ' dont khow ', person.name) 	




user1 = Person('Pol', 23)
user2 = Person('Aron', 23)
user3 = Person('jack', 23)
user4 = Person('Fic', 23)
#print ('user1.name ', user1.name)
#print ('user1.know_list ',user1.know_list)
user1.know(user2)
user1.know(user2)
user1.know(user3)
#print ('user1.know_list ',user1.know_list)
user1.is_known(user2)
user1.is_known(user3)
user1.is_known(user4)
user2.is_known(user4)

