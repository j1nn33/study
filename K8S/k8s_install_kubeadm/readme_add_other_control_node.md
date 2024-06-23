# Добавление control nodes

######    в кластере должно быть нечётное количество control нод.
######    После создания первой ноды кластера, kubeadm выведет на стандартный вывод команды для добавления новых нод.
######    Если не прошло больше суток после создания первой control ноды, то эти команды можно использовать для добавления.
######    Если прошло больше суток (время жизни сгенерированного токена), то действия описаны ниже
######   
######    Посмотреть список токенов можно следующим образом: 

  kubeadm token list

######    В столбце TTL будет показано, сколько времени осталось до окончания действия токена.
######    Подготовительные шаги
######    создадим новый токен (_join_token_).

  kubeadm token create

######     Программа выдаст на стандартный вывод новый токен. Что-то типа: `mpihje.kh1irgs7hbswsxgj`.

######     Так же нам потребуется хеш сертификата CA (_ca_cert_hash_):

  openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | \
        openssl rsa -pubin -outform der 2>/dev/null | \
        openssl dgst -sha256 -hex | sed 's/^.* //'


###### На стандартном выводе получим что-то типа: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.


###### На следующем шаге поместим сертификаты в secret `kubeadm-certs` в namespace `kube-system`.

  kubeadm init phase upload-certs --upload-certs | tail -1

###### В последней строке получим ключ сертификата (_certificate_key_). Что-то 
###### вроде: `97d3b9cf6d10e70abcd73ae4783b9b1c8cd8be3703b229df6122e17a6aa166b6`.

###### Можно посмотреть содержимое сгенерированного сикрета:
  kubectl -n kube-system get secret kubeadm-certs -o yaml

###### получим путь (_join_path_), по которому будем посылать запрос на подключение.

  kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}' | cut -c9-

###### На стандартном выводе должны получить IP адрес и порт 192.168.1.189:7443

###### Подключение дополнительных control нод
###### Команда для подключения control ноды будет следующая:

###### join_path         192.168.1.189:7443
###### join_token         mpihje.kh1irgs7hbswsxgj
###### ca_cert_hash       e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
###### certificate_ke     97d3b9cf6d10e70abcd73ae4783b9b1c8cd8be3703b229df6122e17a6aa166b6

  kubeadm join join_path --token <join_token> \
    --discovery-token-ca-cert-hash sha256:<ca_cert_hash> \
    --control-plane --certificate-key <certificate_key>

###### Подставьте свои значения и запустите команду на остальных серверах, где планируется разместить control ноды.

  kubeadm join 192.168.1.189:7443 --token mpihje.kh1irgs7hbswsxgj \
    --discovery-token-ca-cert-hash sha256:e3b0c44298fc1c149afbf4c89 96fb92427ae41e4649b934ca495991b7852b855 \
    --control-plane --certificate-key 97d3b9cf6d10e70abcd73ae4783b9b  1c8cd8be3703b229df6122e17a6aa166b6


###### Убедитесь, что control ноды добавлены в кластер.

  kubectl get nodes
  kubectl get pods -A


###### Поправим coredns
###### Посмотрим, на каких нодах работают поды coredns.

  kubectl -n kube-system get pods -o wide | grep coredn s

###### coredns-76f75df574-8rphj                      1/1     Running   1 (22m ago)   3d14h   10.233.66.11    control1.kube.local   <none>           <none>
###### coredns-76f75df574-g99ql                      1/1     Running   1 (22m ago)   3d14h   10.233.66.9     control1.kube.local   <none>           <none>
 

###### Есть нюанс что они висят на одной ноде  
###### Несмотря на то, что в Deployment корректно настроен podAntiAffinity, он не сработает до тех пор, пока в системе не появятся
###### новые ноды кластера и мы не перезапустим Deployment.

  kubectl -n kube-system rollout restart deployment coredns

###### Убедимся, что поды DNS сервера разъехались по разным нодам кластера.

  kubectl -n kube-system get pods -o wide | grep coredns

###### coredns-6d87999bc6-cwnhf                      1/1     Running   0             67s     10.233.87.2     control2.kube.local   <none>           <none>
###### coredns-6d87999bc6-s7b4s                      1/1     Running   0             66s     10.233.81.194   control3.kube.local   <none>           <none>

---
###### Ansible 

  ansible-playbook services/install-another-controls.yaml 

  kubectl -n kube-system get pods -o wide | grep coredns
  kubectl -n kube-system rollout restart deployment coredns
  kubectl -n kube-system get pods -o wide | grep coredns