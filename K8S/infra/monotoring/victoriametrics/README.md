#### Описание 
#### Установка 
```
развертывание с использованием deployment         ./K8S/infra/monotoring/victoriametrics/victoria-deployment.yaml 
для архитектуры на                                ./K8S/infra/monotoring/images/image1.jpg

```
#### Тестироваине 



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

развертывание с использованием deployment 
для архитектуры на                                ./K8S/infra/monotoring/images/image2.jpg
```
Установка производится в кластер k8s с учетом созданного NFS    ./study/K8S/infra/NFS/readme.md
deployment                                                      ./K8S/infra/monotoring/victoriametrics/victoria-deployment.yaml                                                  

deployment имеет два service (одни для statefullset, второй для обращения к базе данных)
statefullset необходим для того чтобы выдать pod определенное имя victoriametrics-sys-0 
к которому можно обратиться по selector (если подов будет много, обращение будет только на один)
retentionPeriod - за какой период хранить метрики   

kubectl apply -f victoria-deployment.yaml

```

###### Тестироваине 
```
```