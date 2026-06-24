#### MONITORING PROMETEUS
```
CLIENT                                             /client
- структура http (как выглядят метрики)            - http_sructure.md                       
- node exporter                                    - node_exporter.md
- node exporter (добавить метрику из файла)        - node_exporter_add_metrics_from_file.md
- blackbox exporter                                
     - install                                     - blackbox_install.md
     - настройка + ICMP                            - blackbox_setup_ICMP.md
     - DNS                                         - blackbox_DNS_TCP.md
     - TCP 
     - HTTP                                        - blackbox_HTTP.md
     - настройка на prometeus blackbox_exporter
- custom exporter                                  - custom_exporter.md

```

```
SERVER                                             /server
- Prometheus                                       - prometeus.md
- ServiceDiscovery                                 - service_discovery.md
- Labas                                            - label.md 
- Push Gateway                                     - push_gateway.md
- настройка на prometeus Push Gateway              - prometheus_push_gateway.md
- настройка на prometeus blackbox_exporter         - prometheus_for_blackbox.md

```

```
PromQL                                             /PromQL 
- Типы данных в PromQL                             - type_of_data.md
- функции и labels                                 - function_label.md
      Математические функции
      Функции времени и даты
      Функции для сounter
      labels                                       -label.md

- Rules                                       
      Настройка Rules                              - rules.md
      Именование Rules

```

```
Alerting                                           /alering
 - Настройка Alert Rules                           - alert_rules.md
 - Добавление правил уведомлений                   - add_rules.md

Alertmanager
 - Установка Aletrmanager                          - install_alertmanager.md
 - Ключи запуска Alertmanager
 - Настройка Alertmanager                          - alertmanager.md
 - Настройка Alertmanager HA                       - install_HA.md
```

```
Grafana                                            /grafana

```

```
Advanced usage of prometheus                       /advancerd          
-  
- High Availability                                - ha.md
    - Настройка Prometheus в режиме HA
    - Настройка HA Proxy                           - ha_proxy.md

- Federation                                       - federation.md
- Remote Read Write                                - remote_rw.md
- HTTP API  
    - Общие сведения для запросов API              - http_api_1.md
    - Поиск временных рядов на основании labels    
    - API для получения конфигурации               - http_api_2.md
    - Rules и Alerts API                                              
```