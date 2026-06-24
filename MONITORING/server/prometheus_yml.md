```yaml
# Путь к конфигурационному файлу задается через ключ: --config.file при запуске prometheus
# В конфигурационном файле не допускаются символы табуляции, только пробелы
#

# my global config
global:
  # Как часто собирать данные, значение по умолчанию.
  # [ scrape_interval: <duration> | default = 1m ]
  scrape_interval: 15s     # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  
  # Значение тайм-аут для процесса сбора данных, значение по умолчанию.
  # scrape_timeout is set to the global default (10s).
  # [ scrape_timeout: <duration> | default = 10s ]

  # Как часто перечитывается список правил.
  # [ evaluation_interval: <duration> | default = 1m ]

  # Метки, добавляем по умолчанию.
  # external_labels:
  # [ <labelname>: <labelvalue> ... ]


# Alertmanager configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
# Файл со списком правил
rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
# Конфигурация для сбора данных.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090"]
       # The label name is added as a label `label_name=<label_value>` to any timeseries scraped from this config.
        labels:
          app: "prometheus"
```