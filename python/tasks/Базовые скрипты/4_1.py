# Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24
# Затем вывести информацию о сети и маске в таком формате:
# Network:
# 10       1        1        0
# 00001010 00000001 00000001 00000000
# Mask:
# /24
# 255      255      255      0
# 11111111 11111111 11111111 00000000

################################################################

# ВВОД ДАННЫХ

IPN = input(' Ввод IP-сети в формате: 10.1.1.0/04  ')
#IPN =  '10.1.1.0/24'
print(IPN)
# РАЗБОР ДАННЫХ
IP = IPN[:-3]     # все символы кроме последних трех
MASK = IPN[-3:]   # 3 последних символа
#print (IP)
#print (MASK)

# ОБРАБОТКА IP   (см 3_8)  

list_IP = IP.split(".")                       # преобразование в список
list_bin_IP = []                              # создание пустого списка   

"""
a=(list_mac[0])          # 1 и 2 строка
a=int(a, 16)             # преобразование строкового элемента списка в шестнацатиричное число 16 - префикс
                        
a=int(list_mac[0], 16)   # преобразование строкового элемента списка в шестнацатиричное число 16 - префикс тоже самое только одной строкой
print(bin(a))            # преобразование в бинарное число 

"""
element_bin_IP = (bin(int(list_IP[0], 10)))   
list_bin_IP.append (element_bin_IP[2::])     # добавление элемента в бинарный список и удаление 2-х первых символов
element_bin_IP = (bin(int(list_IP[1], 10))) 
list_bin_IP.append (element_bin_IP[2::])
element_bin_IP = (bin(int(list_IP[2], 10)))  
list_bin_IP.append (element_bin_IP[2::])
element_bin_IP = (bin(int(list_IP[3], 10)))
list_bin_IP.append (element_bin_IP[2::])

# ОБРАБОТКА МАСКИ

int_mask = int (MASK[1:])                    # удаление / у маски и преобразование его в число
#print (int_mask)
#print (type(int_mask))
bin_mask = ( '1' * int_mask + '0'*(32-int_mask))                 # получения маски в бинарном виде 
#print(bin_mask)
                                             # получение октеков бинарной маски путем срезов в виде строки
a=one_okt_bin_mask = bin_mask[:8]
b=two_okt_bin_mask = bin_mask[8:16]
c=three_okt_bin_mask = bin_mask[16:24]
d=four_okt_bin_mask = bin_mask[24:]
#print (one_okt_bin_mask)
#print (two_okt_bin_mask)
#print (three_okt_bin_mask)
#print (four_okt_bin_mask)
                                            # получение октеков маски в десятичной системе
                                            # 10110110 = (1·2^7)+(0·2^6)+(1·2^5)+(1·2^4)+(0·2^3)+(1·2^2)+(1·2^1)+(0·2^0) = 128+32+16+4+2 = 182 
                                            # print (int(a[0])*2**7)

one_okt_dec_mask = (int(a[0])*2**7+int(a[1])*2**6+int(a[2])*2**5+int(a[3])*2**4+int(a[4])*2**3+int(a[5])*2**2+int(a[6])*2**1+int(a[7])*2**0)
two_okt_dec_mask = (int(b[0])*2**7+int(b[1])*2**6+int(b[2])*2**5+int(b[3])*2**4+int(b[4])*2**3+int(b[5])*2**2+int(b[6])*2**1+int(b[7])*2**0)
three_okt_dec_mask = (int(c[0])*2**7+int(c[1])*2**6+int(c[2])*2**5+int(c[3])*2**4+int(c[4])*2**3+int(c[5])*2**2+int(c[6])*2**1+int(c[7])*2**0)
four_okt_dec_mask = (int(d[0])*2**7+int(d[1])*2**6+int(d[2])*2**5+int(d[3])*2**4+int(d[4])*2**3+int(d[5])*2**2+int(d[6])*2**1+int(d[7])*2**0)

# ВЫВОД ИНФОРМАЦИИ
print ("Network:")
print("{:10} {:10}  {:10}  {:10}".format(list_IP[0], list_IP[1], list_IP[2], list_IP[3]))
print("{:010} {:010}  {:010}  {:010}".format(int(list_bin_IP[0]), int(list_bin_IP[1]), int(list_bin_IP[2]), int(list_bin_IP[3])))
print ("Mask:")
print (MASK)


print("{:<8} {:<8} {:<8} {:<8}".format(one_okt_dec_mask, two_okt_dec_mask, three_okt_dec_mask, four_okt_dec_mask))
print("{:8} {:8} {:8} {:8}".format(one_okt_bin_mask, two_okt_bin_mask, three_okt_bin_mask, four_okt_bin_mask))



# /24
# 255      255      255      0
# 11111111 11111111 11111111 00000000