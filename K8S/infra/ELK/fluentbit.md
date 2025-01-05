## fluentbit
##### Документация 
##### Решение (отправка логов напрямую в ELK)
##### Описание 
##### Установка  
##### Проверка
##### Установка через helm   для решения      ./K8S/infra/ELK/to_ELK/to_ELK.md



###### Документация
```
fluentbit   - собирает логи с каждой ноды каластера или пода 

https://www.fluentbit.io/
https://docs.fluentbit.io/manual/installation/kubernetes#installation
https://github.com/fluent/helm-charts

datapipeline 
INPUTS - tail (для чтения файлов типа tail -f)
PARSER - json regular expresion
FILTER - Kubernetes обогащение логов (инфа о подах, нейспасе лейбай и т.д )
       - Modify модификация логов 
 
Outputs - Elasticsearch, NFS
```
###### Решение (отправка логов напрямую в ELK)
```
решение описываемое ниже - fluentbit будет отправлять логи сразу в elasticsearch
```
###### Описание
```
Установка будет кастомной на остнове файлов из официальной установки
сбор логов приложения example-app и системных логов ноды где крутится это приложение из /var/log/
решение описываемое ниже - fluentbit будет отправлять логи сразу в elasticsearch

  ./K8S/infra/ELK/k8s_fluentbit/

./K8S/infra/ELK/k8s_fluentbit/01_flb-acc.yaml         - ServiceAccount, ClusterRole, ClusterRoleBinding, Secret (access to elasticsearch)
./K8S/infra/ELK/k8s_fluentbit/02_flb-cm.yaml          - ConfigMap. Конфигурационные файлы fluentbit.
./K8S/infra/ELK/k8s_fluentbit/03_flb-services.yaml    - Service и Endpoints для доступа ко внешнему (за пределами кластера k8s) elasticserach.
./K8S/infra/ELK/k8s_fluentbit/04_flb-ds.yaml          - DaemonSet
./K8S/infra/ELK/k8s_fluentbit/05_flb-ds-service.yaml  - Service для доступа к метрикам fluentbit
./K8S/infra/ELK/k8s_fluentbit/06_flb-sm.yaml          - ServiceMonitor для PrometheusOperator.


#######  01_flb-acc.yaml
Secret - креды к elasticsearch зашифрованныев  base64

# зашифровать 
base64 <<< 'cred'
# расшифровать
echo <cred> | base64 --decode

####### 02_flb-cm.yaml 
содержит несколько конфигурационных файлов 
чувствителен к отступами
```
```yaml
# глобальная секция SERVICE определяте параметры самого сервиса 
  fluent-bit.conf: |
    [SERVICE]   
        Flush         1
        Log_Level     info
        Daemon        off                                          # не работать в режиме демона тк запускается в контейнере 
        Parsers_File  parsers.conf                                 # имя файла где находятся парсеры см ниже 
        HTTP_Server   On                                           # внутрений HTTP_Server для получения метрик prometeus
        HTTP_Listen   0.0.0.0
        HTTP_Port     2020
    @INCLUDE input-kubernetes.conf                                 # включение дополнительных файлов 
    @INCLUDE filter-kubernetes.conf
    @INCLUDE output-elasticsearch.conf
  input-kubernetes.conf: |
    [INPUT]                                                        # сбор логов с приложения которе называется example-app
        Name              tail
        Tag               example-app.*                            # .*  важно для Parser docker
        Path              /var/log/containers/example-app-*.log  
        Parser            docker
        DB                /var/log/flb-example-app.db              # sql-lite сохранят информацию о прочитанных файла и не перечитывает их при перезапуске
        Mem_Buf_Limit     5MB
        Skip_Long_Lines   On
        Refresh_Interval  10
    [INPUT]                                                        # сбор системных логов с ноды
        Name tail
        Tag sysapp.gen.log.mail                                    # Tag позволяет накладыать маски для обработчика sysapp.gen.log или sysapp.gen
        Parser sys_log_file
        Path /var/log/mail
        db /var/log/mail.db
  filter-kubernetes.conf: |
    [FILTER]                                                      # обогащение логов 
        Name                kubernetes
        Match               example-app.*                         # какой фильтр накладыаем на логи 
        Kube_URL            https://kubernetes.default.svc.cluster.local:443         # доступ к k8s api       
        Kube_CA_File        /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        Kube_Token_File     /var/run/secrets/kubernetes.io/serviceaccount/token         
        Kube_Tag_Prefix     example-app.var.log.containers.       # <Match>+var.log.containers.
        Merge_Log           On                                    # для json логов
        Merge_Log_Key       log_processed                         # префикс для таких логов 
        K8S-Logging.Parser  Off
        K8S-Logging.Exclude Off
    [FILTER]
        Name modify
        Match sysapp.gen.log.mail
        Set app syslog                                           # добавлятеся app syslog
        Set file /var/log/mail
  output-elasticsearch.conf: |                                   # отправка идет в разные индексы в зависимости от поля Match
    [OUTPUT]
        Name            es
        Match           example-app.*                            # в идекс example-app
        Host            ${FLUENT_ELASTICSEARCH_HOST}             # определяется в daemonset
        Port            ${FLUENT_ELASTICSEARCH_PORT}
        HTTP_User       ${FLUENT_ELASTICSEARCH_USER}
        HTTP_Passwd     ${FLUENT_ELASTICSEARCH_PASSWORD}
        Logstash_Format On                                       # формат при передачи данных как и Logstash
        Logstash_Prefix example-app                              # для создания имен индексов см  https://docs.fluentbit.io/manual/pipeline/outputs/elasticsearch  Logstash_Prefi переопределяем базовый Logstash_Prefi на example-app
        Replace_Dots    On
        Retry_Limit     False
    [OUTPUT]
        Name            es
        Match           sysapp.gen.log.*                         # в идекс sysapp.gen.log
        Host            ${FLUENT_ELASTICSEARCH_HOST}
        Port            ${FLUENT_ELASTICSEARCH_PORT}
        HTTP_User       ${FLUENT_ELASTICSEARCH_USER}
        HTTP_Passwd     ${FLUENT_ELASTICSEARCH_PASSWORD}
        Logstash_Format On
        Logstash_Prefix sysapp-gen-log
        Replace_Dots    On
        Retry_Limit     False
  parsers.conf: |
    [PARSER]
        Name        docker
        Format      json
        Time_Key    time                                         # указываем в каком поле находится время
        Time_Format %Y-%m-%dT%H:%M:%S.%L                         # указываем в каком временном формате у нас логи (см оригинальные логи приложенивя)
        Time_Keep   On
    [PARSER]                                                     # кастомный парсер
        Format regex
        Name sys_log_file
        Regex (?<message>(?<time>[^ ]*\s{1,2}[^ ]*\s[^ ]*)\s(?<host>[a-zA-Z0-9_\/\.\-]*)\s.*)$
        Time_Format %b %d %H:%M:%S
        Time_Keep Off
        Time_Key time
        Time_Offset +0300                                        # если логи UTC  сдвиг на 3 часа
```
```bash
####### 03_flb-services.yaml
сервис ссылающийся на elasticsearch тк внутри k8s принято обращаться к sevice, который указвает на внешний ip и порт эластика 

####### 04_flb-ds.yaml
версию приклада в файле берем из docker hub /fluent/fluent-bit 
- image: fluent/fluent-bit:3.2.2-amd64

volumes  - монтируем для чтения логов из ноды и чтения логов прода которые лежат на ноде 
 
       /var/log/containers/<name_pod>_<name_namespace>_*.log
       /var/log/containers/*_kube-system_*.log
       /var/lib/docker/containers сюда смотрят символьные ссылки из /var/log
tolerations  размещать на всех нодах кластера 

# Если креды не подтигиваются можно явно прописать в deployment
#      ./K8S/infra/ELK/k8s_fluentbit/flb-ds_cred_without_configmap.yaml

####### 05_flb-ds-service.yaml    
для доступа prometeus к метрикам  port: 2020
за пределы кластера не выводятся

####### 06_flb-sm.yaml
prometeus оператор получает данные метрики (см мониториг подробнее)
https://docs.fluentbit.io/manual/administration/monitoring

curl -s http://127.0.0.1:2020/api/v1/metrics/prometheus
```
###### Установка 
```bash
kubectl apply -f 01_flb-acc.yaml
kubectl apply -f 02flb-cm.yaml
kubectl apply -f 03_flb-services.yaml
kubectl apply -f 04_flb-ds.yaml 
kubectl apply -f 05_flb-ds-service.yaml
kubectl apply -f 06_flb-sm.yaml
```
###### Проверка  
```bash
# Проверка проводится с пода dnstools
kubectl run -it --rm --restart=Never --image=infoblox/dnstools:latest dnstools
# Проверка доступности внешнего кластера ELK 
curl -XGET http://192.168.1.162:9200/_cluster/health?pretty -u 'admin:password'

# Проверка доступности сервиса который ссылается на внешний кластер ELK

kubectl -n logging get svc -o wide
# NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)     AGE   SELECTOR
# elasticsearch     ClusterIP   10.233.5.52     <none>        9200/TCP    19d   <none>

curl -XGET http://10.233.5.52:9200/_cluster/health?pretty -u 'admin:password'
curl -XGET http://elasticsearch.logging:9200/_cluster/health?pretty -u 'admin:password'
```

