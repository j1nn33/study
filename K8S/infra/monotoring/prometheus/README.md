#### Описание 
#### Установка 
```
для архитектуры на                                ./K8S/infra/monotoring/images/image1.jpg
```
#### Конфигурации собираемых метрик (описание)
```
    - мониторинг самого prometeus         ./study/K8S/infra/monotoring/prometheus/config/01-configmap-prometheus.yaml 
    - Метрики API сервера                 ./study/K8S/infra/monotoring/prometheus/config/01-configmap.yaml 
    - Метрики Kubelet                     ./study/K8S/infra/monotoring/prometheus/config/02-configmap.yaml
    - Метрики Kubelet cadvisor            ./study/K8S/infra/monotoring/prometheus/config/03-configmap.yaml
    - Метрики nodelocaldns                ./study/K8S/infra/monotoring/prometheus/config/04-configmap.yaml
    - Метрики kube-controller             ./study/K8S/infra/monotoring/prometheus/config/05-configmap.yaml
    - Метрики kube-scheduller             ./study/K8S/infra/monotoring/prometheus/config/06-configmap.yaml
    - Метрики node-exporter               ./study/K8S/infra/monotoring/prometheus/config/07-configmap.yaml
    - Метрики kube-state-metrics          ./study/K8S/infra/monotoring/prometheus/config/08-configmap.yaml
    - Метрики ingress-nginx-endpoints     ./study/K8S/infra/monotoring/prometheus/config/09-configmap.yaml
    - сбор метрик с etcd

```
#### Тестироваине 

### --------------------------------------------------------------------------------
###### Описание 
```
Документация            https://prometheus.io/
Докер контейнер         https://quay.io/repository/prometheus/prometheus?tab=info
Пример конфигурации     https://github.com/prometheus/prometheus/blob/master/documentation/examples/prometheus-kubernetes.yml

```
###### Установка 
```
для архитектуры на     ./K8S/infra/monotoring/images/image2.jpg

установка prometeus производится в кластер k8s с учетом созданного NFS                     ./study/K8S/infra/NFS/readme.md

deployment prometheus ./K8S/infra/monotoring/prometheus/prometheus_manifest/03-prom-deployment.yaml
deployment имеет два service 
    prometheus-sys
    prometheus-sys-connect   для statefullse 
statefullset необходим для того чтобы выдать pod определенное имя prometheus-sys-0 
к которому можно обратиться по selector (если подов будет много, обращение будет только на один)

web.external-url - как обратиться к prometeus  http://192.168.1.171:30180/prometheus/     

```
```bash
# Установка конфигурации (подробнее по разбор см. ниже)


# установка prometheus ./K8S/infra/monotoring/prometheus/prometheus_manifest/03-prom-deployment.yaml

kubectl apply -f 03-prom-deployment.yaml

# Доступ к prometheus Grafana
    ./K8S/infra/monotoring/utils/ingress.yml

https://192.168.1.171:30443/prometheus
https://192.168.1.171:30443/prometheus/targets

# Получение метрик (если не доступны смотрим обращения к prometheus-sys-connect)
http://192.168.1.171:30180/prometheus/metrics


```



###### Конфигурации собираемых метрик (описание)
```
01 - мониторинг самого prometeus  ./K8S/infra/monotoring/prometheus/config/01-configmap-prometheus.yaml
```
```yaml
---
  prometheus.yml: |
    global:
      scrape_interval:     15s                                       # интервал обращения к метрикам 
      external_labels:
        monitor: 'k8s-dev-monitor'
    remote_write:
      - url: http://victoriametrics-sys-connect:8428/api/v1/write    # куда сливать данные prometheus (имя сервиса victoriametrics)

    scrape_configs:
      - job_name: 'prometheus'                                       # job prometheus который собирает метрики  https://prometheus.io/docs/introduction/first_steps/
        scrape_interval: 15s
        metrics_path: /prometheus/metrics                            # где живут метрики самого prometheus
        static_configs: 
          - targets: ['localhost:9090']
```
```
01 - Метрики API сервера   
https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config
```
```yaml
    scrape_configs:
      # Метрики API сервера
      - job_name: 'kubernetes-apiservers'
        kubernetes_sd_configs:
        - role: endpoints         # обращение к endpoints
          namespaces:
            names:       
              - default           # имя namespaces
        scheme: https
        tls_config:
          # у любого пода в k8s есть сертификт лежаций по этому пути 
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
          # у любого пода в k8s есть token лежаций по этому пути при обращении к API сервера 
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
        relabel_configs:
          # вибираем все у кого __meta_kubernetes_service_name = kubernetes (Service = kubernetes)
          # и __meta_kubernetes_endpoint_port_name = https                   
        - source_labels: [__meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
          action: keep
          regex: kubernetes;https
```
```
02 - Метрики Kubelet
```
```yaml
 # Kubelet
      # kubelet_certificate_manager_client_ttl_seconds / 60 / 60 /24
      - job_name: 'kubernetes-nodes'
        kubernetes_sd_configs:
        - role: node           # обращение к node  

        scheme: https
        tls_config:
          ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
          insecure_skip_verify: true
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token

        relabel_configs:
        - action: labelmap
          # обращение к ноде по лейбам (.+) - все что угодно
          regex: __meta_kubernetes_node_label_(.+)  
```
```
03 - Метрики Kubelet cadvisor
     дополнительные метрки которы дают более подробную информацию о контейнерах котрые крутятся на данной ноде 
04 - Метрики nodelocaldns 
     обращаемся напрямую к pod по порту 9253 (задаестя при установке ./K8S/k8s_install_kubeadm/manifests/nodelocaldns-daemonset.yaml)
05 - Метрики kube-controller  
     (для сбора метрик заменено )
     replacement: $1:10257   на 127.0.0.1 
06 - Метрики kube-scheduller
     (для сбора метрик заменено )
     replacement: $1:10259   на 127.0.0.1 
07 - Метрики node-exporter
08 - Метрики kube-state-metrics
09 - Метрики ingress-nginx-endpoints
```

```
Cбор метрик с etcd (для etcd который внутри k8s)

Доступ к метрикам получить можно с использованием сертификатов (которые необходимо обновлять)
```
```bash

/etc/kubernetes/pki/apiserver-etcd-client.crt
/etc/kubernetes/pki/apiserver-etcd-client.key

# Проверить наличие метрик 
curl --cert /etc/kubernetes/pki/apiserver-etcd-client.crt \
  --key /etc/kubernetes/pki/apiserver-etcd-client.key  \
  --cacert /etc/kubernetes/pki/ca.crt --insecure \
  https://192.168.1.171:2379/metrics

# Создаём secret
kubectl -n monitoring create secret generic etcd-client \
  --from-file=/etc/kubernetes/pki/apiserver-etcd-client.key \
  --from-file /etc/kubernetes/pki/apiserver-etcd-client.crt

# Подключаем его как volume к контейнеру prometheus 
# которые пробросятся в mountPath: /opt/prometheus/secrets
# ./K8S/infra/monotoring/prometheus/etcd/02-prom-deployment.yaml


```

###### Тестироваине 
```
```
