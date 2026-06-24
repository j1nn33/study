##### Настройка со стороны Prometheus для работы с Blackbox Exporter

```
Пример настроек Prometheus для произведения скрайпинга с Blackbox Exporter
```

```yaml

scrape_configs:
  - job_name: blackbox
    metrics_path: /probe
    params:
      module: [http_slurm]
    static_configs:
      - targets:
        - "https://ya.ru"
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: 127.0.0.1:9115
```

```bash 
params:
  module: [http_slurm]

# в качестве параметров запроса передаем какой модуль использовать для проверки
# Эта часть конфигурационного файла добавляет к запросу параметр module=http_slurm. 
# Здесь можно было бы передать и второй параметр, target. 
# Но в этом случае для каждого URL придется делать отдельную конфигурацию.
# Поэтому рекомендуется делать это через переопределение labels.


static_configs:
      - targets:
        - "https://ya.ru"

# в секции задается не адрес и порт exporter, а адрес проверяемого ресурса.


relabel_configs:

      - source_labels: [__address__]
        target_label: __param_target

        # source label __address__ содержится адрес exporter тот, который задается в targets.
        # Данная часть конфига копирует значение из __address__ (по сути, из targets) в
        # __param_target. Это преобразование добавляет второй параметр, target, к запросу.

  
      - source_labels: [__param_target]
        target_label: instance

        # В этой части мы значение из label __param_target записываем в instance. 
        # Это преобразование нужно, чтобы проверка каждого ресурса в label instance 
        # в качестве значения имела адрес этого ресурса.

  
      - target_label: __address__
        replacement: 127.0.0.1:9115

        # Так как в targets у нас указаны адреса проверяемых ресурсов, то нужно сказать, как
        #  подключаться к exporter. Для этого в label: __adress__ записываем адрес Blackbox.


```