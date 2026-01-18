```
- Пример
- архитектрура приложение 
- как перейти с localhost to microservices
- сборка образов docker
- развертывание приложения на кластере k8s (классический вариант)
- тестирование 

- развертываение с istio
- тестирование 
```
-----------------

##### Пример
```
По материалам 
https://www.freecodecamp.org/news/learn-kubernetes-in-under-3-hours-a-detailed-guide-to-orchestrating-containers-114ff420e882

https://github.com/rinormaloku/k8s-mastery

https://www.freecodecamp.org/news/learn-istio-manage-microservices/

Приложение реализует одну фукнциональность - оценивает чувствительность введенного текста 
```
##### архитектрура приложение 
```
Приложение состоит из 3 микросервисов

 - SA-Frontend:  Nginx web server that serves our ReactJS static files.
 - SA-WebApp:    Java Web Application that handles requests from the frontend.
 - SA-Logic:     python application that performs Sentiment Analysis.

см рис arch.png

1 - Клиентское приложение запрашивает index.html (которое, в свою очередь, запрашивает встроенные скрипты приложения ReactJS)  I like yogobella!
2 - Пользователь, взаимодействующий с приложением, запускает запросы в Spring WebApp.
3 - Spring WebApp перенаправляет запросы на анализ настроений в приложение Python.
4 - Приложение Python вычисляет настроение и возвращает результат в качестве ответа.
5 - Веб-приложение Spring возвращает ответ приложению React. (Которое затем представляет информацию пользователю).
```
##### как перейти с localhost to microservices
```
 Запуск 3-х сервисов на 1 хосте 
 см рис localhost.png
 - SA-Frontend  localhost:80
 - SA-WebApp    localhost:8080
 - SA-Logic     localhost:5000
```
``` 
SA-Frontend  localhost:80
```
```bash
# React application  need NodeJS and NPM installed on localhost
# все Javascript-зависимости приложения React и помещаются в папку node_modules. (Зависимости определены в файле package.json)
# переходим в папку ./k8s-mastery/sa-frontend/
npm install
npm start

# приложение по умолчанию доступно по localhost:3000

# подготовить статические файлы для web-server
# папке ./k8s-mastery/sa-frontend/
npm run build

# будет сгенерирована папка named build которая содержит все статические файлы для ReactJS application.
# устанавливаем nginx
# перемещаем статические файлы из ./sa-frontend/build folder to [nginx_installationdir]/html
# проверить приклад localhost:80
```

```     
SA-WebApp    localhost:8080
```
```bash
# переходим в папку ./k8s-mastery/sa-webapp/
mvn install
# будет создана папка target с файлом sentiment-analysis-web-0.0.1-SNAPSHOT.jar

# Starting our Java Application
cd ./target/
java -jar sentiment-analysis-web-0.0.1-SNAPSHOT.jar --sa.logic.api.url=http://localhost:5000
```

```
SA-Logic     localhost:5000
```
```bash

cd sa-logic/sa
python -m pip install -r requirements.txt
python -m textblob.download_corpora

# Starting the app
python sentiment_analysis.py

```
 
##### сборка образов docker

```
Общий подход

1 Install Docker CE
2 Register to the Docker Hub.
3 Login by executing the below command in your Terminal

docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"

docker build -f Dockerfile -t $DOCKER_USER_ID/<image_name> .
docker push $DOCKER_USER_ID/<image_name>

docker pull $DOCKER_USER_ID/<image_name>
docker run -d -p 80:80 $DOCKER_USER_ID/<image_name>
```

```
 SA-Frontend  localhost:80
```

```bash
# Start from the base Nginx Image
# Copy the sa-frontend/build directory to the containers nginx/html directory.

docker build -f Dockerfile -t $DOCKER_USER_ID/sentiment-analysis-frontend .
docker push $DOCKER_USER_ID/sentiment-analysis-frontend
docker pull $DOCKER_USER_ID/sentiment-analysis-frontend
docker run -d -p 80:80 $DOCKER_USER_ID/sentiment-analysis-frontend
```
```
 SA-WebApp    localhost:8080
```
```bash
docker build -f Dockerfile -t $DOCKER_USER_ID/sentiment-analysis-web-app .
docker run -d -p 8080:8080 -e SA_LOGIC_API_URL='http://<container_ip or docker machine ip>:5000' $DOCKER_USER_ID/sentiment-analysis-web-app  
```
```
 SA-Logic     localhost:5000
```

```bash
docker build -f Dockerfile -t $DOCKER_USER_ID/sentiment-analysis-logic .
docker run -d -p 5050:5000 $DOCKER_USER_ID/sentiment-analysis-logic
```


