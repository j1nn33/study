# Обновление сертификатов

###### Обновление сертификатов происходит автоматически при обновлении версии кластера.
###### Для обновления вручную можно использовать kubeadm.
###### Проверка срока жизни сертификатов. 
```
kubeadm certs check-expiration
```
###### Обратите внимание, что при установке кластера при помощи kubeadm сертификаты CA выписываются на 10 лет.
###### Обновление сертификатов необходимо проводить на каждой control ноде кластера. При помощи kubeadm 
###### возможно обновление всех сертификатов кластера (кроме сертификатов CA) или каждый сертификат можно 
###### обновлять отдельно.
```
kubeadm certs renew --help
```
###### Поскольку обычно все сертификаты живут около года, что бы не вносить путаницы лучше обновить их одной командой.
```
kubeadm certs renew all
```
###### После обновления сертификатов вы получаете следующее сообщение:
###### You must restart the kube-apiserver, kube-controller-manager, kube-scheduler and etcd, 
###### so that they can use the new certificates.
###### Т.е. мало обновить сертификаты, необходимо еще перезапустить приложения. Так же не стоит забывать про kubelet.

```
mkdir /tmp/kube
mv -f /etc/kubernetes/manifests/* /tmp/kube
sleep 45
mv -f /tmp/kube/* /etc/kubernetes/manifests
sleep 45
systemctl restart kubelet
systemctl status kubelet
```
###### Или так второй вариант
```
crictl pods -n kube-system --name 'kube-scheduler-*|kube-controller-manager-*|kube-apiserver-*|etcd-*' -q | xargs crictl rmp -f
until printf "" 2>>/dev/null >>/dev/tcp/127.0.0.1/6443; do sleep 1; done
systemctl restart kubelet
systemctl status kubelet
```
######  придётся рестартовать весь control plane и kubelet. 
###### Мне кажется, что проще это сделать перезагрузив ноду целиком.
```
kubectl drain control1.kube.local
reboot
```
###### Вы можете добавить процедуру обновления сертификатов в систему cron на 
###### сервере. Но не забывайте о необходимости перезапуска приложений.

###### kubectl
###### После обновления сертификатов, обновится конфигурационный файл клиента kubectl - /etc/kubernetes/admin.conf.
###### Если  делали символьную ссылку ~/.kube/config -> /etc/kubernetes/admin.conf, то ничего делать не надо.
###### Иначе, скопируйте файл к себе в домашнюю директорию.
###### И не забудьте поменять его во всех своих инструментах, используемых для доступа к API кластера.
```
cp -f /etc/kubernetes/admin.conf ~/.kube/config
```