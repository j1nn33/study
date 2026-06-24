##### Установка Pushgateway

```
https://github.com/prometheus/pushgateway/releases
```

```bash

# Создаем пользователя для запуска Pushgateway:
useradd pushgateway --comment "Pushgateway server user" --shell /bin/false

cat /etc/passwd | grep push
# pushgateway:x:1001:1001:Pushgateway server user:/home/pushgateway:/bin/false
# Скачиваем архив с PushGateway и распаковываем его.

wget https://github.com/prometheus/pushgateway/releases/download/v1.11.2/pushgateway-1.11.2.linux-amd64.tar.gz
tar -xvf pushgateway-1.11.2.linux-amd64.tar.gz

cd cd pushgateway-1.11.2.linux-amd64
mv pushgateway /usr/local/bin/

vim /usr/lib/systemd/system/pushgateway.service
```
```
[Unit]
Description=Prometheus Pushgateway
Documentation=https://github.com/prometheus/pushgateway
After=network.target

[Service]
User=pushgateway
Group=pushgateway
# EnvironmentFile=/etc/sysconfig/pushgateway
Restart=always
ExecStart=/usr/local/bin/pushgateway --web.listen-address=:9091 --web.telemetry-path=/metrics --persistence.file=/tmp/metric.store --persistence.interval=5m --log.level=info --log.format=json

ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s
[Install]
WantedBy=multi-user.target
```

```bash

systemctl daemon-reload
systemctl start pushgateway
systemctl enable pushgateway


# Проверяем работу.

curl -XGET -IL http://localhost:9091

# HTTP/1.1 200 OK
# Date: Sun, 09 Aug 2026 15:36:36 GMT
# Content-Type: text/html; charset=utf-8
# Transfer-Encoding: chunked

http://192.168.1.236:9091


```
###### Ключи запуска PushGateway
```

--log.level
# Default: info
# Данный ключ устанавливает уровень логирования. Возможные уровни логирования:
# debug, info, warn, error.

--log.format
# Default: logfmt
# Данный ключ устанавливает формат логов. Доступные форматы: logfmt и json.

--web.listen-address
# Default: ":9091"
# Данный ключ устанавливает адрес и порт, по которому будет доступен PushGateway.

--web.telemetry-path
# Default: "/metrics"

--web.enable-admin-api
# Default: -
# Разрешить endpoints для администрирования. Это может потребоваться для очистки данных pushgateway.

--persistence.file
# Default: -
# Файл для сохранения метрик. По умолчанию, значения метрик сохраняются только в памяти.

--persistence.interval
# Default: 5m
# Минимальное время, через которое данные будут сохранены в постоянный файл.

# Полный список ключей можно просмотреть с помощью команды help:
pushgateway --help

```

###### PushGateway API

```
Все взаимодействие с PushGateway производится через API
UI можно использовать для просмотра и очистки данных
Все labels, указанные в URL, используются в качестве ключа для группировки метрик.

Структура URL

Имя задачи и labels передаются как часть URL. Все запросы начинаются с /metrics

/metrics/job/<JOB_NAME>{/<LABEL_NAME>/<LABEL_VALUE>}


<JOB_NAME> - используется как значение label job и является обязательным.

Далее идут пары <LABEL_NAME>/<LABEL_VALUE>, 
где <LABEL_NAME> это имя label, а <LABEL_VALUE> значение этого label. 
Их количество не ограничено.


Например, метрика: 
slurm_pushgateway_test{job="test_job",instance="localhost", edu="slurm"} 

будет преобразована в:
/metrics/job/test_job/instance/localhost/edu/slurm/

Если label содержит "/", пробел или русские символы, то его необходимо закодировать в base64. А при запросе указать @base64.


```

###### Метод PUT
```

PUT запрос замещает все метрики для группы. Код ответа может быть 200 – в случае
успешного обновления, и 400 – в случае ошибки.
Если запрос выполняется с пустым body, то это приводит к удалению всех метрик для
группы. При этом push_times_seconds не обновляется.

push_times_seconds – метка времени последнего удачного POST или PUT запроса.
push_failure_time_seconds – метка времени последнего неудачного POST или PUT запроса.
```
###### Метод POST

```
POST запрос работает аналогично PUT, но обновляет значение только для метрик,
которые присутствуют в запросе.
Если запрос выполняется с пустым body, то push_times_seconds обновляется, а
изменение ранее переданных метрик не производится.
```

###### Метод DELETE

```
DELETE запрос используется для удаления метрик из PushGateway. Удаляется вся группа метрик. 
Тело запроса всегда должно быть пустым.
При успешном выполнении код ответа всегда будет 202
```

###### Отправка данных в PushGateway

```
метрика типа counter c label type
метрика типа типа guage
```

```bash
cat <<EOF | curl --data-binary @- http://127.0.0.1:9091/metrics/job/test_job/instance/monitoring.test
# TYPE test_job_edu_counter counter
test_job_edu_counter{type="counter"} 42
# TYPE test_job_gauge gauge
test_job_gauge 2398.283
EOF

# 
curl -sL http://localhost:9091/metrics/ | grep test
# push_failure_time_seconds{instance="monitoring.test",job="test_job"} 0
# push_time_seconds{instance="monitoring.test",job="test_job"} 1.786292551395539e+09
# # TYPE test_job_edu_counter counter
# test_job_edu_counter{instance="monitoring.test",job="test_job",type="counter"} 42
# # TYPE test_job_gauge gauge
# test_job_gauge{instance="monitoring.test",job="test_job"} 2398.283



# push_failure_time_seconds равный 0  - это говорит о том, что еще не было неудачных отправок данных.
# переменная push_time_seconds        - временя последней удачной отправки данных.
# группировка произведена только по labels  test_job , которые передавались в URL. 
# label type для test_job_edu_counter не учитывается

```
