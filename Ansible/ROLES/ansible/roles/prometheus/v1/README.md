Роль для развертыванивя prometeus

./ROLES/ansible/roles/prometheus/v1/vars/main.yml
описание переменных 
версии 
  - prometeus
  - alertmanager

systemdunit находится 
./ROLES/ansible/roles/prometheus/v1/templates/prometheus.service

Конфигурирование 
Не задано
опции —storage.tsdb.retention.time и —storage.tsdb.retention.size. 
Первая опция говорит, что нужно удалять старые данные старше Х дней, а вторая задает удаление по размеру хранимых данных


# #######################
Проверка на целевом хосте 

Проверка пререквизитов 
systemctl status firewalld
firewall-cmd --list-all

cat /etc/selinux/config


# #######################  
# PROMETEUS          
cat /etc/passwd
# prometheus:x:1000:1000::/home/prometheus:/bin/false

Создание директорий
ll /tmp/ | grep pro
# drwxr-xr-x. 3 prometheus prometheus  43 Sep  4 14:24 prometheus

ll /etc/ | grep prom
# drwxr-xr-x.  4 prometheus prometheus     69 Sep  4 14:24 prometheus  

ll /etc/prometheus/

# drwxr-xr-x. 2 prometheus prometheus  38 Aug 16 16:42 console_libraries
# drwxr-xr-x. 2 prometheus prometheus 173 Aug 16 16:42 consoles
# -rw-r--r--. 1 prometheus prometheus 934 Aug 16 16:42 prometheus.yml

ll /var/lib/ | grep prom
# drwxr-xr-x. 2 prometheus prometheus    6 Sep  4 14:23 prometheus

Скачиваение и распаквка архива 
 ll /tmp/prometheus/
# drwxr-xr-x. 4 3434 3434 132 Aug 16 16:45 prometheus-2.38.0.linux-amd64

ll /usr/local/bin/

# -rwxr-xr-x. 1 prometheus prometheus 110234973 Aug 16 16:26 prometheus
# -rwxr-xr-x. 1 prometheus prometheus 102028302 Aug 16 16:28 promtool




Проверим факт запуска:

systemctl status prometheus


Проверка через веб

Prometeus
http://192.168.X.X:9090

prometeus server metrics
http://192.168.X.X:9090/metrics


# #########################
# Alertmanager


cat /etc/passwd
# alertmanager:x:1001:1001::/home/alertmanager:/bin/false

Создание директорий
ll /tmp/ | grep alert
# drwxr-xr-x. 3 alertmanager alertmanager  45 Sep  4 16:51 alertmanager

ll /etc/ | grep alert
# drwxr-xr-x.  2 alertmanager alertmanager     30 Sep  4 16:51 alertmanager  

ll /etc/alertmanager/

# -rw-r--r--. 1 alertmanager alertmanager 356 Mar 25 12:38 alertmanager.yml


ll /var/lib/prometheus/ | grep alertmanager
# drwxr-xr-x. 2 alertmanager alertmanager     6 Sep  4 16:50 alertmanager

Скачиваение и распаквка архива 
ll /tmp/alertmanager/

# drwxr-xr-x. 2 3434 3434 93 Mar 25 12:39 alertmanager-0.24.0.linux-amd64


 ll /usr/local/bin/

# -rwxr-xr-x. 1 alertmanager alertmanager  31988661 Mar 25 12:32 alertmanager
# -rwxr-xr-x. 1 alertmanager alertmanager  25067944 Mar 25 12:33 amtool
# -rwxr-xr-x. 1 prometheus   prometheus   110234973 Aug 16 16:26 prometheus
# -rwxr-xr-x. 1 prometheus   prometheus   102028302 Aug 16 16:28 promtool




Проверим факт запуска:

systemctl status alertmanager

Проверка через веб

Alertmanager
http://192.168.X.X:9093



# #########################
# GRAFANA

http://192.168.X.X:3000






Node-exporter
URL <host>/metric:9100

Проверим синтаксис:

# promtool check config /etc/prometheus/prometheus.yml