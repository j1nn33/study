
## Podan                                    

######    - docker cli https://docs.docker.com/reference/cli/docker/container/rm/
######    - Install podman       
######    - Подключение к репозиторию        
######    - Создание локального репозитория    
######    - Подготовительные работы 
######    - Создание базоваго docker образа
######    - Создание образа на основе базового образа
######    - Базовые команды        
######    -     
######    -    
######    -         
######    -      

#### Install podman
```
dnf install podman
```
#### Подключение к репозиторию  
```
podman login https://<______>
```
#### Создание локального репозитория
```
mkdir -p /registry

vim /etc/containers/registries.conf
---
[registries.search]
registries = ['registry.access.redhat.com','registry.fedoraproject.org','registry.centos.org','docker.io']

[registries.insecure]
registries = ['localhost:5000']

[registries.block]
registries = []
---
# -d запускать в режиме демона 
podman run -d --name registry -p 5000:5000 -v /registry:/registry --restart=always registry:2

podman images
# REPOSITORY                  TAG         IMAGE ID      CREATED        SIZE
# docker.io/library/registry  2           cfb4d9904335  10 months ago  26 MB
podman ps

# CONTAINER ID  IMAGE                         COMMAND               CREATED        STATUS        PORTS                   NAMES
# f32d214ff0ba  docker.io/library/registry:2  /etc/docker/regis...  2 minutes ago  Up 2 minutes  0.0.0.0:5000->5000/tcp  registry

```
#### Подготовительные работы
```
mkdir ./docker
cd docker/

# почистить перед работой (удалить все image которые были созданы до этого)
podman rmi $(podman images -q) -f

```
#### Создание базоваго docker образа 
```
# Создаем базовый образ на основе которого будем настраивать все остальное  

cat << EOF > Dockerfile_base
FROM almalinux:8.10
RUN dnf -y update && dnf -y clean all
EOF

podman build -f Dockerfile_base . --tag localhost:5000/baseimage:v1.0
podman image push localhost:5000/baseimage:v1.0

podman images
# REPOSITORY                   TAG           IMAGE ID      CREATED         SIZE
# localhost:5000/baseimage     v1.0          0dad56464b8f  12 minutes ago  226 MB
# docker.io/library/almalinux  8.10-minimal  3bcff67817a8  2 weeks ago     95.8 MB
# docker.io/library/almalinux  8.10          70c960dbfdec  2 weeks ago     195 MB
# docker.io/library/registry   2          

```
#### Создание образа на основе базового образа 
```
cat << EOF > /tmp/README.txt
HELLO FROM DOCKER
EOF

chmod 777 /tmp/README.txt

cat << EOF > Dockerfile
FROM localhost:5000/baseimage:v1.0
ARG VERSION
WORKDIR /opt/app
RUN ls -la /
RUN cp /src/README.txt /opt/app/README.txt
RUN echo -e "version == ${VERSION}\n" >> /opt/app/README.txt
CMD cat README.txt

EOF

# Собираем контейнер 
# проброс переменных --build-arg VERSION="1.1demo"
# подключение каталогово -v=[HOST-DIR:CONTAINER-DIR[:OPTIONS]]
podman build -f Dockerfile . --build-arg VERSION="1.1demo" --tag localhost:5000/demo:v1.1 -v /tmp:/src

# Выгрузка образа в registry
podman image push localhost:5000/demo:v1.1

# запустить образ

podman run localhost:5000/demo:v1.1
# HELLO FROM DOCKER
# version == 1.1demo

```
#### Базовые команды  
```
# получить хеш образа
podman inspect localhost:5000/demo:v1.1 | jq .[].Digest

# получить образ и запустить его
podman pull localhost:5000/<name>:v1.1
podman run localhost:5000/<name>:v1.1

# посмотреть списко образов и контейнеров 
podman images
podman ps
```
#### Сборка multistage
```
# Сборака проекта производится на одном образе 
# Результат сборки помещается в другой образ (при этом промежуточные файлы и пакеты сборшики в финальный образ не попадают)

cat << EOF > Dockerfile_multistage
FROM docker.io/library/almalinux:8.10 AS builder
ARG VERSION
WORKDIR /opt/app
RUN echo "======= RUN BUILD PROJECT =========="
RUN cp /src/README.txt /opt/app/README.txt
RUN echo -e "version == ${VERSION}\n" >> /opt/app/README.txt
RUN echo "======= FINISH BUILD PROJECT =========="

FROM localhost:5000/baseimage:v1.0
WORKDIR /opt/finalapp
COPY --from=builder /opt/app/README.txt /opt/finalapp/README.txt
CMD cat README.txt
EOF

podman build -f Dockerfile_multistage . \
--build-arg VERSION="1.1demo_multistage" \
--tag localhost:5000/demo_multistage:v1.1 \
-v /tmp:/src

# Выгрузка образа в registry
podman image push localhost:5000/demo_multistage:v1.1

# запустить образ

podman run localhost:5000/demo_multistage:v1.1
# HELLO FROM DOCKER
# version == 

# узнать под каким пользователем запускается приложение в контейнере
podman run <image> id


```
