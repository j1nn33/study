

```bash
#
kubectl get crd | grep istio


# получить обзор сетки
./istio-1.27.2/bin/istioctl proxy-status
# NAME                                                CLUSTER        ISTIOD                     VERSION     SUBSCRIBED TYPES
# bookinfo-gateway-istio-85dc8cd865-xd495.default     Kubernetes     istiod-f65f49fb5-vfrdd     1.27.2      4 (CDS,LDS,EDS,RDS)

# Проверка наличия механизма внедрения Istio
 kubectl -n istio-system get deployment -l istio=sidecar-injector

# куда\ на какие namespace навешивается механизм внедрения Istio
kubectl get namespace -L istio-injection

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
```
```
узнать внешний IP-адрес сервиса Ingress Gateway

kubectl get svc -n istio-system -l istio=ingressgateway
NAME                   TYPE           CLUSTER-IP     EXTERNAL-IP
istio-ingressgateway   LoadBalancer   10.0.0.1       хх.хх.30.120
поместить его в переменную 
EXTERNAL_IP=$(kubectl get svc -n istio-system \
  -l app=istio-ingressgateway \
  -o jsonpath='{.items[0].status.loadBalancer.ingress[0].ip}')
  
  
При заходе по ip получим что сервис не доступен
по умолчанию Istio блокирует весь входящий трафик, пока не определён Gateway.

шлюз разрешает доступ к порту 80, но не имеет представления о том, куда маршрутизировать запросы. Для этого понадобятся Virtual Services.

```


```bash
while true; do \
   curl -i http://$EXTERNAL_IP/sentiment \
   -H "Content-type: application/json" \
   -d '{"sentence": "I love yogobella"}' \
   --silent -w "Time: %{time_total}s \t Status: %{http_code}\n" \
   -o /dev/null; sleep .1; done
# Time: 0.153075s Status: 200
# Time: 0.137581s Status: 200
# Time: 0.139345s Status: 200
# Time: 30.291806s Status: 500
```