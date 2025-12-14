Условие задачи - разбор логов IP tables
цель - постороение графика в Kibana (график подсчеста входящих ip и их распределение по времени)



Принципр разбора лога 

в исходном сообщении распарсить поля и преобразовать строку в json

1 grok - парсер 
  основные патерные тут 
  https://www.alibabacloud.com/help/en/sls/user-guide/grok-patterns
  
  
Находим необходимый патерн для парсинга даты в json  
  %{SYSLOGTIMESTAMP:date} 
  ./image/1.png
  
Работа  с логом в парсере и результат применения патерна 
  https://www.javainuse.com/grok
  ./image/2.png 
  
Добаление полей и парсинг лога  
  ./image/3.png 

```bash
Mar 15 12:18:46 hostname.realm.ru kernel: IP limit exceeded IN=enp0s9 OUT=enp0s3 MAC=08:00:27:df:e0:96:09:00:27:e1:23:4b:08:00 SRC=192.168.176.4 DST=8.8.8.8 LEN=62 TOS=0x00 PREC=0x00 TTL=63 ID=62689 DF PROTO=UDP SPT=44611 DPT=53 LEN=42  
  
------------------------
%{SYSLOGTIMESTAMP:date} %{HOSTNAME:hostname} kernel: IP limit exceeded %{NOTSPACE:IN} %{NOTSPACE:OUT} %{NOTSPACE:MAC} SRC=%{IP:source_ip} DST=%{IP:destination_ip}

```
2 добавление конфигурции в вектор

vim 10_iptables.yaml

тестирование 

vector --config /root/logging/example_1.yaml

cat example_1.yaml
```yaml
sources:
  app_logs:
    type: "file"
    include:
      - "/root/logging/ip_tables.log"

transforms:
  app_logs_parser:
    inputs:
      - "app_logs"
    type: "remap"
    source: |
      . =  parse_grok!(
        .message, "%{SYSLOGTIMESTAMP:date} %{HOSTNAME:hostname} kernel: IP limit exceeded %{NOTSPACE:IN} %{NOTSPACE:OUT} %{NOTSPACE:MAC} SRC=%{IP:source_ip} DST=%{IP:destination_ip}"
      )
      .environment = "dev"             # добавелине полей 
      .hostname_1 = get_hostname!()    # добавелине имени хоста 
      del(.MAC)
sinks:
  print:
    type: "console"
    inputs:
      - "app_logs_parser"
    encoding:
      codec: "json"

```

Проверирить 

echo "Mar 15 12:18:46 hostname.realm.ru kernel: IP limit exceeded IN=enp0s9 OUT=enp0s3 MAC=08:00:27:df:e0:96:08:00:27:e1:23:4b:08:00 SRC=192.168.176.4 DST=8.8.8.8 LEN=62 TOS=0x00 PREC=0x00 TTL=63 ID=62689 DF PROTO=UDP SPT=44611 DPT=53 LEN=42" >> /root/logging/ip_tables.log

Получим 

{"IN":"IN=enp0s9","OUT":"OUT=enp0s3","date":"Mar 15 12:18:46","destination_ip":"8.8.8.8","environment":"dev","hostname":"hostname.realm.ru","hostname_1":"bastion","source_ip":"192.168.176.4"}

===========================


#### модифицируем логи под условие задачи 


Поля 
- timestamp                     - базовое поле по которому будет строится индекс в ELK для всех логов 
- raw_messages                  - исходное сообщение будет лежать в ELK для инфо - рабираться и индексироватся не будет
- .hostname = get_hostname!()   - имя хоста откуда логи
- .enviroment = "dev"           - указание стенда 
- .log.file.path = .file        - указание пути файла лога 

vector --config /root/logging/example_2.yaml

cat example_2.yaml

```yaml
sources:
  app_logs:
    type: "file"
    include:
      - "/root/logging/ip_tables.log"

transforms:
  app_logs_parser:
    inputs:
      - "app_logs"
    type: "remap"
    source: |
      . =  parse_grok!(
        .message, "%{SYSLOGTIMESTAMP:date} %{HOSTNAME:hostname} kernel: IP limit exceeded %{NOTSPACE:IN} %{NOTSPACE:OUT} %{NOTSPACE:MAC} SRC=%{IP:source_ip} DST=%{IP:destination_ip}"
      )
      .environment = "dev"             # добавелине полей 
      .hostname_1 = get_hostname!()    # добавелине имени хоста 
      del(.MAC)
sinks:
  print:
    type: "console"
    inputs:
      - "app_logs_parser"
    encoding:
      codec: "json"

```
Проверирить 

