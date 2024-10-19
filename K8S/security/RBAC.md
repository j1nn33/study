## RBAC 

### Теория
### Создание пользователя (пример)
###### создание сертификата/подписание сертификата
###### настройка конфига пользователя 
###### предоставление доступа пользователю 
###### - дать возможность просматривать ресуры 
###### - процесс добрасывания грантов пользователю
###### - разрешаем то что нужно, все остальное зарещено
###### предоставление доступа приложению 
### Теория
```
Доступ в k8s кластер - по сути доступ к kubernetis API

k8s
Аутентификация:
    - по сертификатам
    - по токенам
  
Авторизация 
    смотрим /etc/kubernetis/manifest/kube-apiserver.yaml
            --authorization-mode = Node, RBAC
            - по RoleBinding  

    USER (DN - сертификата)
В кластере нет такой возмоности добавить пользователя
Если у пользователя есть сертификат(который валиден с точки зрения k8s кластера), 
то пользователь прошел аутетнификацию
проблемы - сертификат нельзя отозвать, WA - удалить RoleBinding для этого сертификата

    POD
Доступ пода к kubernetis API (нужен pod не всегда)
пример ingress conntroller делает запросы к kubernetis API - следит какие ingress появляются в системе
- по токенам (генерятся в системе автоматически)
в pod директория монтруется автоматом k8s c токеном  /var/run/secrets/kubernetis.io/serviceaccount/token
 
    ServiceAccount         -  можно завести и Pod работает с правами ServiceAccount
    ServiceAccount default - с правами default - если pod не указать ServiceAccount
 
RBAC

- ROLE
  - привязана к конкретному namespace
    (описано к каким объектам API - какие деайствия могут применяться)
- CLUSTERROLE
  - привязана на весь кластер
```  
  
  
### Создание пользователя (пример)
```
пользователь tux должен иметь доступ в namespace app1
за пределами этого namespace прав быть не должно
```
###### создание сертификата/подписание сертификата
```
# созадем сертификат вида 
# cn=tux,dc=kube,dc=local

mkdir users
cd users/

# генерируем ключ
openssl genrsa -out tux.key 4096

# создаем конфигурационный файл opessl 
vim csr.cnf
```

```
[ req ]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn

[ dn ]
CN = tux
DC = kube
DC = local

[ v3_ext ]
authorityKeyIdentifier=keyid,issuer:always
basicConstraints=CA:FALSE
keyUsage=keyEncipherment,dataEncipherment
extendedKeyUsage=serverAuth,clientAuth
```

```
# Генерируем запрос на сертификат.
openssl req -config csr.cnf -new -key tux.key -nodes -out tux.csr

# Поместим содержимое файла csr в формате base64 в переменную среды окружения BASE64_CSR:
# cat tux.csr | base64 | tr -d '\n' - выглядит наш серт в base64
export BASE64_CSR=$(cat tux.csr | base64 | tr -d '\n')

# cоздаём файл csr.yaml c запросом на подпись (зависит от версии кластера валидно для версии v1.29.6)
vim csr.yaml
```
```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: tux_csr
spec:
  request: ${BASE64_CSR}
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
```
```
# Применяем запрос
# envsubst подставляет в проходящие по конвееру в нее данные переменные окружающей среды 
# те на лету загонит в request то что лечит в ${BASE64_CSR}
cat csr.yaml | envsubst | kubectl apply -f -

# Проверяем наличие запроса:
kubectl get csr

# NAME      AGE   SIGNERNAME                            REQUESTOR          REQUESTEDDURATION   CONDITION
# tux_csr   92s   kubernetes.io/kube-apiserver-client   kubernetes-admin   <none>              Pending

# Подписываем и генерируем сертификат:
kubectl certificate approve tux_csr

kubectl get csr
# NAME      AGE     SIGNERNAME                            REQUESTOR          REQUESTEDDURATION   CONDITION
# tux_csr   5m34s   kubernetes.io/kube-apiserver-client   kubernetes-admin   <none>              Approved,Issued

# Поместим сертификат пользователя в файл.
kubectl get csr tux_csr -o jsonpath={.status.certificate} | base64 --decode > tux.crt
# Посмотреть сертификат
openssl x509 -in tux.crt --text | less
```

