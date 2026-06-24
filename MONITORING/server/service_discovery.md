### Service Discovery

##### Настройка scraping с использованием static_config

```bash
cat <<EOF >> /etc/prometheus/prometheus.yml
  - job_name: 'static_config'
    static_configs:
      - targets:
         - localhost:9100
         - 192.168.1.236:9100
        labels:
          sd: static
EOF

```

```
# хост задается с указанием порта, по которому необходимо проводить scraping.
# С помощью директивы labels указывается, что ко всем метрикам будет добавлена метрика sd со значением static

```

```bash
promtool check config /etc/prometheus/prometheus.yml
systemctl reload prometheus.service



http://192.168.1.236:9090/targets
```

##### Настройка service discovery с использованием файлов

```bash

#  Создаем каталог для хранения правил service discovery и выставляем на него права

mkdir /etc/prometheus/sd
chown prometheus:prometheus /etc/prometheus/sd

# Создадим файл со списком хостов:

cat <<EOF > /etc/prometheus/sd/node_exporter.yml
- targets:
  - localhost:9100
  - 192.168.1.236:9100
  labels:
    sd: file
EOF


# Добавляем настройку в основной конфиг Prometheus:
cat <<EOF >> /etc/prometheus/prometheus.yml
  - job_name: 'file_sd'
    file_sd_configs:
      - files:
        - /etc/prometheus/sd/*.yml
        refresh_interval: 1m
EOF

# file_sd_config - что будет использоваться discovery на основании файлов.
#
# files задается список файлов, на основании которых будет
# производиться service discovery. Допускается использование регулярных выражений.
#
# refresh_interval задается, как часто Prometheus будет
# перечитывать информацию из файлов

systemctl reload prometheus.service

```

##### Настройка service discovery с использованием api openstack
```
внешний источник service discovery (их много openstack, consul)

```

```bash
cat <<EOF >> /etc/prometheus/prometheus.yml
  - job_name: 'openstack'
    openstack_sd_configs:
    - identity_endpoint: https://api.openstack.local/identity/v3
      port: 9100
      domain_name: '<domain_name>'
      username: '<user_name>' 
      project_name: '<project_name>'
      password: '<Password>'
      role: 'instance'
      region: '<Region>' 
      refresh_interval: 30s
EOF

systemctl reload prometheus.service


```