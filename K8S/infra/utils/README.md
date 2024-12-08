##          Утилиты                            
######    - Namespaces         
######    - Metrics server        
######    - Priority class     
######    - Reloader           
######    - Cert-manager       

#### Namespaces
```
# Cоздание необходимых для дальнейшей работы namespaces
kubectl apply -f namespace.yaml
```
#### Metrics server
```
https://github.com/kubernetes-sigs/metrics-server
# Cобирает метрики по использованию CPU и RAM.
# Добавляет metrics API, используемый в HPA инструментах горизонтального масштабирования подов. 

# Readiness probe failed: HTTP probe failed with statuscode: 500
# скачиваем манифети и добавляем and add --kubelet-insecure-tls

---
containers:
- args:
- --cert-dir=/tmp
- --secure-port=4443
- --kubelet-insecure-tls
---

kubectl apply -f metrics_server.yaml

kubectl top node
kubectl -n volumes-sample top pods

kubectl -n <name_namespce> get pod
kubectl -n <name_namespce> top pod <pod_name>


```
#### Priority class  
```
# Приоритеты
kubectl apply -f priority-class.yaml
```
#### Reloader
```
# Документация            https://github.com/stakater/Reloader
# Образ на DockerHub.     https://hub.docker.com/r/stakater/reloader/tags?page=1&ordering=last_updated
 
# решает пробелму с configmap 
# утилита для перезагрузки сервиса после изменения comfigMap. 

# На что обратить внимание:
#  - Переменная среды окружения KUBERNETES_NAMESPACE. 
#    Если не определена, работает со всеми namespace кластера.
#  - Аргумент командной строки --namespaces-to-ignore - можно перечислить 
#    через запятую имена namespace, которые программа будет игнорировать.

# Наличие: 
# namespace: monitoring
# priorityClassName: low-priority

kubectl apply -f reloader.yaml

пример  ./K8S/infra/utils/test-app.yaml

# - указание reloder следить за ППО
#   annotations:
#     reloader.stakater.com/auto: "true"
#     configmap.reloader.stakater.com/reload: "index-html"
	
# Пример test-app.yaml
# - указание reloder следить за ППО
```
```yaml
  annotations:
    reloader.stakater.com/auto: "true"
    configmap.reloader.stakater.com/reload: "index-html"
```

#### Cert-manager
```
# cert-manager - утилита для управления сертификатами.
# документация -  https://cert-manager.io/docs/installation/kubernetes/

kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.2.0/cert-manager.yaml
kubectl get pods --namespace cert-manager
# Namespace cert-manager создаётся автоматически.

# Пример испольования
# во внешний мир выставляются ingress на которых терминируются ssl соединения
# все соединения внутри кластера идут без ssl
# cert-manager - следит за этими сертификатами на ingress

```

