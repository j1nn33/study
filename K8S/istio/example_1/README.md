#### Example 1

```
Разбор книги Istio: приступаем к работе

```
###### пример работы без прокси 
./K8S/istio/image/istio_example_1_1.png

###### пример работы istio
./K8S/istio/image/istio_example_1_2.png

######  установка istio
https://istio.io/latest/docs/setup/getting-started/

```
# latest
curl -L https://istio.io/downloadIstio | sh -

# other version  
curl -L https://git.io/getLatestIstio | ISTIO_VERSION=1.1.0 sh -

cd istio-1.27.2

export PATH=$PWD/bin:$PATH

istioctl version

# или полный путь 
./istio-1.27.2/bin/istioctl version

```
```
На примере https://istio.io/docs/examples/bookinfo/

https://istio.io/latest/docs/setup/getting-started/

# Install Istio using the demo profile, without any gateways:
istioctl install -f samples/bookinfo/demo-profile-no-gateways.yaml -y

✔ Istio core installed ⛵️
✔ Istiod installed 🧠
✔ Installation complete

istioctl version
client version: 1.27.2
control plane version: 1.27.2
data plane version: none

# Add a namespace label to instruct Istio to automatically inject Envoy sidecar proxies when you deploy your application later:
kubectl label namespace default istio-injection=enabled

namespace/default labeled

# Install the Kubernetes Gateway API CRDs зарегистрируем определения CustomResourceDefinitions объектов Istio в кластере Kubernetes:

kubectl get crd gateways.gateway.networking.k8s.io &> /dev/null || \
{ kubectl kustomize "github.com/kubernetes-sigs/gateway-api/config/crd?ref=v1.3.0" | kubectl apply -f -; }

kubectl api-resources | grep istio
# wasmplugins                                                                       extensions.istio.io/v1alpha1        true         WasmPlugin
# destinationrules                  dr                                              networking.istio.io/v1              true         DestinationRule
# envoyfilters                                                                      networking.istio.io/v1alpha3        true         EnvoyFilter
# gateways                          gw                                              networking.istio.io/v1              true         Gateway
# proxyconfigs                                                                      networking.istio.io/v1beta1         true         ProxyConfig
# serviceentries                    se                                              networking.istio.io/v1              true         ServiceEntry
# sidecars                                                                          networking.istio.io/v1              true         Sidecar
# virtualservices                   vs                                              networking.istio.io/v1              true         VirtualService
# workloadentries                   we                                              networking.istio.io/v1              true         WorkloadEntry
# workloadgroups                    wg                                              networking.istio.io/v1              true         WorkloadGroup
# authorizationpolicies             ap                                              security.istio.io/v1                true         AuthorizationPolicy
# peerauthentications               pa                                              security.istio.io/v1                true         PeerAuthentication
# requestauthentications            ra                                              security.istio.io/v1                true         RequestAuthentication
# telemetries                       telemetry                                       telemetry.istio.io/v1               true         Telemetry


kubectl get svc -n istio-system
# NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                                          AGE
# grafana            ClusterIP   10.233.39.70    <none>        3000/TCP                                         79d
# istiod             ClusterIP   10.233.60.184   <none>        15010/TCP,15012/TCP,443/TCP,15014/TCP            79d
# jaeger-collector   ClusterIP   10.233.30.185   <none>        14268/TCP,14250/TCP,9411/TCP,4317/TCP,4318/TCP   79d
# kiali              ClusterIP   10.233.3.216    <none>        20001/TCP,9090/TCP                               79d
# loki               ClusterIP   10.233.13.117   <none>        3100/TCP,9095/TCP                                79d
# loki-headless      ClusterIP   None            <none>        3100/TCP                                         79d
# loki-memberlist    ClusterIP   None            <none>        7946/TCP                                         79d
# prometheus         ClusterIP   10.233.38.209   <none>        9090/TCP                                         79d
# tracing            ClusterIP   10.233.30.211   <none>        80/TCP,16685/TCP                                 79d
# zipkin             ClusterIP   10.233.32.226   <none>        9411/TCP                                         79d

kubectl get pod -n istio-system
# NAME                          READY   STATUS    RESTARTS      AGE
# grafana-6c8c9948b6-r6k25      1/1     Running   1 (44m ago)   79d
# istiod-f65f49fb5-vfrdd        1/1     Running   1 (44m ago)   79d
# jaeger-7fdd85f699-r9qhx       1/1     Running   1 (44m ago)   79d
# kiali-744ff9cb54-qkvps        1/1     Running   1 (44m ago)   79d
# loki-0                        0/2     Pending   0             79d
# prometheus-6586f47dcc-shvs9   2/2     Running   2 (44m ago)   79d



```
###### Deploy the sample application
```
Установка базовго приложения и проверка доступности приклада во внутренней сети 
```

