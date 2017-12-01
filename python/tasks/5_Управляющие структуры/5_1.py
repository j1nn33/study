# 1. Запросить у пользователя ввод IP-адреса в формате 10.0.1.1.
# 2. Определить какому классу принадлежит IP-адрес.
# 3. В зависимости от класса адреса, вывести на стандартный поток вывода:
#           'unicast' - если IP-адрес принадлежит классу A, B или C
#           'multicast' - если IP-адрес принадлежит классу D
#           'local broadcast' - если IP-адрес равен 255.255.255.255
#           'unassigned' - если IP-адрес равен 0.0.0.0
#           'unused' - во всех остальных случаях
#  (диапазон значений первого байта в десятичном формате):
#  A: 1-127
#  B: 128-191
#  C: 192-223
#  D: 224-239
"""
 1 введнеие данных
 2 обработка данных
   - получение 1 байта (октека IP-адреса) в десятичном формате
   - определение принадлежности IP-адреса к классу
 3 вывод данных
"""

#     введнеие данных
#IP = input('INPUT IP -address (10.0.1.1) -')
IP = '10.0.1.1'
#print ('input ip -',type(IP),IP)              # input ip - <class 'str'> 10.0.1.1
#     обработка данных
#     - получение (октека IP-адреса) в десятичном формате
list_IP = IP.split(".")                       # преобразование строки к списку по разделителю
#print ('list_IP', list_IP)                    # list_IP ['10', '0', '1', '1']
CLASS_IP_A = int(list_IP[0])                    # получение первого октека IP в цисловом фомате
#print ('CLASS_IP_A',type(CLASS_IP_A),CLASS_IP_A)    # CLASS_IP <class 'int'> 10
CLASS_IP_B = int(list_IP[1])  
CLASS_IP_C = int(list_IP[2])  
CLASS_IP_D = int(list_IP[3])  
#     - определение принадлежности IP-адреса к классу
if (CLASS_IP_A > 0) and (CLASS_IP_A <= 223) :
    str_class = 'unicast'
elif (CLASS_IP_A > 223) and (CLASS_IP_A <= 239):
    str_class = 'multicast'
elif (CLASS_IP_A == 255) and (CLASS_IP_B == 255) and (CLASS_IP_C == 255) and (CLASS_IP_D == 255):
    str_class = 'local broadcast'
elif (CLASS_IP_A == 0) and (CLASS_IP_B == 0) and (CLASS_IP_C == 0) and (CLASS_IP_D == 0):
    str_class = 'unassigned'
else: 
    str_class = 'unused'
#     вывод данных
print ('класс IP адреса ', str_class)
