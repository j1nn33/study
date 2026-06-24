##### Настройка Alertmanager

```
Настройка Alertmanager производится как с помощью ключей, так и с помощью
конфигурационного файла. Формат – yaml. 
В конфигурационном файле настраивается вся обработка алертов. 
Конфигурационный файл может содержать 5 блоков.

```

##### Блок global

```
resolve_timeout
# default: 5m Время, через которое алерт считается решенным, если в течение этого времени он не был обновлен.

smtp_from 
# default: – email адрес, который будет использован в качестве адреса отправителя. 
# В блоке global объявляются значения по умолчанию, переопределить которые можно в блоке receiver.

smtp_smarthost
# default:
# Адрес SMTP сервера, который используется для отправки. 
# Формат: ip:port . 
# В блоке global объявляются значения по умолчанию, перепределить которые можно в блоке receiver.

smtp_require_tls
# default: true
# Задает, использовать ли tls при подключении к SMTP. Обратите внимание, что
# значение по умолчанию true и при использовании с локально установленным postfix без
# дополнительных настроек работать не будет.

# Также в этой секции возможно настроить отправку уведомлений в: slack, hipchat,  pagerduty и другие мессенджеры. 
# Но для настройки получателей рекомендуется
# использовать webhook. Его настройка возможна только в разделе receivers.

```
##### Блок route
```

# В блоке route производится маршрутизация сообщений. 
# В результате получается древовидная структура.

receiver
# Имя конфигурации, которая будет использована для отправки уведомлений.

group_by
# Набор меток, по которым производится агрегация. Значение ['...'] отключает группировку.

сontinue
# default: false
# Если значение false, обработка уведомления прекращается при первом совпадении. Если
# значение true, обработка продолжается и выбирается последний route, удовлетворяющий условиям.

match
# Список меток key: value, при точном совпадении с которыми выбирается этот маршрут.

match_re
# Список меток key: regex, при совпадении с которыми выбирается этот маршрут.

group_wait
# Default: 30s
# Время задержки перед отправкой сообщений для группы. Позволяет дождаться
# поступления большего числа алертов и произвести эффективную группировку.

group_interval
# default: 5m
# Время задержки для отправки новых уведомлений, по которым первоначальное
# уведомление уже было отправлено.

repeat_interval
# default: 4h
# Время задержки для повторной отправки уведомления.

routes
# Дополнительные маршруты. Не являются обязательными.

```

```yaml

route:
  receiver: 'default-receiver'
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  group_by: [cluster, alertname]
  routes:
    - receiver: 'db-team'
      group_wait: 10s
      match_re:
        service: mysql|postgres
    - receiver: 'frontend-team'
      group_by: [product, environment]
      match:
        team: frontend

```

```
все уведомления labels service со значениями mysql или postgres будут отправлены db-team. 
Уведомления, имеющие label team со значением frontend,          будут отправлены frontend-team. 
Остальные уведомления будут отправлены получателю по умолчанию.

```

##### Блок receivers
```
Receiver – это именованная конфигурация одного или нескольких получателей уведомлений. 
для настройки получателей рекомендуется использовать webhook. 
В настройках указываются данные для отправки. 

```

##### Блок inhibit_rules
```
# Блок inhibit_rules позволяет отключить уведомления для алертов, у которых labels
# соответствуют набору labels, указанных в target_match(_re), и при условии, что уже есть
# уведомление, у которого набор labels соответствуют набору labels, указанных в source_match(_re).

target_match
# Список labels, при совпадении с которым сообщение будет отключено.

target_match_re
# Список labels, при совпадении с которым сообщение будет отключено. Для проверки
# используется регулярное выражение.

source_match
# Набор меток, для которых уже должен существовать алерт, чтобы правило подавления работало.

source_match_re
# Набор меток, для которых уже должен существовать алерт, чтобы правило подавления
# работало. Для проверки используется регулярное выражение.

equal
# Набор label, которые должны совпадать в alert и inhibit alert, чтобы подавление работало.


```
##### Блок templates

```
В данном блоке задается список путей для файлов с пользовательскими шаблонами
уведомлений. Допускается использование маски.

templates:
  - 'templates/*.tmpl

```



##### конфигурационный файл

```bash
/etc/alertmanager/alertmanager.yml

```

```yaml

global:
  smtp_smarthost: smtp.yandex.ru:465
  smtp_from: '<user name>@mail.ru'
  smtp_auth_username: '<user name>@mail.ru'
  smtp_auth_password: '<Password>'

route:
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 1h
  receiver: team-monitoring

routes:
  - match:
      service: prom
    receiver: team-ops
  - match:
      severity: (warnings|error|critical)
    receiver: team-monitoring

inhibit_rules:
  - source_match:
      severity: 'critical'
      alertname: PrometheusConfigurationReload
    target_match:
      severity: 'error'

receivers:
  - name: 'team-ops'
    email_configs:
      - to: '<email_1>'
          send_resolved: true
          require_tls: false
  - name: 'team-monitoring'
    email_configs:
      - to: '<email_2>'
          send_resolved: true


```


```
Данная конфигурация использует группировку по alertname и service. 
Все сообщения с label service: prom будут отправлены на email_1, все алерты c label severity: critical, error и
warning будут отправлены на email_2. 
Если есть алерт c label service: prom и alertname:
PrometheusConfigurationReload, остальные алерты отправляться не будут.

для его визуализации можно воспользоваться сайтом
https://prometheus.io/webtools/alerting/routing-tree-editor/
```

```bash

systemctl reload alertmanager.service

```
##### TESTING

```bash
# Исправляем конфиг Prometheus.
# Добавляем в начало конфигурационного файла Prometheus: 1.

vim /etc/prometheus/prometheus.yml
systemctl reload prometheus.service

# Это приведет к отправке алерта об ошибке в конфигурационном файле Prometheus.

http://192.168.1.236:9090/alerts


# Исправляем конфигурационный файл: /etc/prometheus/prometheus.yml, удаляем 1.
systemctl reload prometheus.service

# Теперь должно прийти еще 2 уведомления: первое – об исправлении с конфигурацией
# Prometheus, второе – о недоступности двух exporters.
```