echo "Mar 15 12:18:46 hostname.realm.ru kernel: IP limit exceeded IN=enp0s9 OUT=enp0s3 MAC=08:00:27:df:e0:96:08:00:27:e1:23:4b:08:00 SRC=192.168.176.4 DST=8.8.8.8 LEN=62 TOS=0x00 PREC=0x00 TTL=63 ID=62689 DF PROTO=UDP SPT=44611 DPT=53 LEN=42" >> /root/logging/ip_tables.log

Получим 

```json
{"@timestamp":"2025-06-13T09:03:41.257405069Z",
 "environment":"dev","file":"/root/logging/ip_tables.log",
 "host":"bastion",
 "message":{"date":"Mar 15 12:18:46",
            "destination_ip":"8.8.8.8",
			"hostname":"hostname.realm.ru",
			"in":"IN=enp0s9",
			"mac":"MAC=08:00:27:df:e0:96:08:00:27:e1:23:4b:08:00",
			"out":"OUT=enp0s3",
			"source_ip":"192.168.176.4"
			},
 "raw_message":"Mar 15 12:18:46 hostname.realm.ru kernel: IP limit exceeded IN=enp0s9 OUT=enp0s3 MAC=08:00:27:df:e0:96:08:00:27:e1:23:4b:08:00 SRC=192.168.176.4 DST=8.8.8.8 LEN=62 TOS=0x00 PREC=0x00 TTL=63 ID=62689 DF PROTO=UDP SPT=44611 DPT=53 LEN=42"}
```

-------------

вынесение полей на один уровень


cat example_3.yaml

```yaml

sources:
  app_logs:
    type: "file"
    include:
      - "/root/logging/ip_tables.log"

transforms:
  app_logs_parser:
    inputs:
      - "app_logs"
    type: "remap"
    source: |
      .raw_message = .message                       # добавение исходного сообщения просто строкой 
      .message = parse_grok!(
        .message, "%{SYSLOGTIMESTAMP:date} %{HOSTNAME:hostname} kernel: IP limit exceeded %{NOTSPACE:in} %{NOTSPACE:out} %{NOTSPACE:mac} SRC=%{IP:source_ip} DST=%{IP:destination_ip}"
      )
      .environment = "dev"                          # добавелине стенда              
      del(.source_type)                             # удаление типа источника логов 
      .@timestamp = del(.timestamp)                 # манипуляции с timestamp - такой используется для построения в ELK (так повелось)
      .date = .message.date                         # оригинальная дата 
      .destination_ip = .message.destination_ip     #  
      .hostname = .message.hostname                 #
      .in = .message.in                             #
      .mac = .message.mac                           #
      .out = .message.out                           #
      .source_ip =.message.source_ip                # 
      del(.message)                                 # удаление message
sinks:
  print:
    type: "console"
    inputs:
      - "app_logs_parser"
    encoding:
      codec: "json"

```


```json
{"@timestamp":"2025-06-13T16:44:22.766753140Z",
 "date":"Mar 15 12:18:46",
 "destination_ip":"8.8.8.8",
 "environment":"dev","file":"/root/logging/ip_tables.log",
 "host":"bastion",
 "hostname":"hostname.realm.ru",
 "in":"IN=enp0s9",
 "mac":"MAC=08:00:27:df:e0:96:08:00:27:e1:23:4b:08:00",
 "out":"OUT=enp0s3",
 "raw_message":"Mar 15 12:18:46 hostname.realm.ru kernel: IP limit exceeded IN=enp0s9 OUT=enp0s3 MAC=08:00:27:df:e0:96:08:00:27:e1:23:4b:08:00 SRC=192.168.176.4 DST=8.8.8.8 LEN=62 TOS=0x00 PREC=0x00 TTL=63 ID=62689 DF PROTO=UDP SPT=44611 DPT=53 LEN=42","source_ip":"192.168.176.4"
}

```
#### Много патерная конфигурация
```
В чем суть в логах могут быть строки лога попадающие под разные патерны  

Алгоритм разбора такой 
 - производим первичный парсинг полей до поля который будет срабатывать по условию
 - далее строим конструкцию if else 

---------------------

Рабочий пример для однострочных логов разбираемых grok фильтром example_4_multipatern.yaml
отправляются на вход


echo "May 25 16:40:10 freeipa.local.lan" >> /root/logging/ip_tables.log
echo "May 25 16:40:10 closing down fd 12" >> /root/logging/ip_tables.log
echo "May 25 16:40:10 20" >> /root/logging/ip_tables.log
```
в Кафке получаем 