##### Установка через helm 
```
для решения      ./K8S/infra/ELK/to_ELK/to_ELK.md
```
```bash 

# файлы с параметрами  ./K8S/infra/ELK/k8s_fluentbit/helm

# image
image
# tolerations
# чтобы мог садиться на все ноды 
# Куда отправлять логи 
outputs: |
      [OUTPUT]
          Name        kafka
          Match       kube.*
          # Brokers     kafka.kafka.svc:9092
          Brokers     192.168.1.250:9092
          Topics      kube

[FILTER] [INPUT]
# Обратить вниманиен на теги по которым логи будут разноситься по разным топикам
Tag
   - kube.*
   - host.log.mail
[OUTPUT]
распределение по топикам идет за счет 
Match


# SETUP 
cd  ./K8S/infra/ELK/k8s_fluentbit/to_kafka

kubectl apply -f 01_flb-acc.yaml
kubectl apply -f 02flb-cm.yaml
kubectl apply -f 03_flb-services.yaml
kubectl apply -f 04_flb-ds.yaml 
kubectl apply -f 05_flb-ds-service.yaml
kubectl apply -f 06_flb-sm.yaml


# helm repo add fluent https://fluent.github.io/helm-charts
# helm repo update
# 
# Посмотреть values
https://github.com/fluent/helm-charts/blob/main/charts/fluent-bit/values.yaml

# обратить внимание на секцию outputs в ./K8S/infra/ELK/k8s_fluentbit/helm/values_to_kafka.yaml
# Brokers     kafka:9092
# должен быть сервис на внешнюю кафку   ./K8S/infra/ELK/k8s_fluentbit/to_kafka/03_flb-services.yaml

helm install fluentbit fluent/fluent-bit \
  --namespace logging \
  --create-namespace \
  --values ./values_to_kafka.yaml

helm uninstall fluentbit --namespace logging
```