```bash 


# Общие псевдонимы kubectl
alias k=kubectl
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
# Использование коротких имен для ресурсов
kubectl get po        # pods
kubectl get svc       # services
kubectl get deploy    # deployments
kubectl get ns        # namespaces
kubectl get no        # nodes
# Наблюдение за ресурсами на предмет изменений
kubectl get pods --watch
kubectl get events --watch

# Выбор по меткам
kubectl get pods -l app=nginx
kubectl get pods -l 'environment in (prod,staging)'
kubectl get pods -l app=nginx,version!=v1.0
# Выбор по полю
kubectl get pods --field-selector=status.phase=Running
kubectl get pods --field-
selector=spec.nodeName=worker-node-1
# Комбинирование селекторов
kubectl get pods -l app=nginx --field-
selector=status.phase=Running

# Различные форматы вывода
kubectl get pods -o wide
kubectl get pods -o yaml
kubectl get pods -o json
kubectl get pods -o name
# Пользовательские столбцы
kubectl get pods -o custom-
columns=NAME:.metadata.name,STATUS:.status.phase,N
ODE:.spec.nodeName
# Запросы JSONPath
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
kubectl get pods -o
jsonpath='{.items[*].spec.containers[*].image}'

# Сухой запуск для предварительного просмотра изменений
kubectl apply -f deployment.yaml --dry-run=client -o yaml
# Валидация конфигурации
kubectl apply -f deployment.yaml --validate=true --dry-
run=client
# Показать различия перед применением
kubectl diff -f deployment.yaml
# Принудительное удаление с периодом ожидания
kubectl delete pod  --grace-period=0 --force




# Получить информацию о кластере
kubectl cluster-info
# Получить конфигурацию кластера
kubectl config view
# Проверить доступные ресурсы API
kubectl api-resources
# Отобразить поддерживаемые версии API
kubectl api-versions

# Список всех узлов
kubectl get nodes
# Подробная информация об узлах
kubectl get nodes -o wide
# Описать конкретный узел
kubectl describe node
# Получить использование ресурсов узла
kubectl top nodes

# Список всех пространств имен
kubectl get namespaces
# Создать пространство имен
kubectl create namespace my-
namespace
# Удалить пространство имен
kubectl delete namespace my-
namespace
# Получить ресурсы в конкретном пространстве имен
kubectl get all -n my-namespace

# Запустить простой под
kubectl run nginx --image=nginx
# Создать под из YAML-файла
kubectl create -f pod.yaml
# Запустить под с командой
kubectl run busybox --image=busybox --echo "Hello World"
# Создать задание (job)
kubectl create job hello --image=busybox:1.28 --echo "Hello World"


# Список всех подов в пространстве имен по умолчанию
kubectl get pods
# Список подов с дополнительными деталями
kubectl get pods -o wide
# Список подов во всех пространствах имен
kubectl get pods --all-namespaces
# Наблюдение за изменениями статуса пода
kubectl get pods --watch

# Описать конкретный под
kubectl describe pod
# Описать под в конкретном пространстве имен
kubectl describe pod  -n

# Создать развертывание
kubectl create deployment nginx --image=nginx
# Создать развертывание с репликами
kubectl create deployment webapp --image=nginx --replicas=3
# Создать из YAML-файла
kubectl apply -f deployment.yaml
# Открыть развертывание как службу
kubectl expose deployment nginx --port=80 --type=LoadBalancer


# Список развертываний
kubectl get deployments
# Описать развертывание
kubectl describe deployment
# Редактировать развертывание
kubectl edit deployment
# Удалить развертывание
kubectl delete deployment

# Масштабировать развертывание
kubectl scale deployment nginx --replicas=5
# Масштабировать ReplicaSet
kubectl scale rs  --replicas=3
# Автомасштабирование развертывания
kubectl autoscale deployment nginx --min=2 --max=10 --cpu-percent=80

# Проверить статус развертывания
kubectl rollout status deployment/nginx
# Просмотр истории развертывания
kubectl rollout history deployment/nginx
# Откат к предыдущей версии
kubectl rollout undo deployment/nginx
# Откат к определенной ревизии
kubectl rollout undo deployment/nginx --to-revision=2

# Открыть развертывание как службу ClusterIP
kubectl expose deployment nginx --port=80
# Открыть как службу NodePort
kubectl expose deployment nginx --port=80 --type=NodePort
# Открыть как LoadBalancer
kubectl expose deployment nginx --port=80 --type=LoadBalancer
# Создать службу из YAML
kubectl apply -f service.yaml

# Список всех служб
kubectl get services
# Список служб с дополнительными деталями
kubectl get svc -o wide
# Описать конкретную службу
kubectl describe service
# Получить конечные точки службы
kubectl get endpoints

# Перенаправить порт пода на локальную машину
kubectl port-forward pod/ 8080:80
# Перенаправить порт службы
kubectl port-forward svc/ 8080:80
# Перенаправить порт развертывания
kubectl port-forward deployment/ 8080:80
# Перенаправить несколько портов
kubectl port-forward pod/ 8080:80 8443:443

# Список ресурсов Ingress
kubectl get ingress
# Описать Ingress
kubectl describe ingress
# Создать Ingress из YAML
kubectl apply -f ingress.yaml


# Создать ConfigMap из литералов
kubectl create configmap app-config --from-
literal=database_url=localhost --from-literal=debug=true
# Создать из файла
kubectl create configmap app-config --from-
file=app.properties
# Создать из каталога
kubectl create configmap app-config --from-file=config/

# Просмотр ConfigMap
kubectl get configmaps
kubectl describe configmap app-config
# Получить YAML ConfigMap
kubectl get configmap app-config -o yaml
# Редактировать ConfigMap
kubectl edit configmap app-config
# Удалить ConfigMap
kubectl delete configmap app-config

# Создать общий секрет
kubectl create secret generic db-secret --from-literal=username=admin --from-literal=password=secret123
# Создать секрет из файла
kubectl create secret generic ssl-certs --from-file=tls.crt --from-file=tls.key
# Создать секрет реестра docker
kubectl create secret docker-registry my-registry --docker-server=myregistry.com --docker-username=user --docker-password=pass

# Список секретов
kubectl get secrets
# Описать секрет (значения скрыты)
kubectl describe secret db-secret
# Декодировать значения секрета
kubectl get secret db-secret -o
jsonpath='{.data.password}' | base64 -d
# Удалить секрет
kubectl delete secret db-secret

# Список постоянных томов
kubectl get pv
# Описать постоянный том
kubectl describe pv
# Создать PV из YAML
kubectl apply -f persistent-volume.yaml
# Удалить постоянный том
kubectl delete pv

# Список PVC
kubectl get pvc
# Описать PVC
kubectl describe pvc
# Создать PVC из YAML
kubectl apply -f pvc.yaml
# Удалить PVC
kubectl delete pvc

# Список классов хранения
kubectl get storageclass
# Описать класс хранения
kubectl describe storageclass
# Установить класс хранения по умолчанию
kubectl patch storageclass  -p '{"metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

# Проверить монтирование томов в поде
kubectl describe pod  | grep -A5 "Mounts:"
# Список томов в поде
kubectl get pod  -o yaml | grep -A10 "volumes:"


# Просмотр логов пода
kubectl logs
# Следить за логами в реальном времени
kubectl logs -f
# Просмотр логов предыдущего контейнера
kubectl logs  --previous
# Просмотр логов конкретного контейнера
kubectl logs  -c
# Просмотр событий кластера
kubectl get events --sort-by=.metadata.creationTimestamp

# Описать под
kubectl describe pod
# Описать развертывание
kubectl describe deployment
# Описать службу
kubectl describe service
# Описать узел
kubectl describe node

# Использование ресурсов узлами
kubectl top nodes
# Использование ресурсов подами
kubectl top pods
# Использование ресурсов в пространстве имен
kubectl top pods -n
# Сортировка подов по использованию CPU
kubectl top pods --sort-by=cpu

# Выполнить интерактивную оболочку
kubectl exec -it  -- /bin/bash
# Отладка с помощью эфемерного контейнера (K8s 1.23+)
kubectl debug  -it --image=busybox
# Скопировать файлы из пода
kubectl cp :/path/to/file ./local-file
# Скопировать файлы в под
kubectl cp ./local-file :/path/to/destination

# Применить один файл
kubectl apply -f deployment.yaml
# Применить несколько файлов
kubectl apply -f deployment.yaml -f service.yaml
# Применить весь каталог
kubectl apply -f ./k8s-configs/
# Применить из URL
kubectl apply -f https://example.com/manifest.yaml
# Показать, что будет применено (сухой запуск)
kubectl apply -f deployment.yaml --dry-run=client -o yaml

# Получить все ресурсы в пространстве имен
kubectl get all
# Получить ресурсы с пользовательскими столбцами
kubectl get pods -o custom-
columns=NAME:.metadata.name,STATUS:.status.phase
# Получить ресурсы в формате JSON/YAML
kubectl get deployment nginx -o yaml
kubectl get pod  -o json
# Удалить ресурсы
kubectl delete -f deployment.yaml
kubectl delete pod,service -l app=nginx

# Редактировать ресурс интерактивно
kubectl edit deployment
# Патч ресурса с помощью стратегического слияния
kubectl patch deployment nginx -p '{"spec":{"replicas":3}}'
# Патч с помощью слияния JSON
kubectl patch pod  --type='json' -p='[{"op": "replace", "path": "/metadata/labels/env", "value": "prod"}]'
# Полностью заменить ресурс
kubectl replace -f updated-deployment.yaml

# Показать различия перед применением
kubectl diff -f deployment.yaml
# Объяснить структуру ресурса
kubectl explain pod.spec.containers
# Объяснить с примерами
kubectl explain deployment --recursive
# Проверить ресурс без применения
kubectl apply -f deployment.yaml --dry-run=client --
validate=true

# Отметить узел как недоступный для планирования
kubectl cordon
# Отметить узел как доступный для планирования
kubectl uncordon
# Осушить узел для обслуживания
kubectl drain  --ignore-daemonsets --delete-emptydir-
data
# Добавить "taint" к узлу
kubectl taint nodes  key=value:NoSchedule
# Удалить "taint" с узла
kubectl taint nodes  key:NoSchedule-

# Добавить метку к ресурсу
kubectl label pod  environment=production
# Удалить метку с ресурса
kubectl label pod  environment-
# Добавить аннотацию к ресурсу
kubectl annotate pod  description="Frontend web server"
# Выбрать ресурсы по метке
kubectl get pods -l environment=production
kubectl get pods -l 'environment in (production,staging)'

# Запустить прокси для API Kubernetes
kubectl proxy --port=8080
# Проверить, может ли пользователь выполнить действие
kubectl auth can-i create pods
kubectl auth can-i '*' '*' --as=system:serviceaccount:default:my-sa
# Выполнить действие от имени пользователя
kubectl get pods --as=system:serviceaccount:default:my-sa
# Просмотр информации об аутентификации пользователя
kubectl config view --raw -o jsonpath='{.users[*].name}'

# Ожидание условия
kubectl wait --for=condition=Ready pod/ --timeout=300s
# Запуск временного пода для тестирования
kubectl run tmp-pod --rm -i --tty --image=busybox --/bin/sh
# Генерация YAML ресурса без создания
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml
# Сортировка ресурсов по времени создания
kubectl get pods --sort-by=.metadata.creationTimestamp

# Использование ресурсов узлами
kubectl top nodes --sort-by=cpu
kubectl top nodes --sort-by=memory
# Использование ресурсов подами
kubectl top pods --sort-by=cpu
kubectl top pods --sort-by=memory -A
# Использование ресурсов контейнерами
kubectl top pods --containers=true
# Историческое использование ресурсов (требуется metrics-server)
kubectl top pods --previous

# Проверить статус развертывания
kubectl rollout status deployment/
# Проверить готовность пода
kubectl get pods --field-selector=status.phase=Running
# Мониторинг квот ресурсов
kubectl get resourcequota
kubectl describe resourcequota
# Проверить состояние компонентов кластера
kubectl get componentstatuses

# Просмотр запросов и лимитов ресурсов
kubectl describe node  | grep -A5 "Allocated resources:"
# Проверить бюджеты прерывания пода
kubectl get pdb
# Просмотр горизонтальных автомасштабировщиков подов
kubectl get hpa
# Проверить сетевые политики
kubectl get networkpolicy

# Просмотр запросов и лимитов ресурсов
kubectl describe node  | grep -A5 "Allocated resources:"
# Проверить бюджеты прерывания пода
kubectl get pdb
# Просмотр горизонтальных автомасштабировщиков подов
kubectl get hpa
# Проверить сетевые политики
kubectl get networkpolicy

# Резервное копирование всех ресурсов в пространстве имен
kubectl get all -o yaml -n  > backup.yaml
# Экспорт конкретного ресурса
kubectl get deployment  -o yaml > deployment-
backup.yaml
# Список всех ресурсов для резервного копирования
kubectl api-resources --verbs=list --namespaced -o name | xargs -n 1 kubectl get --show-kind --ignore-not-found -n

# Просмотр текущего контекста
kubectl config current-context
# Список всех контекстов
kubectl config get-contexts
# Переключение контекста
kubectl config use-context
# Создание нового контекста
kubectl config set-context dev-context --cluster=dev-cluster --user=dev-user --namespace=development


# Просмотр объединенного kubeconfig
kubectl config view
# Установка информации о кластере
kubectl config set-cluster  --server=https://cluster-api-url --certificate-authority=/path/to/ca.crt
# Установка учетных данных пользователя
kubectl config set-credentials  --client-certificate=/path/to/client.crt --client-key=/path/to/client.key
# Слияние файлов kubeconfig
KUBECONFIG=~/.kube/config:~/.kube/config2 kubectl config view --merge --flatten > ~/.kube/merged-config

# Установить пространство имен по умолчанию для
текущего контекста
kubectl config set-context --current --namespace=
# Установить другой формат вывода по умолчанию
kubectl config set-context --current --output=yaml
# Просмотр деталей конфигурации
kubectl config view -o jsonpath='{.users[*].name}'
kubectl config view --raw




```