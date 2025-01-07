#### Описание 
#### Установка 
```
для архитектуры на (v1)                             ./K8S/infra/monotoring/images/image2.jpg
для архитектуры на (v2)                             ./K8S/infra/monotoring/images/image3.jpg
для архитектуры на (v3)                             ./K8S/infra/monotoring/images/image1.jpg
```
###### Troubleshoot
###### -----------------------------------------------------------------------------------------

###### Описание 
```
База данных, используемая для длительного хранения метрик.

Victoriametrics Home       https://victoriametrics.com/
Victoriametrics GitHub     https://github.com/VictoriaMetrics/VictoriaMetrics
Victoriametrics DockerHub  https://hub.docker.com/r/victoriametrics/victoria-metrics

Retention Period/Disk Space 
Calculation Example       https://docs.victoriametrics.com/guides/understand-your-setup-size/?highlight=simple&highlight=size&highlight=calcula#retention-perioddisk-space

```
###### Установка 
```

```
###### для архитектуры на (v1)                               ./K8S/infra/monotoring/images/image2.jpg
```
развертывание с использованием deployment                       ./K8S/infra/monotoring/victoriametrics/v1_victoria-deployment.yaml 
Установка производится в кластер k8s с учетом созданного NFS    ./study/K8S/infra/NFS/readme.md
                                               
deployment имеет два service (одни для statefullset, второй для обращения к базе данных)
statefullset необходим для того чтобы выдать pod определенное имя victoriametrics-sys-0 
к которому можно обратиться по selector (если подов будет много, обращение будет только на один)
retentionPeriod - за какой период хранить метрики   

kubectl apply -f v1_victoria-deployment.yaml

```

###### для архитектуры на (v2)                              ./K8S/infra/monotoring/images/image3.jpg
```
Victoriametrics может самостоятельно собирать метрики с приложений, также можно использовать конфиг prometheus
(c некоторыми изменениями) и убрать prometheus из схемы 
в deployment ./K8S/infra/monotoring/victoriametrics/v2-victoriametrics.yaml
добавлются роли для доступа в k8s, дополнительные параметры конфигурирования
    - promscrape.config=/etc/prometheus.yml      - использование конфига prometheus
    - selfScrapeInterval=15s                     - интервал сбора метрик самой себя
    - http.pathPrefix=/vm                        - префикс к url
    - volumeMounts                               - для монтирования конфига prometheus

Измениния в конфигрурационом файле prometeus
./K8S/infra/monotoring/victoriametrics/v2_00-prometeus-config.yaml

Удалено     remote_write: - url: http://victoriametrics-sys-connect:8428/api/v1/write
Добавлено   replacement: "meta_${1}"

Для доступа используем ingress ./K8S/infra/monotoring/utils/v2-ingress.yml


kubectl apply -f v2_00-prometeus-config.yaml
kubectl apply -f v2-victoriametrics.yaml
kubectl apply -f v2-ingress.yaml


При такой схеме если обновлять конфиг prometeus-config.yaml, то необходимо перезапускать victoriametrics (при этом теряется часть метрик)
в качестве решения использовать vmagent
vmagent - позволяет собирать метрики (не только prometheus) и передавать их куда-либо
          без разницы как реализовывать (тк состояния не сохраняет) statefullset или deployment
          statefullset - как решение если несколько vmagent с разными конфигами (один мониторит одно, другой другое)  

Без изменнией            prometeus-config.yaml 
Изменено                 victoriametrics.yaml
   - удаляем  -  доступы 
   - удаляем  -  promscrape.config=/etc/prometheus.yml


Для доступа используем ingress ./K8S/infra/monotoring/utils/v2_2-ingress.yml

kubectl apply -f v2_00-prometeus-config.yaml
kubectl apply -f v2_2-victoriametrics.yaml
kubectl apply -f v2_2-ingress.yaml


Доступ 
https://192.168.1.171:30443/vmagent/targets

```

###### для архитектуры на (v3)                               ./K8S/infra/monotoring/images/image1.jpg

```
```

###### Troubleshoot
```
Если под лежит с ошибкой, то удаляем пустой каталого и перезапускаем под
# "ts":"2025-01-07T11:07:34.606Z","level":"panic","caller":"VictoriaMetrics/lib/fs/reader_at.go:92","msg":"FATAL: cannot open file \"/victoria-metrics-data/data/small/2025_01/70320_14708_20250105233745.530_20250105234100.530_1817DD23A04894FF/timestamps.bin\" for reading: open /victoria-metrics-data/data/small/2025_01/70320_14708_20250105233745.530_20250105234100.530_1817DD23A04894FF/timestamps.bin: no such file or directory"}



```

