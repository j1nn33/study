##          Хранилища в кубере                             
######          - video                                    https://www.youtube.com/playlist?list=PLmxqUDFl0XM76Hnmsc2UDSvBT9Wf4W8Zl
######          - prepare_cluster
######          - emptyDir                                 https://www.kryukov.biz/kubernetes/lokalnye-volumes/emptydir/
######          - hostPath                                 https://www.kryukov.biz/kubernetes/lokalnye-volumes/hostpath/
######          - configMap                                https://www.kryukov.biz/kubernetes/lokalnye-volumes/configmap/
######          - secrets                                  https://www.kryukov.biz/kubernetes/lokalnye-volumes/secrets/
######          - downwardAPI                              https://www.kryukov.biz/kubernetes/lokalnye-volumes/downwardapi/
######          - projected                                https://www.kryukov.biz/kubernetes/lokalnye-volumes/projected/



####  Теория 
##### prepare_cluster
```
kubectl apply -f prepare-cluster-volume.yaml
kubectl get all -o wide -n volumes-sample 
kubectl get all -ALL -o wide | grep volumes

# Убрать за собой 

kubectl delete namespaces volumes-sample
```

##### emptyDir
```
- для размещения кеш файлов.
- для данных, которые необходимо сохранить при сбое в работе контейнера.
- для обмена файлами между несколькими контейнерами в под.
- Можно разместить в RAM (используется tmpfs)
        Medium – значение по умолчанию «». Если volume необходимо разместить в RAM, указывают значение Memory.
        sizeLimit – Общий объем локального хранилища, необходимый для тома emptyDir.
```
###### ---- Пример ./K8S/useful/test_case/04-test-volume-emptydir.yaml

##### hostPath 
```
- когда необходимо предоставить доступ к локальной файловой системе. Например, к логам приложений в /var/log.
        path – путь к файлу (директории) на сервере.
        type – тип подключения.
                : DirectoryOrCreate — Если по данному пути ничего не существует,то будет создан пустой каталог с разрешением 0755, имеющим ту же группу и владельца, что и Kubelet.
                : Directory — Каталог должен существовать по указанному пути.
                : FileOrCreate — Если по указанному пути ничего не существует, то будет создан пустой файл с разрешением 0644, имеющим ту же группу и владельца, что и Kubelet.
                : File — Файл должен существовать.
- необходимо учитывать, что в случае DirectoryOrCreate и FileOrCreate, должны существовать все директории, указанные в пути к конечному файлу.
```
###### ---- Пример ./K8S/tasks/kryukov/local_volumes/01_hostPath_afinity.yaml
```
# - приземлить pod на определенную ноду например worker3.kube.local
#             на ноде должен быть уже каталог 1000:3000  /var/directory 
ls -la /var | grep directory
drwxr-xr-x   2 1000 3000    6 Jul 15 02:49 directory

приземление пода на определенную ноду идет за счет affinity
# - поставить label на node.
kubectl label nodes worker3.kube.local directory=centos

kubectl apply -f 01_hostPath_afinity.yaml
kubectl -n volumes-sample get pod

# в pod
# bash-4.4$ touch /host_logs/23.txt
# bash-4.4$ ls -la /host_logs/
# -rw-r--r-- 1 root root  0 Jul 15 07:35 111.txt
# -rw-r--r-- 1 1000 3000  0 Jul 15 07:40 23.txt

# - Удалит метку с node
kubectl label nodes worker3.kube.local directory-

kubectl -n volumes-sample get all
kubectl -n volumes-sample delete deployment openresty
```  
###### ---- Пример ./K8S/tasks/kryukov/local_volumes/02_hostPath_log.yaml
```
DaemonSet (развертывается на каждой воркер ноде кластера) в pod в /host_logs - доступен на чтение каталог ноды /var/log

kubectl apply -f 02_hostPath_log.yaml

# в pod
# ls -la host_logs/

# Убрать за собой 
kubectl delete namespaces volumes-sample
```

