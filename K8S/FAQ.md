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
###### 
###### 
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