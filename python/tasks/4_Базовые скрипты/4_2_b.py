# Переделать скрипт из задания 4.2a таким образом, чтобы, при запросе параметра,
# отображался список возможных параметров.
# Вывести информацию о соответствующем параметре, указанного устройства.
# 
# $ python task_4_2b.py
# Enter device name: r1
# Enter parameter name (ios,model,vendor,location,ip): ip
# 10.255.0.1
##############################################
"""
 Задание словаря
 Ввод информации от пользователя
 Обработка информации
 Выыод информации
"""
                                # Задание словаря (в словаре в качестве значения можно используется словарь)
london_co = {
    'r1' : {
    'location': '21 New Globe Walk',
    'vendor': 'Cisco',
    'model': '4451',
    'ios': '15.4',
    'ip': '10.255.0.1'
    },
    'r2' : {
    'location': '21 New Globe Walk',
    'vendor': 'Cisco',
    'model': '4451',
    'ios': '15.4',
    'ip': '10.255.0.2'
    },
    'sw1' : {
    'location': '21 New Globe Walk',
    'vendor': 'Cisco',
    'model': '3850',
    'ios': '3.6.XE',
    'ip': '10.255.0.101',
    'vlans': '10,20,30',
    'routing': True
    }
}

                                    # Ввод информации от пользователя
#name = input('Введите имя устройства ')
name = 'r1'
london_copy={}                      # создаем пустой словарь
london_copy.update(london_co[name]) # заполняем пустой словарь значение (которое является словарем) 
#print (london_copy.keys())
param = input('Enter parameter name {}'.format(london_copy.keys()))
print (param)
                                # Обработка информации

                                # Выыод информации
print (london_copy[param])


# Enter device name: r1
# Enter parameter name (ios,model,vendor,location,ip): ip
# 10.255.0.1