###### настройка конфига пользователя 
```
# Настройка доступа пользователю
# Создание файла config
# Получаем информацию о подключении к кластеру.

kubectl cluster-info

# Нас интересует строка
# Kubernetes control plane is running at https://192.168.1.171:6443

# можно для информации посмотреть свой конфиг (его можно редачить по своему усмотреию)
cat .kube/config 

# Начинаем создавать файл конфигурации.
# Сначала добавим информацию о кластере.
# делаем относительно директории /root/user иначе убьем свой конфиг  
kubectl config --kubeconfig=./config set-cluster cluster.local --server=https://192.168.1.171:6443 \
--certificate-authority=/etc/kubernetes/pki/ca.crt /root/user

# Добавляем пользователя. (tux - имя для удобства, реальное определнено в DN)
kubectl config --kubeconfig=./config set-credentials tux --client-key=tux.key --client-certificate=tux.crt --embed-certs=true

# --embed-certs=true  - включает серты в конфиг иначе будут указаны пути к конфигам

# Определяем контекст. (--namespace app1 - опционально)
kubectl config --kubeconfig=./config set-context default --cluster=cluster.local --user=tux --namespace app1

# Устанавливаем контекст по умолчанию.
kubectl config --kubeconfig=./config use-context default

# Проверяем доступ к серверу
kubectl --kubeconfig=./config -n app1 get pods

#Error from server (Forbidden): pods is forbidden: User "tux" cannot list resource "pods" in API group "" in the namespace "app1"

# Мы должны получить сообщение об ошибке доступа пользователя tux к ресурсу. Это нормально. 
# На данном этапе мы сконфигурировали доступ к кластеру для пользователя – конфигурационный файл для программы kubectl.
# Доступ к элементам API кластера мы будем описывать отдельно.
# Скопируйте полученный config файл в домашнюю директорию пользователя tux:

mkdir /home/tux/.kube
cp config /home/tux/.kube
chown -R tux:tux /home/tux/.kube

# Проверка
sudo su - tux
pwd
# /home/tux
kubectl -n app1 get pods,services
# Error from server (Forbidden): pods is forbidden: User "tux" cannot list resource "pods" in API group "" in the namespace "app1"
# Error from server (Forbidden): services is forbidden: User "tux" cannot list resource "services" in API group "" in the namespace "app1"
```

 предоставление доступа

```
# Начальные условия 
# /home/tux
kubectl -n app1 get pods,services
# Error from server (Forbidden): pods is forbidden: User "tux" cannot list resource "pods" in API group "" in the namespace "app1"
# Error from server (Forbidden): services is forbidden: User "tux" cannot list resource "services" in API group "" in the namespace "app1" 


# пользователь tux должен иметь доступ в namespace app1
# за пределами этого namespace прав быть не должно
```
###### предоставление доступа приложению 
###### - дать возможность просматривать ресуры 

```
# Описание смотри в манифетсе 


kubectl apply -f 01_user.yaml

kubectl -n app1 get role
# NAME         CREATED AT
# tux-role-1   2024-10-08T05:57:37Z

kubectl -n app1 get rolebinding
# NAME     ROLE              AGE
# tux-rb   Role/tux-role-1   117s

kubectl -n app1 get pods,svc
# NAME                                        READY   STATUS    RESTARTS      AGE
# pod/app1-pod1-deployment-546cc875b9-k5zvt   1/1     Running   1 (12h ago)   39h
# NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
# service/service-app1-pod1   ClusterIP   10.233.11.150   <none>        81/TCP    39h


kubectl delete -f 01_user.yaml
```

###### - процесс добрасывания грантов пользователю
```
# - ошибка у пользователя 
# /home/tux
kubectl -n app1 get pods
# Error from server (Forbidden): pods is forbidden: User "tux" cannot list resource "pods" in API group "" in the namespace "app1"
# ------------------------------------------------------------ verbs ------resources---------apiGroups-------                                                         
# - apiGroups: [""]
#   resources: ["pods"]
#   verbs: [ "list"]

kubectl apply -f 02_user.yaml

# /home/tux
kubectl -n app1 get pods
# NAME                                    READY   STATUS    RESTARTS      AGE
# app1-pod1-deployment-546cc875b9-k5zvt   1/1     Running   1 (12h ago)   39h

# /home/tux
kubectl -n app1 get deployment
# Error from server (Forbidden): deployments.apps is forbidden: User "tux" cannot list resource "deployments" in API group "apps" in the namespace "app1"

kubectl apply -f 03_user.yaml
```

