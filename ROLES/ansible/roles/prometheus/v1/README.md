Роль для развертыванивя prometeus

./ROLES/ansible/roles/prometheus/v1/vars/main.yml
описание переменных 
версии 
  - prometeus
  - alertmanager

systemdunit находится 
./ROLES/ansible/roles/prometheus/templates/prometheus.service

Конфигурирование 
Не задано
опции —storage.tsdb.retention.time и —storage.tsdb.retention.size. 
Первая опция говорит, что нужно удалять старые данные старше Х дней, а вторая задает удаление по размеру хранимых данных


#####################
Проверка на целевом хосте 

Проверка пререквизитов 
systemctl status firewalld
firewall-cmd --list-all

cat /etc/selinux/config

Проверим факт запуска:

systemctl status prometheus


Проверка через веб

