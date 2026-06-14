##### Downward API 
```
https://kubernetes.io/docs/concepts/workloads/pods/downward-api/
```

```
Позволяет ППО(которое работае в контейнере) получать некоторую информацию об окружении (поде, имя пода, ip, статусе) без 
обращения к k8s API 

инфа получается 2 способами
- переменные окружения (ENV)
- через файлы в volumes  (позволяте забирать несколько больше информации )

```
###### ENV

```
работает так переменная в прикладе получает значение
через  
valueFrom.fieldRef.<INFO>

metadata.name                  the pod's name
metadata.namespace             the pod's namespace
metadata.uid                   the pod's unique ID
metadata.annotations['<KEY>']  the value of the pod's annotation named <KEY> (for example, metadata.annotations['myannotation'])
metadata.labels['<KEY>']       the text value of the pod's label named <KEY> (for example, metadata.labels['mylabel'])

# нельзя получить через volumes
# ./study/K8S/tasks/kryukov/local_volumes/09_openresty_downwardAPI.yaml

spec.serviceAccountName        the name of the pod's service account
spec.nodeName                  the name of the node where the Pod is executing
status.hostIP                  the primary IP address of the node to which the Pod is assigned
status.hostIPs                 the IP addresses is a dual-stack version of status.hostIP, the first is always the same as status.hostIP.
status.podIP                   the pod's primary IP address (usually, its IPv4 address)
status.podIPs                  the IP addresses is a dual-stack version of status.podIP, the first is always the same as status.podIP
metadata.labels                all of the pod's labels, formatted as label-key="escaped-label-value" with one label per line
metadata.annotations           all of the pod's annotations, formatted as annotation-key="escaped-annotation-value" with one annotation per line

resource: limits.cpu                  A container's CPU limit
resource: requests.cpu                A container's CPU request
resource: limits.memory               A container's memory limit
resource: requests.memory             A container's memory request
resource: limits.hugepages-*          A container's hugepages limit
resource: requests.hugepages-*        A container's hugepages request
resource: limits.ephemeral-storage    A container's ephemeral-storage limit
resource: requests.ephemeral-storage  A container's ephemeral-storage request

```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
    - name: my-container
      image: my-image
      env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace

```
```
Пример 
запускаем под в котором выводяться переменные 

./study/K8S/tasks/kryukov/downwardapi/downward_api_test_pod.yaml
```
```bash
kubectl apply -f downward_api_test_pod.yaml

kubectl get pods
# NAME                    READY   STATUS    RESTARTS   AGE
# downward-api-demo-env   1/1     Running   0          44s

kubectl logs downward-api-demo-env
# -------
# Pod Name: downward-api-demo-env
# Pod Namespace: default
# Pod IP: 10.233.64.15
# Node name: control1.kube.local
# App Label: test

kubectl delete -f downward_api_test_pod.yaml --force
```
###### volume
```
- смонтировать информацию как файлы в volume типа downwardAPI
- более гибкий позволяте запихать больше инфы
- инфа обновляется автоматически (искл subPath)

downward_api_test_pod_2.yaml
```
```bash
kubectl apply -f downward_api_test_pod_2.yaml

kubectl get pods
# NAME                       READY   STATUS    RESTARTS   AGE
# downward-api-demo-volume   1/1     Running   0          13s

