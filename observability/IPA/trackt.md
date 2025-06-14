
#### Тракт логов 
выстраивание тракта для логов по  

1 LOGGING 	ver 1
vector(1) ---> kafak ---> vector(2) ---> elasticsearch ---> kibana (dashboard)
======================================

192.168.1.230   kafka
192.168.1.1     monitoring
192.168.1.162   ELK 

======================================
###### vector(1)

отправка лога 
echo "Mar 15 12:18:46 hostname.realm.ru kernel: IP limit exceeded IN=enp0s9 OUT=enp0s3 MAC=08:00:27:df:e0:96:08:00:27:e1:23:4b:08:00 SRC=192.168.176.4 DST=8.8.8.8 LEN=62 TOS=0x00 PREC=0x00 TTL=63 ID=62689 DF PROTO=UDP SPT=44611 DPT=53 LEN=42" >> /root/logging/ip_tables.log

чтобы добититься эффекта как на рис 4 выносим все поля в json на 1 уровень

Потестировать события можно череза парсер 
https://playground.vrl.dev/

рис 5 

vector --config tract_vector_1_v1.yaml

cat tract_vector_2_v2.yaml
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
      .raw_message = .message      
      .message = parse_grok!(
        .message, "%{SYSLOGTIMESTAMP:date} %{HOSTNAME:hostname} kernel: IP limit exceeded %{NOTSPACE:in} %{NOTSPACE:out} %{NOTSPACE:mac} SRC=%{IP:source_ip} DST=%{IP:destination_ip}"
      )
      .environment = "dev"
      del(.source_type)
      .@timestamp = del(.timestamp)                 # добавляем те поля которые планируем использовать в индексе 
      .date = .message.date
      .destination_ip = .message.destination_ip
      .hostname = .message.hostname
      .in = .message.in
      .mac = .message.mac
      .out = .message.out
      .source_ip =.message.source_ip
      del(.message)
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
###### kafka 

На стороне кафка заранее создали топик 

```bash
/opt/kafka/bin/kafka-topics.sh --create --topic ipa-topic --bootstrap-server $(hostname -f):9092
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server $(hostname -f):9092 --topic ipa-topic --from-beginning
/opt/kafka/bin/kafka-topics.sh --list --bootstrap-server $(hostname -f):9092

/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server $(hostname -f):9092 --topic ipa-topic 

{"@timestamp":"2025-06-13T10:49:53.851311333Z",
 "environment":"dev",
 "file":"/root/logging/ip_tables.log",
 "host":"bastion","message":{"date":"Mar 15 12:18:46","destination_ip":"8.8.8.8",
 "hostname":"hostname.realm.ru",
 "in":"IN=enp0s9",
 "mac":"MAC=08:00:27:df:e0:96:08:00:27:e1:23:4b:08:00",
 "out":"OUT=enp0s3","source_ip":"192.168.176.4"},
 "raw_message":"Mar 15 12:18:46 hostname.realm.ru kernel: IP limit exceeded IN=enp0s9 OUT=enp0s3 MAC=08:00:27:df:e0:96:08:00:27:e1:23:4b:08:00 SRC=192.168.176.4 DST=8.8.8.8 LEN=62 TOS=0x00 PREC=0x00 TTL=63 ID=62689 DF PROTO=UDP SPT=44611 DPT=53 LEN=42"
}
```

###### vector(2)

```yaml
sources:
  kafka-iptables:                                # имя потока 
    type: "kafka"
    bootstrap_servers: "192.168.1.230:9092"
    group_id: "loggers"
    key_field: "message_key"
    topics:
      - ipa-topic

transforms:
  transform-iptables:
    type: remap
    inputs:
      - kafka-iptables
    timezone: local
    source: |-
      . = parse_json!(.message)
      del(.source_type)                          # удаление технических полей 
      del(.topic)
      del(.partition)
      del(._score)
      del(.message_key)
      del(.offset)
sinks:
  es-iptables:
    inputs:
      - transform-iptables 
    type: elasticsearch
    # endpoint: "https://opensearch-cluster-master.es.svc:9200"
    endpoints:
      - "http://192.168.1.162:9200"
    # suppress_type_name: true
    bulk:
      action: "create"
      index: 'iptables-%Y-%m-%d-%H'             # Создание часовых индексов 
    #tls:
    #  verify_certificate: false
    auth:
      user: admin
      password: admin
      strategy: basic

```
###### elasticsearch

1 Создаем патерн индекса и должны получить то что на картинке 
 рис 4

###### kibana (dashboard)

Создаине визуализации ./study/observability/kibana_dasboard.md