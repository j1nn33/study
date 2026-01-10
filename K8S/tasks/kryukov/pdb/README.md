#### PDB 
```
Video https://rutube.ru/video/f5eab5236002477564061fff12a6af26/
PodDisruptionBudget (PDB) — это механизм в Kubernetes, который позволяет администраторам контролировать, сколько подов (pods) приложения могут быть одновременно недоступны во время плановых или внеплановых событий:
— Обновления узлов (node drain, node upgrades)
— Масштабирование кластера
— Ручное удаление подов (например, `kubectl delete pod`)

параметры могут назначаться числом (кол-во pod)
процентами (округление всегда в большую сторону)

You can specify only one of maxUnavailable and minAvailable in a single PodDisruptionBudget
```
```bash
Check the status of the PDB

kubectl get poddisruptionbudgets
# NAME     MIN AVAILABLE   MAX UNAVAILABLE   ALLOWED DISRUPTIONS   AGE

ALLOWED DISRUPTIONS - сколько можно удалить

```
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: zk-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: zookeeper
```
или 
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: zk-pdb
spec:
  maxUnavailable: 1
  selector:
    matchLabels:
      app: zookeeper

```
```
Ограничения PDB
— Не защищает от неплановых сбоев (например, падение узла).
— Работает только с добровольными удалениями (не принудительными `kubectl delete pod —force`).
- можно удалить поды уменьшив replicaset
```