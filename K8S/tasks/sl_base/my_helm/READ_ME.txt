# мануал по созданию см MANUALS/K8S/helm/My_new_chart.txt 
# 
#
cd ~
mkdir myapp

cd myapp

touch Chart.yaml values.yaml
mkdir templates

cp ~/deployment.yaml ~/myapp/templates/

# Проверим что рендеринг чарта работает

helm template .

# Для проверки используем ту же команду, но с доп ключом:

helm template . --name-template  release-1.1

/my_helm$ helm install . --name-template release-1.1 --dry-run --debug

# см secret если при отлаживании будет ругаться на то что уже есть
------------------------
kubectl get all -o wide

kubectl run test --image=centosadmin/utils:0.3 -it bash

kubectl exec test -it bash

--------------
curl <ip-адрес сервиса>
curl my-service
(возвращает имя пода)
exit

helm list
helm delete <name>