kubectl logs downward-api-demo-volume
# -------
# Pod Name: downward-api-demo-volume
# Pod Namespace: default
# App Label:
# app.kubernetes.io/instance="test"
# app.kubernetes.io/name="downward-demo-volume"
# app.kubernetes.io/version="v0.0.1"
# 
# Annotations:
# kubectl.kubernetes.io/last-applied-configuration="{\"apiVersion\":\"v1\",\"kind\":\"Pod\",\"metadata\":{\"annotations\":{},\"labels\":{\"app.kubernetes.io/instance\":\"test\",\"app.kubernetes.io/name\":\"downward-demo-volume\",\"app.kubernetes.io/version\":\"v0.0.1\"},\"name\":\"downward-api-demo-volume\",\"namespace\":\"default\"},\"spec\":{\"containers\":[{\"args\":[\"echo \\\"-------\\\";\\necho \\\"Pod Name: $(cat /etc/podinfo/pod_name)\\\";\\necho \\\"Pod Namespace: $(cat /etc/podinfo/pod_namespace)\\\";\\necho \\\"App Label:\\n$(cat /etc/podinfo/labels)\\n\\\";\\necho \\\"Annotations:\\n$(cat /etc/podinfo/annotations)\\n\\\";\\necho \\\"CPU Limit\\\" $(cat /etc/podinfo/cpu_limit)\\\";\\necho \\\"Memory Limits $(cat /etc/podinfo/memory_limit)\\\";\\\"\\nsleep infinity\\n\"],\"command\":[\"sh\",\"-c\"],\"image\":\"busybox:1.37\",\"name\":\"main\",\"resources\":{\"limits\":{\"cpu\":\"200m\",\"memory\":\"64Mi\"},\"requests\":{\"cpu\":\"200m\",\"memory\":\"32Mi\"}},\"volumeMounts\":[{\"mountPath\":\"/etc/podinfo\",\"name\":\"podinfo\"}]}],\"restartPolicy\":\"Never\",\"volumes\":[{\"downwardAPI\":{\"items\":[{\"fieldRef\":{\"fieldPath\":\"metadata.name\"},\"path\":\"pod_name\"},{\"fieldRef\":{\"fieldPath\":\"metadata.namespace\"},\"path\":\"pod_namespace\"},{\"fieldRef\":{\"fieldPath\":\"metadata.labels\"},\"path\":\"labels\"},{\"fieldRef\":{\"fieldPath\":\"metadata.annotations\"},\"path\":\"annotations\"},{\"path\":\"cpu_limit\",\"resourceFieldRef\":{\"containerName\":\"main\",\"divisor\":\"1\",\"resource\":\"limits.cpu\"}},{\"path\":\"memory_limit\",\"resourceFieldRef\":{\"containerName\":\"main\",\"divisor\":\"1Mi\",\"resource\":\"limits.memory\"}}]},\"name\":\"podinfo\"}]}}\n"
# kubernetes.io/config.seen="2026-06-14T17:54:41.806305115+03:00"
# kubernetes.io/config.source="api"
# 
# CPU Limit 1;
# Memory Limits 64;

kubectl delete -f downward_api_test_pod_2.yaml --force
```
###### Динамическое обновление данных
```
пример пода который периодически считывает метки и выводит их в лог
```
```bash

kubectl apply -f downward_api_test_pod_3.yaml

kubectl get pods
# NAME                        READY   STATUS    RESTARTS   AGE
# downward-api-demo-dynamic   1/1     Running   0          7s

kubectl logs downward-api-demo-dynamic

# Reading labels at Sun Jun 14 15:19:24 UTC 2026:
# app.kubernetes.io/name="downward-demo-dynamic"
# status="pending"-------


# Меняем статус на running 
kubectl label pod downward-api-demo-dynamic status=running --overwrite
# pod/downward-api-demo-dynamic labeled

kubectl logs downward-api-demo-dynamic

# Reading labels at Sun Jun 14 15:23:24 UTC 2026:
# app.kubernetes.io/name="downward-demo-dynamic"
# status="pending"-------
# Reading labels at Sun Jun 14 15:23:34 UTC 2026:
# app.kubernetes.io/name="downward-demo-dynamic"
# status="running"-------
# Reading labels at Sun Jun 14 15:23:44 UTC 2026:
# app.kubernetes.io/name="downward-demo-dynamic"


# смотрим, что внутри пода

kubectl exec downward-api-demo-dynamic -it -- ls -la /etc/podinfo

# drwxrwxrwt    3 root     root           100 Jun 14 15:23 .
# drwxr-xr-x    1 root     root            69 Jun 14 15:19 ..
# drwxr-xr-x    2 root     root            60 Jun 14 15:23 ..2026_06_14_15_23_29.1498059607
# lrwxrwxrwx    1 root     root            32 Jun 14 15:23 ..data -> ..2026_06_14_15_23_29.1498059607
# lrwxrwxrwx    1 root     root            13 Jun 14 15:19 labels -> ..data/labels

kubectl delete -f downward_api_test_pod_3.yaml --force
```