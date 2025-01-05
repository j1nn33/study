##### Тестовое приложение которое генерирует метрики prometeus и логи в формате json

https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/user-guides/getting-started.md

```
Оригинал с сайта не генерирует логи        ./K8S/infra/ELK/test_app/test_mon_log_app.yaml

Для того чтобы приклад генерировал логи 
необходимо использовать другой 
image fabxc/instrumented_app
                                          ./K8S/infra/ELK/test_app/test_mon_log_app.yaml


см Deploying a sample application
  
  - Deployment
  - Service
  - ServiceMonitor (расказать prometeus о приложении)

```
##### Проверка 
```
http://___:8080/metrics

dnstools# curl http://example-app:8080/
Hello from example application.dnstools#

curl http://example-app:8080/metrics
curl example-app:8080/metrics
```