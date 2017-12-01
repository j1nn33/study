# Переделать скрипт из задания 4.2b таким образом, чтобы, при запросе параметра,
# которого нет в словаре устройства, отображалось сообщение 'Такого параметра нет'.
# Если выбран существующий параметр, вывести информацию о соответствующем
# параметре, указанного устройства.
#
# $ python task_4_2c.py
# Enter device name: r1
# Enter parameter name (ios,model,vendor,location,ip): io
# Такого параметра нет
###############################
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
param = input('Enter parameter name {}'.format(london_copy.keys()))
                                    # Выыод информации
print (london_copy.get(param,'Такого параметра нет'))

# $ python task_4_2c.py
# Enter device name: r1
# Enter parameter name (ios,model,vendor,location,ip): io
# Такого параметра нет