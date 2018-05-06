#----------------------------
# Program  by Konstantin. B.
#
# Version	Date		
# 1.0 		2018
# Info
#
#----------------------------

class Hero():
	def __init__(self, name, level, race):
		self.name=name
		self.level=level
		self.race=race
		self._health=100

	def show_hero(self):
		description=(self.name+' level '+str(self.level)+' health '+str(self._health))
    
		print(description)
	def newhealth(self,healt):
		self._health=healt


"""
Класс SuperHero
берет все что есть в Hero
"""
class SuperHero (Hero):
	"""Class to Create Super Hero"""
	def __init__(self, name, level, race, magiclevel):
		super().__init__(name, level, race)
		self.magiclevel = magiclevel
		self.magic = 100

	def makemagic(self):
		"""use magic"""
		self.magic -= 10

	def show_hero(self):
		description=(self.name+' level '+str(self.level)+' health '+str(self._health)+
			         " Magic is "+ str(self.magic))
		print(description)

orc=Hero('wix', 6, 'orc')
orc.show_hero()
orc.newhealth(90)
orc.show_hero()

man=SuperHero("SOLO",10,"Human",5)
man.show_hero()
man.makemagic()
man.show_hero()