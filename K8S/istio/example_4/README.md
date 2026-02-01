
#### ISTIO EXAMPLE

```
https://www.freecodecamp.org/news/learn-istio-manage-microservices/
https://github.com/rinormaloku/master-istio.git 

```
###### APP
```
SA-Frontend   — service serves the frontend; a React JavaScript application
SA-WebApp     — service handles queries for analyzing the sentiment of sentences
SA-Logic      — service performs sentiment analysis
SA-Feedback   — service records the user feedback about the accuracy of the analysis

# см pic_2.png

```

###### Run the Services on the Mesh

```bash
# Create a namespace and label it for automatic injection.
kubectl create ns demo 
kubectl label ns demo istio-injection=enabled
kubectl get namespace -L istio-injection
# demo                   Active   20s    enabled

# Switch the kubectl context to the demo namespace
kubectl config set-context --current --namespace=demo


git clone https://github.com/rinormaloku/master-istio.git 
cd master-istio

deploy the services
kubectl apply -f ./kube

kubectl get pods -n demo
# NAME                           READY     STATUS    RESTARTS   AGE
# sa-feedback-55f5dc4d9c-c9wfv   2/2       Running   0          12m
# sa-frontend-558f8986-hhkj9     2/2       Running   0          12m
# sa-logic-568498cb4d-2sjwj      2/2       Running   0          12m
# sa-logic-568498cb4d-p4f8c      2/2       Running   0          12m
# sa-web-app-599cf47c7c-s7cvd    2/2       Running   0          12m

kubectl get pods -n demo --show-labels=true

# Проверка что в контейнер приложения заехал istio как sidecar 
# Проверить в поде 
# kubectl describe pod <pod_name> -n <namespace_name>

kubectl describe pod sa-frontend-566756455d-wgqz2 -n demo

# istio-proxy:
#    Container ID:  containerd://96aa1443bd8ec02d2efcfa7b2aebe618e7cdcb928c0b3d809cd62e3b3faabca3
#    Image:         docker.io/istio/proxyv2:1.27.2
#    Image ID:      docker.io/istio/proxyv2@sha256:b00a23cb37e7b8e422b57e617c1bb7304955e368308b5c166e38f0444e0f5a08
#    Port:          15090/TCP
#    Host Port:     0/TCP
#    Args:
#      proxy
#      sidecar


kubectl get service -n demo
# NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)            AGE
# sa-feedback          ClusterIP   10.233.4.59     <none>        80/TCP             27h
# sa-frontend          ClusterIP   10.233.41.11    <none>        80/TCP             27h
# sa-logic             ClusterIP   10.233.38.131   <none>        80/TCP             27h
# sa-webapp            ClusterIP   10.233.19.29    <none>        80/TCP             27h


# Проверить доступность сервиса 
kubectl port-forward --address 0.0.0.0 service/sa-frontend 88:80
http://192.168.1.171:88/
#

```
###### Open the application to outside traffic

