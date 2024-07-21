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

```
#### Cert-manager
```

```

