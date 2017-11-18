#Преобразовать строку MAC из формата XXXX:XXXX:XXXX в формат
#XXXX.XXXX.XXXX

MAC = 'AAAA:BBBB:CCCC'
print (MAC)
NEW_MAC = MAC.replace (':', '.')
print (NEW_MAC)