```bash
# configure the Istio ingress gateway
kubectl apply -f http-gateway.yaml -n demo

kubectl describe Gateway http-gateway

# Configure HTTP routing

#  By default, Istio creates a LoadBalancer service for a gateway. As we will access this gateway by a tunnel, we don’t need a load balancer.
# Change the service type to ClusterIP by annotating the gateway:

kubectl annotate gateway http-gateway networking.istio.io/service-type=ClusterIP --namespace=demo
# configures traffic routing within the mesh for all proxies and gateways.
# Paths matching exactly      /                     should be routed to SA-Frontend to get the Index.html
# Paths prefixed with         /static/*             should be routed to SA-Frontend to get any static files needed by the frontend, like Cascading Style Sheets and JavaScript files.
# Paths that match the regex  '^.*\.(ico|png|jpg)$' should be routed to SA-Frontend.

kubectl apply -f vs-route-ingress.yaml
kubectl describe HTTPRoute sa-external-services -n demo

kubectl port-forward --address 0.0.0.0 service/http-gateway-istio 8080:80
kubectl port-forward -n demo svc/http-gateway-istio --address 0.0.0.0 8080:80
http://localhost:8080/
 
```
##### Observability
```bash
# Prometheus  for collecting metrics
# Grafana     for visualizing those
# Jaeger      for snitching traces
# Kiali       brings all telemetry data together

kubectl get svc -n istio-system
# NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                                          AGE
# grafana            ClusterIP   10.233.39.70    <none>        3000/TCP                                         103d
# istiod             ClusterIP   10.233.60.184   <none>        15010/TCP,15012/TCP,443/TCP,15014/TCP            103d
# jaeger-collector   ClusterIP   10.233.30.185   <none>        14268/TCP,14250/TCP,9411/TCP,4317/TCP,4318/TCP   103d
# kiali              ClusterIP   10.233.3.216    <none>        20001/TCP,9090/TCP                               103d
# loki               ClusterIP   10.233.13.117   <none>        3100/TCP,9095/TCP                                103d
# loki-headless      ClusterIP   None            <none>        3100/TCP                                         103d
# loki-memberlist    ClusterIP   None            <none>        7946/TCP                                         103d
# prometheus         ClusterIP   10.233.38.209   <none>        9090/TCP                                         103d
# tracing            ClusterIP   10.233.30.211   <none>        80/TCP,16685/TCP                                 103d
# zipkin             ClusterIP   10.233.32.226   <none>        9411/TCP                                         103d


# grafana
#./istio-1.27.2/bin/istioctl dashboard grafana

istioctl dashboard grafana
kubectl port-forward --address 0.0.0.0 -n istio-system svc/grafana 3000:3000
http://192.168.1.171:3000

# istioctl dashboard jaeger
# http://localhost:16686

kubectl port-forward --address 0.0.0.0 -n istio-system svc/tracing 16686:80
#Forwarding from 0.0.0.0:16686 -> 16686
http://192.168.1.171:16686
```




###### generate traffic
```bash
while true; do \
  curl -i http://localhost:8080/sentiment \
  -H "Content-type: application/json" \
  -d '{"sentence": "I love yogobella"}'; \
  sleep .$RANDOM; done

```

##### LOG
```

[2026-02-01T16:29:24.710Z] "GET /static/js/main.f7659dbb.js HTTP/1.1"                      200             -                via_upstream            -                                 "-"                                    0                 279879       0         0                                      "10.233.66.16"             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36" "8fcedd10-23a4-9b4d-8caa-ade8a92a66a8" "192.168.1.171:8080"      "10.233.66.32:80"  inbound|80||        127.0.0.6:40305         10.233.66.32:80            10.233.66.16:0              outbound_.80_._.sa-frontend.demo.svc.cluster.local default
"[%START_TIME%]           \"%REQ(:METHOD)% %REQ(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%\" %RESPONSE_CODE% %RESPONSE_FLAGS% %RESPONSE_CODE_DETAILS% %CONNECTION_TERMINATION_DETAILS% \"%UPSTREAM_TRANSPORT_FAILURE_REASON%\" %BYTES_RECEIVED% %BYTES_SENT% %DURATION% %RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)% \"%REQ(X-FORWARDED-FOR)%\" \"%REQ(USER-AGENT)%\"                                                                                              \"%REQ(X-REQUEST-ID)%                  \" \"%REQ(:AUTHORITY)%\" \"%UPSTREAM_HOST%\" %UPSTREAM_CLUSTER% %UPSTREAM_LOCAL_ADDRESS% %DOWNSTREAM_LOCAL_ADDRESS% %DOWNSTREAM_REMOTE_ADDRESS% %REQUESTED_SERVER_NAME%                            %ROUTE_NAME%\n"

```





# Access the Kiali dashboard.

# This gateway is exposed by a Kubernetes Service of type LoadBalancer


istioctl dashboard kiali
kubectl port-forward --address 0.0.0.0 -n istio-system svc/kiali 20001:20001


http://192.168.1.171:20001/kiali 
```













