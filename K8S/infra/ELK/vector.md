#### Описание 
#### установка 
#### тестироване 

###### Описание 
```
https://vector.dev/
https://vector.dev/docs/setup/installation/package-managers/helm/

# для роли routing "Stateless-Aggregator"    
https://github.com/vectordotdev/helm-charts/blob/develop/charts/vector-aggregator/values.yaml


конфигурация без ssl
```
```bash

# Define the Vector image to use
image

# Configuration for Vector's Service
service:

# откуда брать данные 
sources  

bootstrap_servers: "kafka.kafka.svc:9092"
bootstrap_servers: "192.168.1.250:9092"
topics: 
   - kube   - все логи связанные с k8s
   - host   - все логи системного приложения сервера linux

# Куда данные помещаем 
sinks
endpoint: "http://192.168.1.161:9200"   
action: "create"                           # создание индекса 
index: 'kube-%Y-%m-%d'

# persistence storage 
persistence 
# производим трансформации с данными 
transforms:

# Удаление технических полей kafka   ./K8S/infra/ELK/image/kafka_message.png
# Offset: 0   Key: empty   Timestamp: 2025-01-05 08:19:12.422 Headers: empty

# . (точка) означает корень 
. = parse_json!(.message)   # смещает корень на само сообщение (без учета тех. полей кафка)

# Преобразование вермени в сообщениях топика host из unx фомата 
# https://vector.dev/docs/reference/vrl/functions/
# "@timestamp":1736065151.0,"message":"Jan  5 11:19:11 control1 kubelet[1513]: I0105 11:19:11.939627 

# добавеляем новое поле timestamp присваиваем которому значение функции from_unix_timestamp!(.@timestamp)
# далее новое поле timestamp будет использоваться при создании патерна индексов в elastic
.timestamp = from_unix_timestamp!(.@timestamp)
# удаление первоночального значения 
del(."@timestamp")



# Преобразование вермени в сообщениях топика kube из unx фомата 
# удаление не нужных полей
del(._p)
del(."@timestamp")

# замена значений которые не понимет ELK  "." на  "_" 
# cni.projectcalico.org  
# cni_projectcalico_org
# если этого не сделать, то сообщения в ELK не заедут

if ! is_null(.kubernetes.labels) { 
  .kubernetes.labels = map_keys(value: object!(.kubernetes.labels)) -> |key| {replace(key, ".", "_")}
}
if ! is_null(.kubernetes.annotations) {
  .kubernetes.annotations = map_keys(value: object!(.kubernetes.annotations)) -> |key| {replace(key, ".", "_")}
}

```

###### установка 
```bash

helm repo add vector https://helm.vector.dev
helm repo update

helm install vector vector/vector \
  --namespace vector \
  --create-namespace \
  --values ./values-vector-opensearch.yaml


# access
kubectl -n vector exec -it statefulset/vector -- vector top

logs:     http://vector.vector:8282
metrics:  http://vector.vector:8282



# REMOVE
helm uninstall vector --namespace vector

```

###### тестироване 
```
# API to view internal metrics by running:
kubectl -n vector exec -it statefulset/vector -- vector top --url http://0.0.0.0:8686/graphql

```