###### - разрешаем то что нужно, все остальное зарещено
```
rules:
- apiGroups: [""]
  resources: ["pods", "services", "replicationcontrollers"]
  verbs: ["create", "get", "update", "list", "delete"]
- apiGroups: [""]
  resources: ["pods/log"]                                                
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods/exec"]
  verbs: ["create"]
- apiGroups: ["apps"]
  resources: ["deployments","daemonsets","replicasets","statefulsets"]
  verbs: ["create", "get", "update", "patch", "list", "delete", "deploy"]
- apiGroups: ["autoscaling"]
  resources: ["horizontalpodautoscalers"]
  verbs: ["create", "get", "update", "list", "delete"]
- apiGroups: ["batch"]
  resources: ["jobs","cronjobs"]
  verbs: ["create", "get", "update", "list", "delete"]

# get  - получить конкретный ресурс по имени   kubectl -n app1 get pods app1-pod1-deployment-546cc875b9-k5zvt
# list - список без миени                      kubectl -n app1 get pods
# resources: ["pods/log"]                      kubectl -n app1 logs app1-pod1-deployment-546cc875b9-k5zvt
# resources: ["pods/exec"]                     kubectl -n app1 exec app1-pod1-deployment-546cc875b9-k5zvt -it -- bash
```

###### предоставление доступа приложению 
```
# предоставление доступа идет на осове токенов 
# ServiveAccount используют для доступа к API Kubernetes из приложений.
# Когда в системе создаётся pod, ему по умолчанию присваивается default ServiceAccount текущего namespace.
# Посмотреть ServiceAccount в namespace можно следующим образом:

# kubectl -n app1 get serviceaccounts
# Создавать ServiceAccount можно прямо в командной строке:

# kubectl -n app1 create serviceaccount testaccount
# или с помощью манифеста 
```
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: testaccount
  namespace: app1
``` 
``` 
kubectl apply -f file.yaml

# Если приложение (pod) запускается без явного указания ServiceAccount, ему присваивается ServiceAccount default.
# Для определения ServiceAccount, при описании пода используйте serviceAccountName.
# При запуске приложения ему автоматически подключается директория /var/run/secrets/kubernetes.io/serviceaccount в которой находятся файлы:
#       - ca.crt – сертификат CA кластера.
#       - Namespace – содержит имя namespace, в котором находится pod.
#       - token – содержит токен, используемый для доступа к API кластера.
# Если вы хотите получать доступ к API кластера не из приложения, а, например из командной строки при помощи curl. 
# Необходимо получить токен соответствующего ServiceAccount:

[root@app1-pod1-deployment-546cc875b9-k5zvt /]# ls  /var/run/secrets/kubernetes.io/serviceaccount/
ca.crt  namespace  token
[root@app1-pod1-deployment-546cc875b9-k5zvt /]# cat  /var/run/secrets/kubernetes.io/serviceaccount/namespace ; echo
app1


kubectl -n kubetest get secret $(kubectl -n app1 get serviceaccount kubetest-account \
-o jsonpath="{.secrets[0].name}") -o jsonpath="{.data.token}" | base64 –decode 

# Пример для приложения которое получает для своей работы список pods в определенном namespace
# те в процессе работы обращается к api kubernetis
# реализация serviceaccount

в deployment.yml приложения определяем 
```
```yml
apiVersion: apps/v1
kind: Deployment

spec:
    spec:
      serviceAccountName: kubetest-account
```
```
# определям ServiceAccount Role RoleBinding
# ./K8S/security/RBAC/01-acc.yaml

# перед deployment приложения необходимо создать ServiceAccount
kubectl apply -f 01-acc.yaml

kubectl -n app1 get serviceaccount

```
