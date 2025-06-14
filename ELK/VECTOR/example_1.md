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

