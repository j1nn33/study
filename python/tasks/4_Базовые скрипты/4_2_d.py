# Переделать скрипт из задания 4.2c таким образом, чтобы, при запросе параметра,
# пользователь мог вводить название параметра в любом регистре.

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
param = param.lower()
                                    # Выыод информации
print (london_copy.get(param,'Такого параметра нет'))