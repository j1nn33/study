#### k8s

```bash
# Среда k3s

systemctl status k3s.service
● k3s.service - Lightweight Kubernetes
   Loaded: loaded (/etc/systemd/system/k3s.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2026-09-28 19:18:49 MSK; 7min ago

```

## Запустить несколько подов 
```bash
# Установка k8s dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

# посмотреть что все развернулось
kubectl -n kubernetes-dashboard get all

# посмотреть порт на котором работает dashboard
kubectl -n kubernetes-dashboard describe service kubernetes-dashboard
# TargetPort:        8443/TCP

# добавляем доступ к виртуалке (не хорошо, но быстро норм)
# внешний порт 30800 смотри 8443
kubectl apply -f ./test/dashboard/node-port-ks-dasboard.yaml 

https://192.168.1.171:30800/#/login

# Доступ к дашборду
kubectl apply -f ./test/dashboard/create_cred_ks-dasboard.yaml

# Создание и получение токена 
kubectl apply -f ./test/dashboard/token_for_dashboard.yaml
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d

# запускам http openresty 
kubectl apply -f ./test/app/app_1_http.yaml

kubectl describe pod openresty-78786fc7cd-98zt5

kubectl top pod openresty-78786fc7cd-98zt5
# NAME                         CPU(cores)   MEMORY(bytes)
# openresty-78786fc7cd-98zt5   1m           3Mi
# 1m (0.001 core)

# Проверить в консоле самого пода в k8s dasboard
curl http://localhost
# <html>
# <head>
#     <title>Тестовая страница</title>
#     <meta charset="UTF-8">
# </head>
# <body>
# <h1>Тестовая страница</h1>
# <p>Простая тестовая страница, версия 2</a>.
# </p>
# </body>
# </html>


# Убрать за собой 
kubectl get deployment -n default
# NAME        READY   UP-TO-DATE   AVAILABLE   AGE
# openresty   1/1     1 
kubectl delete deployment openresty -n default

# Контейнер с консолью для тестов 
kubectl run -it --rm --restart=Never --image=infoblox/dnstools:latest dnstools
# или 
kubectl run test --image=centosadmin/utils:0.3 -it bash
kubectl exec test -it bash

# Несколько контейнеров 
kubectl get pods -A
NAMESPACE              NAME                                        READY   STATUS      RESTARTS       AGE
default                openresty-78786fc7cd-98zt5                  1/1     Running     0              62m

kubernetes-dashboard   dashboard-metrics-scraper-8d46b45f6-z7r5f   1/1     Running     0              97m
kubernetes-dashboard   kubernetes-dashboard-b44857bbb-7xbps        1/1     Running     0              97m

```

#### Сборка совего контейнера 
```bash 
dnf install podman

mkdir test_container
cd test_container/

cat  dockerfile
```
```
# Используем UBI 7.7 в качестве базового образа
FROM registry.red-soft.ru/ubi7/ubi:latest

# Устанавливаем Apache HTTP Server (httpd)

RUN dnf install -y httpd && \
    dnf clean all && \
    rm -rf /var/cache/yum

# Заменяем содержимое домашней страницы по умолчанию
# Создаём новый файл index.html с нужным текстом
RUN echo "Hello from UBI 7.7 Apache Container!" > /var/www/html/index.html

# Открываем порт 80 для доступа к веб-серверу
EXPOSE 80

# Запускаем Apache в фоновом режиме (foreground), чтобы контейнер не завершался
ENTRYPOINT ["/usr/sbin/httpd"]
CMD ["-D", "FOREGROUND"]

```

```bash 
# Сборка образа
podman build -f dockerfile . --tag localhost:80/demo:v1

# Запуск контейнера с пробросом порта

podman run -d --name my-pache-container -p 8080:80 localhost:80/demo:v1

# Проверить статус контейнера
podman ps

# CONTAINER ID  IMAGE                 COMMAND        CREATED         STATUS         PORTS                 NAMES
# b17b6021c851  localhost:80/demo:v1  -D FOREGROUND  29 seconds ago  Up 29 seconds  0.0.0.0:8080->80/tcp  my-pache-container

# Проверить содержимое страницы
curl http://192.168.1.236/:8080

Hello from UBI 7.7 Apache Container!
```