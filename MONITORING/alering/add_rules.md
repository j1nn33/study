###### Добавление правил уведомлений

```bash
vim /etc/prometheus/rules_alert.yml

```
```yaml
groups:
  - name: PrometheusGroup
    rules:
      - alert: PrometheusConfigurationReload
        expr: prometheus_config_last_reload_successful != 1
        for: 1m
        labels:
          severity: critical
          service: prom
        annotations:
          summary: "Prometheus configuration reload (instance {{ $labels.instance }})"
          description: "Prometheus configuration reload error\n VALUE = {{ $value }}\n LABELS: {{$labels }}"

  - name: NodeExporterGroup
    rules:
      - alert: ExporterDown
        expr: up == 0
        for: 1m
        labels:
          severity: error
          service: prom
        annotations:
          summary: "Exporter down (instance {{ $labels.instance }})"
          description: "Prometheus exporter down\n VALUE = {{ $value }}\n LABELS: {{ $labels }}"

      - alert: HighCpuLoad
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU load (instance {{ $labels.instance }})"
          description: "CPU load is > 80%\n VALUE = {{ $value }}\n LABELS: {{ $labels }}"
      
      - alert: SystemdServiceCrashed
        expr: node_systemd_unit_state{state="failed"} == 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "SystemD service crashed (instance {{ $labels.instance }})"
          description: "SystemD service crashed\n VALUE = {{ $value }}\n LABELS: {{ $labels }}"

```
```bash
# Проверяем правила
promtool check rules /etc/prometheus/rules_alert.yml

# Добавляем данные о Rules в основной конфигурационый файл Prometheus
#   и после rule_files
#     добавляем "- rules_*.yml
vim /etc/prometheus/prometheus.yml 
```
```yaml

rule_files:
  - rules.yml
  - rules_*.yml

```
```bash
# Проверяем корректность внесенных изменений:
promtool check config /etc/prometheus/prometheus.yml

# Checking /etc/prometheus/prometheus.yml
#   SUCCESS: 2 rule files found
#  SUCCESS: /etc/prometheus/prometheus.yml is valid prometheus config file syntax
# 
# Checking /etc/prometheus/rules.yml
#   SUCCESS: 4 rules found
# 
# Checking /etc/prometheus/rules_alert.yml
#   SUCCESS: 4 rules found


# reload для Prometheus, чтобы применить новые настройки:
systemctl reload prometheus.service

# Проверяем, что правила появились
http://192.168.1.236:9090/rules


# отображается состояние всех правил
http://192.168.1.236:9090/alerts


# Тестирование работы правил.
# Отключаем node_exporter, выполнив команду:
systemctl stop node_exporter.service
```

