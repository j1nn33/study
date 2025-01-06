#### Описание 
#### Установка 
```
для архитектуры на                                ./K8S/infra/monotoring/images/image1.jpg
```
#### Dashboards 
```

```


###### Описание 
```
Дашбоды                  https://grafana.com/grafana/dashboards
Список метрик:           https://github.com/kubernetes/kube-state-metrics/tree/master/docs
node-exporter dashboard: https://grafana.com/grafana/dashboards/1860

```
###### Установка 
```
для архитектуры на                                              ./K8S/infra/monotoring/images/image1.jpg
statefullstate - сервис 
Установка производится в кластер k8s с учетом созданного NFS    ./study/K8S/infra/NFS/readme.md
в конфигурацию добавляем datasource victoriametrics
с учетом созднного ingress                                      ./K8S/infra/monotoring/utils/ingress.yml


kubectl apply -f 01-configmaps.yaml
kubectl apply -f 02-grafana-deployment.yaml

Доступ 

https://192.168.1.171:30443/grafana/login
admin
admin


```
###### Dashboards 
```
Дашбоды                  https://grafana.com/grafana/dashboards
Список метрик:           https://github.com/kubernetes/kube-state-metrics/tree/master/docs
node-exporter dashboard: https://grafana.com/grafana/dashboards/11074
                         https://grafana.com/grafana/dashboards/15172

k8s                      https://grafana.com/grafana/dashboards/8685

```

```
как допилить дашборд

1 - там где нет данных смотрим как называется метрика 
для дашборда 8685 / Cluster CPU Capacity / метрика -  kube_node_status_capacity_cpu_cores

2 - идем в prometeus и ищем похожую метрику kube_node_status_capacity 
kube_node_status_capacity{instance="kube-state-metrics.kube-system.svc.cluster.local:8080", job="kube-state-metrics", node="control1.kube.local", resource="cpu", unit="core"}

3 - идем в дашборд и делаем 
kube_node_status_capacity{resource="cpu"}
sum(kube_node_status_capacity{resource="cpu"})
игарем по значениям sum() не sum

```