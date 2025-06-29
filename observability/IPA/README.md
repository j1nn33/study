#### IPA  observability and AUDIT

#### INTRO
#### STAND
#### IPA tunning
#### LOGGING
#### MONITORING

#### AUDIT SECURITY
###### ==============================


###### INTRO

1 LOGGING    - процесс сбора логов в ELK стек и построение дашбордов 
2 MONITORING - процесс мониторинга ldap
3 - процесс анализа логов (событий безопасности и сбор их в долговременное хранилище для последующего анализа)

MAN
https://docs.altlinux.org/ru-RU/domain/10.4/html/freeipa/index.html
https://github.com/mzamora9913/Collecting-Syslogs-from-FreeIPA-and-clients-using-ELK-Stack

|                                          |                                                                   | 
|:----------------------------------------:|:-----------------------------------------------------------------:|
| /var/log/httpd/error_log                 | FreeIPA API call logs (and Apache errors)                         |
| /var/log/krb5kdc.log                     | FreeIPA KDC utilization                                           |
| /var/log/dirsrv/slapd-$REALM/access      | Directory Server utilization                                      |
| /var/log/dirsrv/slapd-$REALM/errors      | Directory Server errors (including mentioned replication errors)  |
| /var/log/pki/pki-tomcat/ca/transactions: | FreeIPA PKI transactions/logs                                     |
|                                          |                                                                   |
| freeIPA client logs                      |                                                                   |
| /var/log/sssd/*.log                      | SSSD logs (multiple, for all tracked logs)                        |                
| /var/log/audit/audit.log                 | user login attempts                                               |
| /var/log/secure                          | reasons why user login failed                                     |



=====================================   
###### STAND 

192.168.1.101   IPA 
192.168.1.230   kafka
192.168.1.1     monitoring
192.168.1.162   ELK  ad

======================================

###### Архитектура 

1 LOGGING
	ver 1
vector(1) ---> kafak ---> vector(2) ---> elasticsearch ---> kibana ---> dashboard  

	ver 2   
filebeat ---> kafka ---> logstash ---> elasticsearch ---> kibana ---> dashboard

2 MONITORING
ldapexporter ---> prometeus ---> grafana
   
3 AUDIT SECURITY
ELK ---> ETL ---> DB   
   
###### IPA tunning

Добавить логи 
/var/log/dirsrv/slapd-$REALM/audit  

Настройка (некоторые параметры)
|  Параметр                            |  Значенение                           |   Описание                            | 
|:------------------------------------:|:-------------------------------------:|:-------------------------------------:|
| nsslapd-securePort                   |  636                                  |  Порт LDAPS.                          |
| nsslapd-security                     |  on                                   |  Включение LDAPS.                     |
| nsslapd-auditlog-logging-enabled     |  on                                   |  Включить логирование событий аудита. |
| nsslapd-errorlog-logging-enabled     |  on                                   |  Включить логирование ошибок.         |
| nsslapd-accesslog-logging-enabled    |  on                                   |  Включить логирование событий доступа.| 
| nsslapd-auditfaillog-logging-enabled |  on                                   |  Включить логирование ошибок доступа. |
| nsslapd-accesslog-level              |  256                                  |  Уровень логирования событий доступа. |
| nsslapd-errorlog-level               |  16384                                |  Уровень логирования ошибок.          |
| nsslapd-auditlog                     | /var/log/dirsrv/slapd-{REALM}/audit   |  Путь к лог-файлу событий аудита.     |
| nsslapd-accesslog                    | /var/log/dirsrv/slapd-{REALM}/access  |  Путь к лог-файлу событий доступа.    |
| nsslapd-errorlog                     | /var/log/dirsrv/slapd-{REALM}/errors  |  Путь к лог-файлу ошибок.             |
| nsslapd-allow-anonymous-access       | rootdse                               |  Отключение анонимного доступа к LDAP.|

    как применить
заносим настройки напрямую в файл /etc/dirsrv/slapd-*/dse.ldif
проверяем наличие настроек в файле (при внесении настроек важно отсутвие пробелов в конце)
остановка ipa
бекап файла
правка файла 

sslapd-errorlog-level: 16384
nsslapd-errorlog-logging-enabled: on
nsslapd-auditlog-logging-enabled: on
nsslapd-accesslog-logging-enabled: on
nsslapd-auditfaillog-logging-enabled: on
nsslapd-accesslog-level: 256

###### LOGGING ver 1

vector(1) ---> kafak ---> vector(2) ---> elasticsearch ---> kibana (dashboard)

######## Условие задачи и разбор примера 

Цель мероприятия строки логов обогатить полями и преобразовать в json 

- примеры логов source.txt 
- пример 1 (принцип логированя )   ./study/ELK/VECTOR/example_1.md
- track пример                     ./study/observability/IPA/trackt.md    
- лог парсер                       ./study/observability/ipa_parser.md
.//study/observability/IPA/ipa_vector_client_v1.yaml


=================================
###### LOGGING ver 2  

Пример описывется по ссылке выше 

filebeat ---> kafka ---> logstash ---> elasticsearch ---> kibana (dashboard)
####### filebeat - устанавливается на freeIPA
filebeat - устанавливается на freeIPA

curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.5.2-x86_64.rpm
rpm -ivh filebeat-8.5.2-x86_64.rpm

конфигурация 
https://www.elastic.co/guide/en/beats/filebeat/8.17/configuration-filebeat-options.html


###### MONITORING