##### configMap
```
- Создание конфигурационных файлов или любых других не пустых файлов.
- Определения большого количества переменных среды окружения контейнера.
- Текстовые данные должны быть в кодировке UTF-8. Если файл должен быть в другой кодировке, используйте binаryData.
- Необходимо сначала создать объект configMap, прежде чем его использовать. Иначе при инициализации пода будет выводиться сообщение об ошибке, а сам под не будет запущен.
       Name – указываем имя volume из раздела volumes.
       mountPath – точка монтирования. В конкретном примере в configMap описан один файл и монтирование происходит как файл, а не как директории.
       subPath — путь внутри тома, из которого должен быть смонтирован том контейнера. По умолчанию <> (корень тома) при изменении configMap не будет изменяться содержимое подмонтированного ресурса
```
###### ---- Пример ./K8S/tasks/kryukov/local_volumes/02_hostPath_log.yaml
```
# запускаем контейнер с openresty и заменяем в нем index.html на целевую ./K8S/tasks/kryukov/volumes/index.html
# создание configMap из файла  
kubectl create configmap index-html --from-file=./index.html --dry-run=client -o yaml | sed '/creationTimestamp/d' > out_file_configmap.yaml
kubectl apply -f prepare-cluster-volume.yaml

kubectl -n volumes-sample apply -f out_file_configmap.yaml
kubectl -n volumes-sample get configmap
# NAME               DATA   AGE
# index-html         1      27s

# Создание ENV для проброса в pod (изменяются только когда pod инициализируется)
kubectl -n volumes-sample apply -f 03_configmap_env.yaml

# Создаем под
kubectl apply -f 04_openresty_configmap_env.yaml

# Добавелено в описании pod
env | grep NGINX_HOST
NGINX_HOST=openresty-7bdcdbcc8d-6xrnl

# Добавелено в описании configmap
env | grep ENV       
ENV_SOME_VALUE=new
ENV_HOSTS=1

# Получить доступ 
kubectl -n volumes-sample apply -f 05_nodeport_nginx.yaml

kubectl -n volumes-sample get all -o wide
# NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE   SELECTOR
# service/openresty-srv                ClusterIP   10.233.63.159   <none>        80/TCP         70m   app=openresty
# service/service-nodeport-openresty   NodePort    10.233.12.87    <none>        80:30880/TCP   4s    app=openresty

http://192.168.1.171:30880/
# При наличии HA (когда разворачивался клатстер)
http://192.168.1.189:30880/

# Убрать за собой 
kubectl delete namespaces volumes-sample
```
##### secrets
```
- содержит небольшое количество конфиденциальных данных, таких как пароль, токен или ключ
  может быть использован:
     - Как файлы в томе, смонтированном на одном или нескольких его контейнерах.
     - В качестве переменной среды окружения контейнера.
```
###### ---- Пример
```
# Создание secret из файла
kubectl -n volumes-sample create secret generic my-secret --from-file=user=user.txt --from-file=password=password.txt

kubectl -n volumes-sample get secret
# NAME        TYPE     DATA   AGE
# my-secret   Opaque   2      100s

# Получить значения секрета 
kubectl -n volumes-sample get secret my-secret -o yaml

# apiVersion: v1
# data:
#   password: bXlwYXNzd29yZAo=
#   user: dXNlcl9hZG1pbg==

# Декодировать значение 
echo "bXlwYXNzd29yZAo=" | base64 --decode
# mypassword

# Подключение секретов в качестве переменных среды окружения 
#   - либо как переменные на начальном этапе (закоменчено)
#   - либо как envFrom  (позвлояет менять secret на лету)

kubectl -n volumes-sample apply -f 

# [root@openresty-749b54f844-7mxn7 /]# env | grep pass
# password=mypassword
# [root@openresty-749b54f844-7mxn7 /]# env | grep user
# user=user_admin

# Передача secret в виде файла
kubectl -n volumes-sample apply -f 07_secret.yaml

# Подклчюение secret в виде volume 
kubectl -n volumes-sample apply -f 

# [root@openresty-556b59b584-ldfw4 /]# ls  /etc/secrets/
# password  user
# cat /etc/secrets/user 
# user_admin
# cat /etc/secrets/password 
# mypassword

```
##### downwardAPI 
```
- Используется для того, чтобы сделать данные API доступными для приложений. Он монтируется как каталог и записывает запрошенные данные в текстовые файлы.
  (те пробрасывает характериски пода (CPU/MEM) во внутрь пода в виде файла, для использования ППО)
```
###### ---- Пример
```
kubectl -n volumes-sample apply -f 09_openresty_downwardAPI.yaml
# [root@openresty-5bc7479f7c-f8l66 /] ls /etc/pod-info/
# labels  limit-cpu-millicores  limit-memory-kibibytes
```
##### projected
```
- projected позволяет объединить несколько различных источников в одном volume. Все объединяемые ресурсы должны находится с подом в одном namespace.
     Поддерживается объединение:
         - secret
         - downwardAPI
         - configMap
         - serviceAccountToken   
```
###### ---- Пример
```
# в примере заворачиваем 3 сущности
#          projected:
#            sources:
#              - downwardAPI:
#              - secret:
#              - configMap:

# в pod будет смонтировано в файлову систему
# /etc/pod-data/-
#               - limits/cpu-millicore
#               - limits/memory-kibibytes
#               - labels
#               - secret/user
#               - secret/password
#               - configs/example.txt
#               - configs/config.yaml

kubectl -n volumes-sample apply -f 10_projected_secret.yaml
kubectl -n volumes-sample apply -f 11_projected_configMap.yaml
kubectl -n volumes-sample apply -f 12_openresty_projected.yaml

# [root@openresty-75cbf75847-qlxdl /]# ls /etc/pod-data/
# configs  labels  limits  secret
# ls /etc/pod-data/limits/
# cpu-millicore  memory-kibibytes
# cat /etc/pod-data/limits/cpu-millicore 
# 200
# ls /etc/pod-data/secret/                 
# password  user      
# cat /etc/pod-data/secret/user 
# adminuser
# ls /etc/pod-data/configs/
# config.yaml  example.txt  
#  cat /etc/pod-data/configs/example.txt 
# Пример configMap hello world.
# cat /etc/pod-data/configs/config.yaml 
# any_body:
#   params:
#     param1: value1
#     param2: value2
  
```