```bash 
kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml

# The application will start. As each pod becomes ready, the Istio sidecar will be deployed along with it.
$ kubectl get services

# NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
# details       ClusterIP   10.233.44.231   <none>        9080/TCP   29s
# example-app   ClusterIP   10.233.3.15     <none>        8080/TCP   289d
# kubernetes    ClusterIP   10.233.0.1      <none>        443/TCP    490d
# productpage   ClusterIP   10.233.15.72    <none>        9080/TCP   29s
# ratings       ClusterIP   10.233.41.207   <none>        9080/TCP   29s
# reviews       ClusterIP   10.233.25.187   <none>        9080/TCP   29s

kubectl get pods
# NAME                              READY   STATUS    RESTARTS   AGE
# details-v1-d689f847b-bctll        2/2     Running   0          97s
# productpage-v1-59ffbf8b65-2sdth   2/2     Running   0          97s
# ratings-v1-67b76f57b8-pdc6g       2/2     Running   0          97s
# reviews-v1-fc458f97b-gmw7g        2/2     Running   0          97s
# reviews-v2-75f48cdfc6-ln2j9       2/2     Running   0          97s
# reviews-v3-7ffcc4f88d-d9v2r       2/2     Running   0          97s


# Проверка что в контейнер приложения заехал istio как sidecar 
# Проверить в поде 
# kubectl describe pod <pod_name> -n <namespace_name>

kubectl describe pod productpage-v1-59ffbf8b65-2sdth -n default

#istio-proxy:
#    Container ID:  containerd://ffbe24a074bf182617eb6c310dfce705e692d11139d8f3bf4703827d17c97a1c
#    Image:         docker.io/istio/proxyv2:1.27.2
#    Image ID:      docker.io/istio/proxyv2@sha256:b00a23cb37e7b8e422b57e617c1bb7304955e368308b5c166e38f0444e0f5a08
#    Port:          15090/TCP
#    Host Port:     0/TCP
#    Args:
#      proxy
#      sidecar


# Validate that the app is running inside the cluster by checking for the page title in the response

kubectl exec "$(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"

<title>Simple Bookstore App</title>

```
###### Open the application to outside traffic

```bash
kubectl apply -f samples/bookinfo/gateway-api/bookinfo-gateway.yaml

# gateway.gateway.networking.k8s.io/bookinfo-gateway created
# httproute.gateway.networking.k8s.io/bookinfo created

# By default, Istio creates a LoadBalancer service for a gateway. As we will access this gateway by a tunnel, we don’t need a load balancer.
# Change the service type to ClusterIP by annotating the gateway:

kubectl annotate gateway bookinfo-gateway networking.istio.io/service-type=ClusterIP --namespace=default

kubectl get gateway

# NAME               CLASS   ADDRESS                                            PROGRAMMED   AGE
# bookinfo-gateway   istio   bookinfo-gateway-istio.default.svc.cluster.local   True         3m11s
```

###### Access the application
```bash 
# You will connect to the Bookinfo productpage service through the gateway you just provisioned. To access the gateway, you need to use the kubectl port-forward command:
kubectl port-forward svc/bookinfo-gateway-istio 8080:80

http://localhost:8080/productpage


curl http://localhost:8080/productpage | grep reviews 
# If you refresh the page, you should see the book reviews and ratings changing as the requests are distributed across the different versions of the reviews service.

# ...
#<title>Simple Bookstore App</title>
# ...
curl http://localhost:8080/productpage 

kubectl port-forward --address 0.0.0.0 svc/bookinfo-gateway-istio 8080:80
http://192.168.1.171:8080/productpage

```

###### View the dashboard
```bash
# install Kiali and the other addons and wait for them to be deployed.
kubectl apply -f samples/addons
kubectl rollout status deployment/kiali -n istio-system


# Access the Kiali dashboard.
istioctl dashboard kiali
kubectl port-forward --address 0.0.0.0 -n istio-system svc/kiali 20001:20001
kubectl port-forward --address 0.0.0.0 -n istio-system svc/kiali 30001:20001

http://192.168.1.171:30001/kiali 
```