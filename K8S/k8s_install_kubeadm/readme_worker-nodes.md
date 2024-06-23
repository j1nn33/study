# Добавление worker ноды

###### в кластере должно быть нечётное количество control нод.
###### После создания первой ноды кластера, kubeadm выведет на стандартный вывод команды для добавления новых нод.
###### Если не прошло больше суток после создания первой control ноды, то эти команды можно использовать для добавления.
###### Если прошло больше суток (время жизни сгенерированного токена), то действия описаны ниже
###### 
###### Посмотреть список токенов можно следующим образом: 
```
kubeadm token list
```
###### В столбце TTL будет показано, сколько времени осталось до окончания действия токена.

###### Подготовительные шаги
###### создадим новый токен (_join_token_).
```
kubeadm token create
```
###### Программа выдаст на стандартный вывод новый токен. Что-то типа: `mpihje.kh1irgs7hbswsxgj`.


###### Так же нам потребуется хеш сертификата CA (_ca_cert_hash_):
```
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | \
  openssl rsa -pubin -outform der 2>/dev/null | \
  openssl dgst -sha256 -hex | sed 's/^.* //'
```

###### На стандартном выводе получим что-то типа: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.


###### На следующем шаге поместим сертификаты в secret `kubeadm-certs` в namespace `kube-system`.
```
kubeadm init phase upload-certs --upload-certs | tail -1
```
###### В последней строке получим ключ сертификата (_certificate_key_). Что-то 
###### вроде: `97d3b9cf6d10e70abcd73ae4783b9b1c8cd8be3703b229df6122e17a6aa166b6`.

###### Можно посмотреть содержимое сгенерированного сикрета:
```
kubectl -n kube-system get secret kubeadm-certs -o yaml
```
###### получим путь (_join_path_), по которому будем посылать запрос на подключение.
```
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}' | cut -c9-
```
###### На стандартном выводе должны получить IP адрес и порт 192.168.1.189:7443

###### Подключение дополнительных control нод
###### Команда для подключения control ноды будет следующая:

###### join_path         192.168.1.189:7443
###### join_token         mpihje.kh1irgs7hbswsxgj
###### ca_cert_hash       e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
###### certificate_ke     97d3b9cf6d10e70abcd73ae4783b9b1c8cd8be3703b229df6122e17a6aa166b6
```
kubeadm join join_path --token <join_token> \
  --discovery-token-ca-cert-hash sha256:<ca_cert_hash> \
  --control-plane --certificate-key <certificate_key>
```
###### Подставьте свои значения и запустите команду на остальных серверах, где планируется разместить control ноды.
```
kubeadm join 192.168.1.189:7443 --token mpihje.kh1irgs7hbswsxgj \
  --discovery-token-ca-cert-hash sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 \
  --control-plane --certificate-key 97d3b9cf6d10e70abcd73ae4783b9b1c8cd8be3703b229df6122e17a6aa166b6
```

###### Убедитесь, что control ноды добавлены в кластер.
```
kubectl get nodes
kubectl get pods -A
```

## Ansible 
```
ansible-playbook services/install-workers.yaml 

kubectl get nodes
watch kubectl get nodes
```
###### готово будет когда все pods будут в стутусе Running
```
kubectl get pods -A
```