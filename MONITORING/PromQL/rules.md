##### Настройка Rules

```bash
# нужны для вычисления какого либо значения и храниения результата в базе
# чтобы потом не вычилсять
# описываются в файле и файлов может быть много
# после любого изменения правил требуется, как минимум,
# выполнять reload – для того, чтобы Prometheus применил изменения

# Чтобы загрузить правила в Prometheus, список файлов с Rules необходимо взять в
# основном конфигурационном файле Prometheus.
rule_files:
  - "rules_file1.yml"
  - "rules_file2.yml"
  - "rules/*.yml"

# проверить синткасис

promtool check rules /path/to/example.rules.yml


```
###### Синтаксис rules файла

```
Все правила объединяются в группы. Правила внутри группы запускаются
последовательно, с регулярными интервалами. Разные группы выполняются в разное
время, чтобы снизить нагрузку на Prometheus.
```
```yaml
groups:
  - name: example
    interval: 10s
    rules:
    - record: job:process_cpu_seconds:rate5m
      expr: sum without(instance)(rate(process_cpu_seconds_total[5m]))
      labels:
        slurm_edu: exmple_rules
```

```
name       – это имя для группы правил. Оно должно быть уникальным и является обязательным.
interval   – интервал, с которым будет производиться выполнение и сохранение правил в
             группе. Не является обязательным. По умолчанию равен global.evaluation_interval.
record     – имя, по которому результат будет доступен при извлечении данных.
             Рекомендации по составлению будут приведены в следующем шаге. Является обязательным.
expr       – выражение, которое используется для вычисления. Является обязательным.
labels     – список меток, которые будут добавлены к вектору. Не является обязательным.
```

###### Именование Rules
```
Для Rules у Prometheus имеются рекомендации по именованию правил
   Разделителем в имени правила является ":"
   Общий вид имени должен быть таким:

level:metric:operations

level      – отражает уровень агрегации на основании labels. Он должен включать метку job и
             другие значимые labels, которые имеют отношение к метрике.
metric     – это имя метрики. Допускается удаление _total, но в остальных случаях это
             должно быть точное название исходной метрики. Для обозначения необходимо
             использовать _per_.
operations – представляет собой список функций и агрегаций, примененных к метрике.
             Если применяется несколько одинаковых функций, например min, указывать необходимо
             только одну.

Примеры 

- record: instance_path:request_latency_seconds_count:rate5m
  expr: rate(request_latency_seconds_count{job="myjob"}[5m])

- record: instance_path:request_latency_seconds_sum:rate5m
  expr: rate(request_latency_seconds_sum{job="myjob"}[5m])

- record: job:request_failures_per_requests:ratio_rate5m
  expr: |2sum without (instance, path)(instance_path:request_failures:rate5m{job="myjob"})/sum without (instance, path)(instance_path:requests:rate5m{job="myjob"})

```
###### Антипаттерны для использования Rules

```
 
  1. Не стоит перемещать значения labels в название правил, это существенно сократит
     возможность обработки данных в дальнейшем.

  2. Не стоит использовать rules для всех данных по умолчанию, это приведет к
     дополнительным накладным расходам. Как правило, 90% метрик не используются в
     повседневной работе и к ним обращаются только когда ищут источник проблем.
     Единственно когда, можно добавить правило - если без него запрос выполняется намного дольше.
  
  3. Не стоит использовать rules для исправления имен или labels. Новый временной ряд
     записывается с новой временной меткой и приводит к потере исходной временной метрики.

```

###### Настройка Rules

```bash
# Сохраняем правила в файл: rules.yml
vim /etc/prometheus/rules.yml
```
```yaml
groups:
  - name: slurm-edu-example-node-exporter-rules
    rules:
    # The count of CPUs per node, useful for getting CPU time as a percent of total.
    - record: instance:node_cpus:count
      expr: count(node_cpu_seconds_total{mode="idle"}) without (cpu,mode)
    # CPU in use by CPU.
    - record: instance_cpu:node_cpu_seconds_not_idle:rate5m
      expr: sum(rate(node_cpu_seconds_total{mode!="idle"}[5m])) without (mode)
    # CPU in use by mode.
    - record: instance_mode:node_cpu_seconds:rate5m
      expr: sum(rate(node_cpu_seconds_total[5m])) without (cpu)
    # CPU in use ratio.
    - record: instance:node_cpu_utilization:ratio
      expr: sum(instance_mode:node_cpu_seconds:rate5m{mode!="idle"}) without (mode) / instance:node_cpus:count
```

```bash
# Проверяем правила.
promtool check rules /etc/prometheus/rules.yml

# Добавляем данные о Rules в основной конфигурационый файл Prometheus. после rule_files
vim /etc/prometheus/prometheus.yml 
```
```yaml
rule_files:
  - rules.yml
```  

```bash

# Проверяем корректность внесенных изменений:
promtool check config /etc/prometheus/prometheus.yml

# reload для Prometheus, чтобы применить новые настройки:
systemctl reload prometheus.service

# Для применения изменений в prometheus.yml достаточно выполнить reload для службы. 
# Этот способ предпочтительней, так как в случае ошибки в конфигурационном
# файле просто не применятся изменения. Если же выполнить restart, то из-за ошибки весь
# Prometheus станет недоступен до устранения этой самой ошибки.

#  Проверяем, что правила появились.
http://192.168.1.236:9090/rules
```