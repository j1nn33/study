# FAQ

###### Посмотреть секрет 
###### Закодироветь в base64
###### Создание secret из файла
###### Создание secret указывая данные в командной строке
###### Secret для доступа к хранилищу docker images 
###### Навесить лейбу на ноду  
###### Заставивить под заехать на определнную ноду 
###### Удалить taint с пода
###### Создание configMap из файла
###### Создание configMap, включая в него все файлы в текущей директории
###### Как через переменные закинуть несколько команд 
###### В манифесте для label если надо указать числа в виде строки то берем его "2"
###### проброс портов 
###### NET fast
###### 

### Ответы 

###### Посмотреть секрет 
```
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d
```
###### Закодироветь в base64
```
echo adminuser | base64
YWRtaW51c2VyCg==
```
###### Создание secret из файла
```
kubectl -n volumes-sample create secret generic my-secret --from-file=user=user.txt --from-file=password=password.txt
```
###### Создание secret указывая данные в командной строке
```
kubectl -n volumes-sample create secret generic my-secret --from-literal=user=user_admin --from-literal=password=mypassword
```
###### Secret для доступа к хранилищу docker images 
```
    imagePullSecrets:
      - name: registrykey
```
###### Навесить лейбу на ноду  
```
# - поставить на node worker3.kube.local label <directory=centos>
kubectl label nodes worker3.kube.local directory=centos

# - Удалит метку с node
kubectl label nodes worker3.kube.local directory-
```
###### Заставивить под заехать на определнную ноду 
```
# пример описан для ноды на которую навесили label <directory=centos> см. выше
# ./K8S/tasks/kryukov/volumes/01_hostPath_afinity.yaml
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:  # проверяется при создании, но игнорируется при работе 
            nodeSelectorTerms:
            - matchExpressions:
              - key: directory                             # нода помечена label directory
                operator: In
                values:
                - centos                                   # значение label directory равно centos
```
###### Удалить taint с пода
```
kubectl describe pod <name_pod> -n kube-system
kubectl taint nodes control1.kube.local node-role.kubernetes.io/master-
kubectl taint nodes control1.kube.local node-role.kubernetes.io/master:NoSchedule
```
###### Создание configMap из файла index.html
```
# Сразу создает configmap в кластере 
kubectl create configmap index-html --from-file=./index.html

# Позволяет создать описание манифеста для создания configmap
kubectl create configmap index-html --from-file=./index.html --dry-run=client -o yaml | sed '/creationTimestamp/d' > out_file_configmap.yaml

# sed '/creationTimestamp/d'    - удаялем строеки creationTimestamp чтобы не было проблем с обновлением
# --dry-run=client -o yaml      - создать описание манифеста, те не создает configmap в кластере 
```
###### Создание configMap, включая в него все файлы в текущей директории
```
kubectl create configmap index-html --from-file=./ --dry-run=client -o yaml | sed '/creationTimestamp/d' > out_dir_configmap.yaml
```
###### Как через переменные закинуть несколько команд 
```
crictl ps
crictl inspect <CONTAINER_ID>
PID=$(crictl inspect<CONTAINER_ID> | jq '.info.pid')
ps -ef | grep $PID | grep -v grep
```
###### В манифесте для label если надо указать числа в виде строки то берем его "2"
```
var_1: 2    - число
var_2: "2"  - строка

selector - за какими объектами следим
```

###### проброс портов 
```bash 
kubectl -n argocd get service

# NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
# argocd-dex-server       ClusterIP   10.233.1.44     <none>        5556/TCP,5557/TCP,5558/TCP   4h34m
# argocd-metrics          ClusterIP   10.233.24.13    <none>        8082/TCP                     4h34m
# argocd-redis            ClusterIP   10.233.36.175   <none>        6379/TCP                     4h34m
# argocd-repo-server      ClusterIP   10.233.62.110   <none>        8081/TCP,8084/TCP            4h34m
# argocd-server           ClusterIP   10.233.7.62     <none>        80/TCP,443/TCP               4h34m
# argocd-server-metrics   ClusterIP   10.233.39.95    <none>        8083/TCP                     4h34m

# открываем порт 
# kubectl port-forward [resource-type]/[resource-name] [local-port]:[resource-port]
# resource-type — тип ресурса (например, pod, svc, deployment)

kubectl port-forward -n argocd service/argocd-server --address 0.0.0.0 8888:443

http://192.168.1.171:8888

https://192.168.1.171:8888

```
###### открываем порт 
```bash 
kubectl proxy --address 0.0.0.0 --port=9090

# обращение к любому севрису 
http://localhost:9090/api/v1/proxy/namespaces/services/<SERVICE-NAME>:<PORT-NAME>/

http://192.168.1.171:9090/api/v1/proxy/argocd/services/argocd-server:80
https://192.168.1.171:9090/api/v1/proxy/argocd/services/argocd-server:443/
```
###### NET - FAST
```bash
###### Сервис NodePort.
# работает сам по себе, ничего дополнительного не надо 
nodeport.yaml
```
```yaml
---
apiVersion: v1
kind: Service
metadata:
  # имя сервиса
  name: nginx-nodeport   
  namespace: default
spec:
  type: NodePort
  ports:
      # 80 port если обратиться внутри кластера
    - port: 80
      name: http
      protocol: TCP
	  # порт куда пересылаются запросы в приложение k8s-app: nginx 
	  # имя порта http или номер порта 80 (зависит от конфига приложения )
      targetPort: http
	  # какой порт выставлять наружу 
      nodePort: 31080
  selector:
    # метка приложения куда пересылается трафик
    k8s-app: nginx          #
```
```
http://<IP>:31080

# кусок конфига приложения 
k8s-app: nginx
```
```yaml
 containers:
        - name: nginx
          image: nginx:1.23.1
          imagePullPolicy: IfNotPresent
          # имя порта и номер на которое слушает приклад
		  ports:
            - containerPort: 80
              name: http
```
```
###### Сервис LoadBalancer.
# сам по себе не работает - нужны доп сущности типа metallb
http://<IP>:8080
```
```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-loadbalancer
  namespace: default
spec:
  type: LoadBalancer
  ports:
      # порт доступа к приложению как внутри так и снаружи 
    - port: 8080
      name: http
      protocol: TCP
      targetPort: http
  selector:
    k8s-app: nginx
```


