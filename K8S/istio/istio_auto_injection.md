#### Автоматичекское внедрение istio sidecar

```bash
# добавление метки на namespace для автовнедрения
kubectl label namespace default istio-injection=enabled

# Какие пространства имен Kubernetes имеют метку istioinjection?
kubectl get namespace -L istio-injection
# NAME           STATUS    AGE       ISTIO-INJECTION
# default        Active    1h        enabled

```

### Init-контейнеры 
```
используются для выполнения задач инициализации ресурсов, таких как объединение 
активов, миграция баз данных или клонирование Git-репозитория

 
В случае Istio init-контейнеры используются для настройки сетевых фильтров – iptables, – управляющих трафиком.
```