##### Настройка Prometheus for PushGateway

```
Настройка scraping c PushGateway не отличается от scraping с обычных exporters.

Добавляем настройки в основной конфигурационный файл Prometheus:
```
```bash
cat <<EOF >> /etc/prometheus/prometheus.yml
  - job_name: pushgateway
    honor_labels: true
    static_configs:
      - targets:
         - localhost:9091
EOF

promtool check config /etc/prometheus/prometheus.yml
# Checking /etc/prometheus/prometheus.yml
#  SUCCESS: /etc/prometheus/prometheus.yml is valid prometheus config file syntax


# Применяем настройки:
systemctl reload prometheus.service

```

```

#  проверкa
Выполните запрос в UI Prometheus:
test_job_edu_counter[1m]
В ответ вы должны получить вектор:
# test_job_edu_counter{instance="monitoring.test", job="test_job", type="counter"}	42

```