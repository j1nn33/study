#### Парсер логов IPA
```
 - Архитектура 
 - Список логово
 - Клиенсткая часть 
 - Серверная часть
 - ELK (dashboard)
```
###### Архитектура 
реализовывем LOGGING ver 1     ./study/observability/IPA/README.md
vector(1) ---> kafak ---> vector(2) ---> elasticsearch ---> kibana (dashboard)

###### Список логово
```
    логи хоста 
 + /var/log/messages
 + /var/log/maillog
 + /var/log/cron
 + /var/log/yum.log
 + /root/.bash_history
 + /home/*/.bash_history
 + /var/log/sssd/*.log
 + /var/log/audit/*.log
 + /var/log/secure

    логи freeIPA
 - /var/log/httpd/error_log        
 - /var/log/httpd/access_log         
 - /var/log/krb5kdc.log                     
 - /var/log/dirsrv/slapd-$REALM/access      
 - /var/log/dirsrv/slapd-$REALM/errors 
 - /var/log/dirsrv/slapd-$REALM/audit     
 - /var/log/pki/pki-tomcat/ca/transactions: 
 - /var/log/pki/pki-tomcat/ca/debug
 - /var/log/kadmind.log

```

###### Клиенсткая часть 
```
   логи хоста 
разбирать не будем просто пойдут исходной строкой (аналитика в ELK по ним строится не будет)+ некоторые дополнительные поля

 - /var/log/messages
 - /var/log/maillog
 - /var/log/cron
 - /var/log/yum.log
 - /root/.bash_history
 - /home/*/.bash_history
 - /var/log/sssd/*.log
 - /var/log/audit/*.log
 - /var/log/secure

    логи freeIPA 
(будут разбираться для отдельного для анализа )
 - /var/log/httpd/error_log        
 - /var/log/httpd/access_log         
 - /var/log/krb5kdc.log                     
 - /var/log/dirsrv/slapd-$REALM/access      
 - /var/log/dirsrv/slapd-$REALM/errors 
 - /var/log/dirsrv/slapd-$REALM/audit     
 - /var/log/pki/pki-tomcat/ca/transactions: 
 - /var/log/pki/pki-tomcat/ca/debug
 - /var/log/kadmind.log

```
Обязательные дополнительные поля 

```
.raw_message = .message         # сохранение исходного сообщения 
.environment = "dev"            # добавление тега стенда 
del(.source_type)               # удаление лишнего поля 
.@timestamp = del(.timestamp)   # преобразование timestamp по @timestamp будет строится патерн индекса
.date = .message.date
.hostname = .message.hostname 
.type_log = "krb5kdc_log"       # тип лога
```



###### Серверная часть
###### ELK (dashboard)