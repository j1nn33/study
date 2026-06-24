##### Настройка Alert Rules

```
Alert Rules очень похожи на Record Rules, рассмотренные в предыдущей главе. Они
располагаются в тех же группах, что и rules. Допускается комбинировать alert и record
rules в одном файле

```

```yaml

groups:
  - name: node_rules
    rules:
  - record: job:up:avg
    expr: avg without(instance)(up{job="node_exporter"})
  - alert: ManyInstancesDown
    expr: job:up:avg{job="node_exporter"} < 0.5

```

###### Синтаксис Alert Rules

```
Правила уведомлений формируются по группам

```

```yaml

groups:
  - name: example
    rules:
  - alert: ManyInstancesDown
    for: 5m
    expr: avg without(instance)(up{job="node_exporter"}) * 100 < 50
    labels:
      severity: warning
    annotations:
      summary: 'More than half of instances are down.'
      dashboard: http://192.168.1.236:3000/dashboard/db/prometheus
```

```
name        – это имя для группы правил. Оно должно быть уникальным и является обязательным.
alert       – это имя алерта.
for         – задержка с момента выполнения условий для срабатывания до начала обработки.
              Пока условие for не выполнено, данные в Alertmanager не отправляются.
expr        – задает условие, и если оно истинное, то начинается обработка alert.
labels      – задет произвольный набор labels для alert. 
              alert labels никак не связаны с metrics labels и используются для обработки алертов на стороне Alertmanager.
annotations – набор дополнительных произвольных меток (ключ: значение), которые
              передаются вместе с алертом. 
              В отличие от меток, которые передаются в labels, метки из
              annotations не используются для группировки и маршрутизации уведомлений.

alert annotation поддерживает шаблоны GO, а также PromQL запросы. 
Например, можно добавить список недоступных node_exporter

description: >
  Down instances: {{ range query "up{job=\"node\"} == 0" }}
    {{ .Labels.instance }}
  {{ end }}


```