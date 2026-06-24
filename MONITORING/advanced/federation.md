#####  Настройка Prometheus Federation
```bash
# Настройка Prometheus.

vim /etc/prometheus/prometheus.yml

```

```yaml
global:
  scrape_interval: 15s 
  evaluation_interval: 15s 

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - localhost:9093

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
  - job_name: 'node_exporter'
    static_configs:
      - targets:
         - localhost:9100

```
```bash
# Настройка Federation

vim /etc/prometheus/prometheus.yml
```
```yaml
global:
  scrape_interval: 15s 
  evaluation_interval: 15s 

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - localhost:9093

scrape_configs:
  - job_name: "federate"
    honor_labels: true
    metrics_path: '/federate'

    params:
      match:
        - '{ job="prometheus" }'
        - '{__name__=~"job:.*"}'
    static_targets:
      - source-prometheus-1:9090
      - source-prometheus-2:9090
```

```
endpoint /federate    позволяет получить значения все метрики одним запросом.
honor_labels: true    позволяет выставить приоритет labels
                      источника, что позволяет сохранять значения для labels: job и instance.
match                 является обязательным. С его помощью задается, для каких метрик
                      будет производиться scraping. Фильтрация производится на основание labels.


# Проверка работы.
Открываем в браузере: 

http://<monitoring>/targets. Должно отображаться два сервера.
                             задержка возможна мин 15


```