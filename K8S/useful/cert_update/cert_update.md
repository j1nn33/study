# Обновление сертификатов  
Исходная статься  https://github.com/BigKAA/youtube/blob/master/kubeadm/certificates.md

Дополнительно     https://facsiaginsa.com/kubernetes/renew-kubernetes-certificate

Документация      https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/

Обновление сертификатов происходит автоматически при обновлении версии кластера.

Для обновления вручную можно использовать kubeadm.

Проверка срока жизни сертификатов. 

```shell
kubeadm certs check-expiration

# Выборочно посмотереть
# Сертификат api-server, порт 6443

echo -n | openssl s_client -connect localhost:6443 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | openssl x509 -text -noout | grep Not
            Not Before: Jun 18 17:51:46 2024 GMT
            Not After : Jun 18 17:56:46 2025 GMT

# Сертификат controller manager, порт 10257.
echo -n | openssl s_client -connect localhost:10257 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | openssl x509 -text -noout | grep Not
            Not Before: May 25 06:53:43 2025 GMT
            Not After : May 25 06:53:43 2026 GMT
# Сертификат scheduler, порт 10259.			
echo -n | openssl s_client -connect localhost:10259 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | openssl x509 -text -noout | grep Not
            Not Before: May 25 06:54:03 2025 GMT
            Not After : May 25 06:54:03 2026 GMT
			
#			
echo -n | openssl s_client -connect localhost:2379 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' | openssl x509 -text -noout | grep Not
            Not Before: Jun 18 17:51:47 2024 GMT
            Not After : Jun 18 17:56:47 2025 GMT


```

Backup Old Certificates
Before we renew the certificate, it is better to back up our existing configuration & certificate so we can use it later if the renewing process fails.
We can copy them to /tmp folder on your Kubernetes master node.

```shell
mkdir /tmp/k8s-backup
cp /etc/kubernetes/*.conf /tmp/k8s-backup
cp -r /etc/kubernetes/pki /tmp/k8s-backup
```

при установке кластера при помощи kubeadm сертификаты CA выписываются на 10 лет.

Обновление сертификатов необходимо проводить на каждой control ноде кластера - это важно. 
#### обновляемся на каждой control ноде кластера
При помощи kubeadm возможно обновление всех сертификатов кластера (кроме сертификатов CA) или каждый сертификат можно 
обновлять отдельно.

```shell
kubeadm certs renew --help
```

Поскольку обычно все сертификаты живут около года, что бы не вносить путаницы лучше обновить их одной командой.

```shell
kubeadm certs renew all
```

После обновления сертификатов вы получаете следующее сообщение:

```
You must restart the kube-apiserver, kube-controller-manager, kube-scheduler and etcd, 
so that they can use the new certificates.
```

Т.е. мало обновить сертификаты, необходимо еще перезапустить приложения. Так же не стоит забывать про kubelet.

```shell
mkdir /tmp/kube
mv -f /etc/kubernetes/manifests/* /tmp/kube
sleep 45
mv -f /tmp/kube/* /etc/kubernetes/manifests
sleep 45
systemctl restart kubelet
systemctl status kubelet
```

Или так ([из kubespray](https://github.com/kubernetes-sigs/kubespray/blob/master/roles/kubernetes/control-plane/templates/k8s-certs-renew.sh.j2)):

```shell
crictl pods -n kube-system --name 'kube-scheduler-*|kube-controller-manager-*|kube-apiserver-*|etcd-*' -q | xargs crictl rmp -f
until printf "" 2>>/dev/null >>/dev/tcp/127.0.0.1/6443; do sleep 1; done
systemctl restart kubelet
systemctl status kubelet
```

Вобщем вам придётся рестартовать весь control plane и kubelet. 
проще это сделать перезагрузив ноду целиком.

```shell
kubectl drain control1.kryukov.local
reboot
```

Вы можете добавить процедуру обновления сертификатов в систему cron на 
сервере. Но не забывайте о необходимости перезапуска приложений.

## kubectl

После обновления сертификатов, обновится конфигурационный файл клиента kubectl - `/etc/kubernetes/admin.conf`.

Если вы, как я рекомендовал, делали символьную ссылку `~/.kube/config` -> `/etc/kubernetes/admin.conf`, то
ничего делать не надо.

Иначе, скопируйте файл к себе в домашнюю директорию.

```shell
cp -f /etc/kubernetes/admin.conf ~/.kube/config
```

И не забудьте поменять его во всех своих инструментах, используемых для доступа к API кластера.

## Интересное

Статья на Хабре "[Ломаем и чинимKubernetes](https://habr.com/ru/post/541118/)".