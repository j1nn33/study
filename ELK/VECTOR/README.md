#### INSTALL и тестовый стенд 
###### Генератор логов 
###### INSTALL
#### WORK 
#### Парсинг VRL
#### Парсинг grok to json

##### INSTALL и тестовый стенд 
###### Генератор логов  

```bash
mkdir logging
cd logging

mkdir log_gen
cd log_gen

sudo mkdir /var/log/loggen
vim loggen.sh

```
```bash
#!/bin/bash
# function creates a log entry in the JSON format
# {"status": 200, "ip": "127.0.0.1", "level": 30, "emailAddress": "user@mail.com", "msg": "Task completed successfully", "pid": 12655, "ssn": "407-01-2433", "time": 1694551048}
filepath="/var/log/loggen/app.log"

create_log_entry() {
    local info_messages=("Connected to database" "Task completed successfully" "Operation finished" "Initialized application")
    local random_message=${info_messages[$RANDOM % ${#info_messages[@]}]}
    local http_status_code=200
    local ip_address="127.0.0.1"
    local emailAddress="user@mail.com"
    local level=30
    local pid=$$
    local ssn="407-01-2433"
    local time=$(date +%s)
    local log='{"status": '$http_status_code', "ip": "'$ip_address'", "level": '$level', "emailAddress": "'$emailAddress'", "msg": "'$random_message'", "pid": '$pid', "ssn": "'$ssn'", "time": '$time'}'
    echo "$log"
}

while true; do
    log_record=$(create_log_entry)
    echo "${log_record}" >> "${filepath}"
    sleep 3
done

```

###### INSTALL VECTOR

```bash

bash -c "$(curl -L https://setup.vector.dev)"
sudo apt install vector
vector --version

sudo systemctl stop vector

/etc/vector/vector.yaml


# sources:  # this section defines the data sources that Vector should read.
#   <unique_source_name>:
#     # source configuration properties go here
# 
# transforms 
#   <unique_transform_name>:
#     # transform configuration properties go here
# 
# sinks: # defines the destinations where Vector should route the data
#   <unique_destination_name>:
#     # sink configuration properties go here
	
```yaml
sources:
  app_logs:
    type: "file"
    include:
      - "/var/log/loggen/app.log"

sinks:
  print:
    type: "console"
    inputs:
      - "app_logs"
    encoding:
      codec: "json"
```

```bash
vector validate /etc/vector/vector.yaml