```
{"@timestamp":"2025-06-29T15:53:04.473606487Z","date":"May 25 16:40:10","environment":"dev","file":"/root/logging/ip_tables.log","host":"bastion","hostname":"freeipa.local.lan","pattern":"krba","payload":"freeipa.local.lan","raw_message":"May 25 16:40:10 freeipa.local.lan","status":"freeipa.local.lan","success":true}
{"@timestamp":"2025-06-29T15:53:04.473695565Z","date":"May 25 16:40:10","environment":"dev","file":"/root/logging/ip_tables.log","host":"bastion","pattern":"krbb","payload1":"closing down fd","payload2":"12","raw_message":"May 25 16:40:10 closing down fd 12","status":"closing down fd 12","success":true}
{"@timestamp":"2025-06-29T15:53:05.516553037Z","environment":"dev","file":"/root/logging/ip_tables.log","host":"bastion","log_type":"unknown_pattern_krb5","parse_error":"failed_to_match_any_pattern","raw_message":"May 25 16:40:10 20","status":"20","success":false}
```


```yaml
sources:
  app_logs:
    type: "file"
    include:
      - "/root/logging/ip_tables.log"

transforms:
  app_logs_parser:
    inputs:
      - "app_logs"
    type: "remap"
    source: |
    
      # Определяем кастомные паттерны
      patterns = {
        "krba": "%{SYSLOGTIMESTAMP:date} %{HOSTNAME:hostname}",
        "krbb": "%{SYSLOGTIMESTAMP:date} %{GREEDYDATA:krb5kdc_action} %{NUMBER:krb5kdc_fd}"
      }
      # Производим первичный парсинг полей до поля который будет срабатывать по условию  %{GREEDYDATA:action}    freeipa.local.lan или closing down fd 12
      .raw_message = .message      
      .message = parse_grok!(
        .message, "%{SYSLOGTIMESTAMP:date} %{GREEDYDATA:action}"
      )
      #.environment = "dev"
      #del(.source_type)
	  # Получили значение поля 
      .status = .message.action
      #.@timestamp = del(.timestamp)


      if .status == "freeipa.local.lan" 
        {
        #.raw_message_1 = .raw_message
        .message = parse_grok!(.raw_message, patterns.krba) 
        .environment = "dev"
        del(.source_type)
        .@timestamp = del(.timestamp)
        .date = .message.date
        .hostname = .message.hostname
        .pattern = "krba"
        .success = true
        .payload = .message.hostname
        del(.message)
      } else if .status == "closing down fd 12"  
        {
        #.raw_message_1 = .raw_message 
        .message = parse_grok!(.raw_message, patterns.krbb)
        .environment = "dev"
        del(.source_type)
        .@timestamp = del(.timestamp)
        .date = .message.date
        .pattern = "krbb"
        .success = true
        .payload1 = .message.krb5kdc_action
        .payload2 = .message.krb5kdc_fd
        del(.message)
      } else {
        .log_type = "unknown_pattern_krb5"
        .@timestamp = del(.timestamp)
        .parse_error = "failed_to_match_any_pattern"
        .environment = "dev"
        .success = false
        del(.source_type)
        del(.message)
      }


sinks:
  vector_kafka:
    type: kafka
    inputs:
      - app_logs_parser
    bootstrap_servers: 192.168.1.230:9092
    topic: ipa-topic
    encoding:
      codec: "json"
```