try: 
    #исполняемый код
    pass
except Exeption as e:
    #обработка исключения
    pass
else:
    #код, который будет исполнен в случае, когда нет исключения
    pass
finally:
    #код, который гарантированно будет исполнен последним (всегда исполняется)	
	pass

# ----

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Деление на ноль!")