```
###### WORK

```bash
systemctl restart vector
# смотреть логи в режиме реального времени
vector --watch-config
vector --config /etc/vector/vector.yaml
vector --config /etc/vector/*.yaml


# Multiple files
vector --config vector1.yaml --config vector2.yaml

# config 
vector validate /etc/vector/vector.yaml

# куда кидать лог

echo '{"status": 200, "ip": "127.0.0.1", "level": 30, "emailAddress": "user@mail.com", "msg": "Task completed successfully", "pid": 12655, "ssn": "407-01-2433", "time": 1694551048}' >> /var/log/loggen/app.log


```
###### Парсинг VRL
```bash 
# Работа с  парсером https://playground.vrl.dev/

# Входящий лог 
{"file":"/var/log/logify/app.log",
        "host":"vector-test",
		"message":"{\"status\": 200, \"ip\": \"127.0.0.1\", \"level\": 30, \"emailAddress\": \"user@mail.com\", \"msg\": \"Task completed successfully\", \"pid\": 12655, \"ssn\": \"407-01-2433\", \"time\": 1694551048}","source_type":"file",
		"timestamp":"2023-09-12T20:40:21.582883690Z"}

# Получить значение переменной host
. = .host

"vector-host"
# Распарсить message
., err = parse_json(.message)

# 1 - .message: returns the entire string within the message field.
# 2 - parse_json(.message): The method parses the JSON data.
# 3 - ., err: If parsing JSON is successful, the . is set to the result of calling the parse_json() method; otherwise, the err variable is initialized.

# ========================

# Работа с внутренним парсером

vi input.json
vector vrl --input input.json

# Получить весь лог на выходе 
.

# Получить имя хоста 
.host
"vector-test"

# =====================
# Adding and removing fields with Vector


/etc/vector/vector.yaml
transforms:
  app_logs_parser:
    ...
    source: |
      # Parse JSON logs
      ., err = parse_json(.message)

      # Remove emailAddress field
      del(.emailAddress)

      # Add an environment field
      .environment = "dev"


# Formatting dates with Vector
# Format date to the ISO format
      .time = from_unix_timestamp!(.time)
      .time = format_timestamp!(.time, format: "%+")
# Добавление дополнительного поля success в зависимости от значения

if .status == 200 {
    .success = true
} else {
    .success = false
}


### Redacting sensitive data
### маскирование некторых полей чувствительных данных

# Redact field values
      . = redact(., filters: ["us_social_security_number", r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$'])


### фильтр на VRL отсекает логи с severity = info

[transforms.filter_severity]
type = "filter"
inputs = ["logs"]
condition = '.severity != "info"'

### удалять такие лейблы

[transforms.sanitize_kubernetes_labels]
type = "remap"
inputs = ["logs"]
source = '''
  if exists(.pod_labels."controller-revision-hash") {
    del(.pod_labels."controller-revision-hash")
  }
  if exists(.pod_labels."pod-template-hash") {
    del(.pod_labels."pod-template-hash")
  }


### как несколько строк лога можно объединить в одну:

[transforms.backslash_multiline]
type = "reduce"
inputs = ["logs"]
group_by = ["file", "stream"]
merge_strategies."message" = "concat_newline"
ends_when = '''
  matched, err = match(.message, r'[^\]$');
  if err != null {
    false;
  } else {
    matched;
  }
  
### В этом случае поле merge_strategies  добавляет символ новой строки в поле сообщения. 

```	  

###### Парсинг grok to json
```bash 
#  Преобразование и обогащение лога в json

# как докинуть лог 
echo 'time="2023-12-12T17:32:44Z" level=info msg="getRepoObjs stats" application=argocd/longhorn build_options_ms=0 helm_ms=14 plugins_ms=0 repo_ms=13 time_ms=126 unmarshal_ms=97 version_ms=0' >> app.log

# как проверить 

vector --watch-config
vector --config /etc/vector/vector.yaml

# Исходный лог
time="2023-12-12T17:32:44Z" level=info msg="getRepoObjs stats" application=argocd/longhorn build_options_ms=0 helm_ms=14 plugins_ms=0 repo_ms=13 time_ms=126 unmarshal_ms=97 version_ms=0

# grok parser
https://www.javainuse.com/grok
# Что получили на выходе 

{"file":"/var/log/loggen/app.log","host":"bastion","message":"time=\"2023-12-12T17:32:44Z\" level=info msg=\"getRepoObjs stats\" application=argocd/longhorn build_options_ms=0 helm_ms=14 plugins_ms=0 repo_ms=13 time_ms=126 unmarshal_ms=97 version_ms=0","source_type":"file","timestamp":"2025-04-27T09:09:04.387686470Z"}

# конифиг 

cat  /etc/vector/vector.yaml
---
sources:
  app_logs:
    type: "file"
    include:
      - "/var/log/loggen/app.log"

transforms:
  app_logs_parser:
    inputs:
      - "app_logs"
    type: "remap"
    source: |
      parsed, err_parsed = parse_grok(
        .message,
        "time=\"%{TIMESTAMP_ISO8601:timestamp}\" level=%{LOGLEVEL:level} msg=\"%{GREEDYDATA:msg}\" application=%{GREEDYDATA:application} build_options_ms=%{NUMBER:build_options_ms:int} helm_ms=%{NUMBER:helm_ms:int} plugins_ms=%{NUMBER:plugins_ms:int} repo_ms=%{NUMBER:repo_ms:int} time_ms=%{NUMBER:time_ms:int} unmarshal_ms=%{NUMBER:unmarshal_ms:int} version_ms=%{NUMBER:version_ms:int}"
      )

sinks:
  print:
    type: "console"
    inputs:
      - "app_logs_parser"
    encoding:
      codec: "json"
---



```

