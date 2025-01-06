#### Описание 
#### Установка 
```
для архитектуры на                                ./K8S/infra/monotoring/images/image1.jpg
```
#### Тестироваине 

### --------------------------------------------------------------------------------
###### Описание 
```
kube-state-metrics     - это сервис, который обращается к Kubernetes API и генерирует метрики о состоянии объектов в формате prometheus


kube-state-metrics      https://github.com/kubernetes/kube-state-metrics
список метрик           https://github.com/kubernetes/kube-state-metrics/tree/master/docs
node-exporter           https://github.com/prometheus/node_exporter

```
###### Установка 
```
для архитектуры на                                ./K8S/infra/monotoring/images/image2.jpg
```
```bash 
# установка exporter 
#    - (для kube-state-metrics, критична версия в зависимости от версии в кластере) https://github.com/kubernetes/kube-state-metrics
#    - node-exporter необходимо дать доступ на чтение к файловой системе хоста (метрики собраются с хостовой системы, размещается на каждом хосте системы)
kubectl apply -f kube-state-metrics.yaml    
kubectl apply -f node-exporter.yaml  

```
###### Тестироваине 
```
```
