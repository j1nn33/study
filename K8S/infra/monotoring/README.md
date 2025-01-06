#### Мониторинг
##### Архитектра 
##### Компоненты мониторинга
##### Установка 
##### Доступы 
### --------------------------------------------------------------------------------
```
```
###### Архитектра 
```
Реализация 
  по размещению компонетнов 
    - внешний мониторинг (компоненты реализованы на серверах не входящих в кластер k8s) 
    - внутренний мониторинг (компонеты реализованны в кластере k8s)

  по составу компонетов 
    - ./K8S/infra/monotoring/images/image1.jpg
    - ./K8S/infra/monotoring/images/image2.jpg
```
###### Компоненты мониторинга
```
Exporters          - разнообразные источники метрик в формате Prometheus. Метрики может отдавать непосредственно приложение, так и специально написанные для приложений экспортёры.
Victoriametrics    - Хранилище метрик. Вариант victoriametrics single - один экземпляр приложения. Предназначен для небольших объемов и сроков хранения данных.
Vmagent            - приложение, собирающее метрики из экспортёров и помещающее их в хранилище метрик. Имеет возможность работать не только с экспортёрами метрик Prometheus, но и с другими  системами (Graphite, InfluxDB agent и т.д.). Может быть запущено несколько vmagent.
Prometheus         - Сбор метрик
Vmalert            - Формирует алёрты на основании метрик, хранящихся в базе victoriametrics. Сгенерированные алёрты отправляет в alertmanager для дальнейшей обработки.
Alertmanager       - обрабатывает алёрты, отправляемые клиентскими приложениями. Он заботится о дедупликации, группировке и маршрутизации алёртов к получателям. Также может выключать и запрещать алёрты.
Karma              - Приложение, формирующее дашборды на основании информации из alertmanager. Отображает текущие (не закрытые) алёрты. Позволяет гибко фильтровать информацию, основываясь на метках.
Grafana            - Приложение для создания дашбордов на основании различных источников данных. В том числе находящихся в
kube-state-metrics - это простой сервис, который обращается к Kubernetes API и генерирует метрики о состоянии объектов.
```
###### Установка 
```
Реализация архитектуры на           ./K8S/infra/monotoring/images/image1.jpg
    - victoriametrics               ./K8S/infra/monotoring/victoriametrics/README.md   
    - exporter                      ./K8S/infra/monotoring/exporter/README.md
    - prometheus                    ./K8S/infra/monotoring/prometheus/README.md    
        - мониторинг самого prometeus   
        - Метрики API сервера                  
        - Метрики Kubelet                     
        - Метрики Kubelet cadvisor            
        - Метрики nodelocaldns                
        - Метрики kube-controller             
        - Метрики kube-scheduller             
        - Метрики node-exporter               
        - Метрики kube-state-metrics          
        - Метрики ingress-nginx-endpoints   
        - сбор метрик с etcd  
    - grafana                       ./K8S/infra/monotoring/grafana/README.md

```
###### Доступы 
```
Реализованы на осное ingress          ./K8S/infra/monotoring/utils/readme.md
https://192.168.1.171:30443/prometheus/
https://192.168.1.171:30443/grafana/login

```












==================================================================
==================================================================
==================================================================

Принцип установки приложений
Структура git
Exporters. Чарты «обёртки».
Victoriametrics
Vmagent
Grafana
Alertmanager
Vmalert
Karma

Kubernetes monitoring [04]. Правила сбора метрик.

values файлы.
job kubernetes-apiserver
job kubernetes-nodes
job kubernetes-nodes-cadvisor
сбор по аннотациям
job node-exporter
job kube-state-metrics

Kubernetes monitoring [07]. Vmalert


— Для чего используется vmalert?
— Файлы деплоймента.
— Список алёртов.
— Файлы правил.
— Подключение файлов правил.
— Запускаем vmalert.