##### развертывание приложения на кластере k8s (классический вариант)
###### POD
```
# Creating the SA Frontend pod
kubectl create -f sa-frontend-pod.yaml
# pod "sa-frontend" created

kubectl get pods
# NAME                          READY     STATUS    RESTARTS   AGE
# sa-frontend                   1/1       Running   0          7s


# Accessing the application externally
kubectl port-forward --address 0.0.0.0 pod/sa-frontend 88:80
# Forwarding from 0.0.0.0:88 -> 80

http://192.168.1.171:88/
```
###### SERVICE
```
# проверям наличие label у pod (service  будет ориентироваться на label)
kubectl get pod -l app=sa-frontend
#NAME           READY   STATUS    RESTARTS   AGE
#sa-frontend    1/1     Running   0          31m
#sa-frontend2   1/1     Running   0          6m28s

---
apiVersion: v1
kind: Service              # 1 A service
metadata:
  name: sa-frontend-lb
spec:
  type: LoadBalancer       # 2 Specification type, we choose LoadBalancer because we want to balance the load between the pods. 
  # type: ClusterIP
  ports:
  - port: 80               # 3 Port: Specifies the port in which the service gets requests
    protocol: TCP          # 4 Protocol: Defines the communication
    targetPort: 80         # 5 TargetPort: The port at which incomming requests are forwarded
  selector:                # 6 Selector: Object that contains properties for selecting pods.
    app: sa-frontend       # 7 app: sa-frontend Defines which pods to target, only pods that are labeled with “app: sa-frontend"
---

kubectl create -f service-sa-frontend-lb.yaml

kubectl get svc
# sa-frontend-lb           ClusterIP   10.233.24.77    <none>        80/TCP             3m50s

kubectl port-forward --address 0.0.0.0 service/sa-frontend-lb 88:80

http://192.168.1.171:88/

```
###### Deployment 
```
---
apiVersion: apps/v1
kind: Deployment                                          # 1 
metadata:
  name: sa-frontend
spec:
  selector:                                               # 2
    matchLabels:
      app: sa-frontend                                    
  replicas: 2                                             # 3
  minReadySeconds: 15
  strategy:
    type: RollingUpdate                                   # 4
    rollingUpdate: 
      maxUnavailable: 1                                   # 5
      maxSurge: 1                                         # 6
  template:                                               # 7
    metadata:
      labels:
        app: sa-frontend                                  # 8
    spec:
      containers:
        - image: rinormaloku/sentiment-analysis-frontend
          imagePullPolicy: Always                         # 9
          name: sa-frontend
          ports:
            - containerPort: 80


---
# 1 Kind: A deployment.
# 2 Selector: Pods matching the selector will be taken under the management of this deployment.
# 3 Replicas is a property of the deployments Spec object that defines how many pods we want to run. So only 2.
# 4 Type specifies the strategy used in this deployment when moving from the current version to the next. The strategy RollingUpdate ensures Zero Downtime deployments.
# 5 MaxUnavailable is a property of the RollingUpdate object that specifies the maximum unavailable pods allowed (compared to the desired state) when doing a rolling update. For our deployment which has 2 replicas this means that after terminating one Pod, we would still have one pod running, this way keeping our application accessible.
# 6 MaxSurge is another property of the RollingUpdate object that defines the maximum amount of pods added to a deployment (compared to the desired state). For our deployment, this means that when moving to a new version we can add one pod, which adds up to 3 pods at the same time.
# 7 Template: specifies the pod template that the Deployment will use to create new pods. Most likely the resemblance with Pods struck you immediately.
# 8 **app:** sa-frontend the label to use for the pods created by this template.
# 9 ImagePullPolicy when set to Always, it will pull the container images on each redeployment.

kubectl apply -f sa-frontend-deployment.yaml

kubectl get pods
# NAME                                      READY   STATUS    RESTARTS       AGE
# sa-frontend                               1/1     Running   0              88m
# sa-frontend-846bf7c545-nzmwl              1/1     Running   0              9s
# sa-frontend-846bf7c545-w4wpq              1/1     Running   0              9s
# sa-frontend2                              1/1     Running   0              63m

# We got 4 running pods, two pods created by the Deployment and the other two are the ones we created manually. Delete the ones we created manually using the command 

kubectl delete pod <pod-name>.
```

###### Rolling a Zero-Downtime deployment
```
# Произвели изменение в коде новый image: rinormaloku/sentiment-analysis-frontend:green
# цель обновить его 
# Edit the file sa-frontend-deployment.yaml by changing the container image to refer to the new image: rinormaloku/sentiment-analysis-frontend:green

kubectl apply -f sa-frontend-deployment-green.yaml

# check the status of the rollout
kubectl rollout status deployment sa-frontend
# Waiting for deployment "sa-frontend" rollout to finish: 1 old replicas are pending termination...
# Waiting for deployment "sa-frontend" rollout to finish: 1 old replicas are pending termination...
# deployment "sa-frontend" successfully rolled out

### Rolling back to a previous state
kubectl rollout history deployment sa-frontend
# deployment.apps/sa-frontend
# REVISION  CHANGE-CAUSE
# 1         <none>
# 2         <none>

kubectl rollout undo deployment sa-frontend --to-revision=1
# deployment.apps/sa-frontend rolled back


#### Deployment SA-Logic
kubectl apply -f sa-logic-deployment.yaml

#### Service SA Logic
kubectl apply -f service-sa-logic.yaml

##### Deployment SA-WebApp

---
env:
    - name: SA_LOGIC_API_URL
      value: "http://sa-logic"
# environment variable SA_LOGIC_API_URL with the value “http://sa-logic” inside our pods
# kube-dns is that it creates a DNS record for each created service
# when we created the service sa-logic it got an IP address. 
# Its name was added as a record (in conjunction with the IP) in kube-dns. 
# This enables all the pods to translate the sa-logic to the SA-Logic services IP address.

##### Service SA-WebApp
kubectl apply -f service-sa-web-app-lb.yaml 
---

```


