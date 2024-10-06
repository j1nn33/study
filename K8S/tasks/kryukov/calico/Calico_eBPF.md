## Calico eBPF

```
Плюсы

- ускорение обработки пакетов и меньшую нагрузку на CPU при использовании сервисов kubernetes (замена kubernetes proxy).
- меньшие нагрузки на CPU и задержки при обработке правил Network Polices.
- оптимизация service mesh.

минусы:
- не простая отладка.
- не имеет смысла в небольших кластерах.
- не имеет смысла при малом количестве Network Polices.
```
#### Что такое eBPF

[eBPF](https://ebpf.io/) - это технология, которая может запускать программы в привилегированном контексте, ядра 
Linux. Что значительно ускоряет обработку данных.
```
Для выполнения программ, написанных на специальном языке программирования, в ядре Linux запускается виртуальная машина.

Перед загрузкой программы в виртуальную машину происходит ее обязательная проверка, во время которой выполняется
статический анализ кода. Если приложение может привести к сбою, зависанию или иным образом негативно влияют на работу 
ядра - оно не будет запущено.

Нас ePBF интересует с точки зрения работы с сетевым стеком ядра. Ядро Linux позволяет почти на каждое событие в
сетевом стеке подключать функции пользователя, и передаёт в эти функции обрабатываемый пакет. Это позволит
перенести обработку NAT и Network Polices на уровень ядра.
```
#### Calico и eBPF
```
Calico поддерживает три технологии для организации работы сервисов (NAT преобразования): iptables, ipvs и ePBF.

Iptables является самым медленным и не приспособленным для обработки большого количества преобразований. Поэтому его
сейчас практически не используют.

ipvs упрощает и ускоряет обработку пакетов. Добавляет специальный виртуальный сетевой интерфейс. В большинстве случаев
ipvs хватает для работы сети кластера. Но если вдруг вы почувствовали что сеть торомозит - то следующий шаг это переход 
на ePBF.

При включении ePBF от calico необходимо выключить kube-proxy, calico берет на себя функцию NAT. Переход с ipvs 
на eBPF на работающем кластере может положить кластер кубера. Поэтому - не надо переходить на eBPF на работающем 
кластере. Существует не маленькая вероятность его поломать. Поставьте рядом новый кластер и перенесите приложения на
него.
```
Так же необходимо посмотреть, какие 
[платформы и дистрибутивы kubernetes поддерживаются](https://docs.tigera.io/calico/latest/operations/ebpf/enabling-ebpf#supported).


#### Не рабочие способы [Подробнее](https://github.com/BigKAA/youtube/blob/master/net/06-calico%20ebpf/README.md)
- Переход на eBPF текущего кластера
- Установка при помощи calico operator https://docs.tigera.io/calico/latest/operations/ebpf/install

[Подробнее](https://github.com/BigKAA/youtube/blob/master/net/06-calico%20ebpf/README.md)
#### Рабочий

```
Устанавливать calico bpf надо строго на новом кластере, в момент его первоначальной установки.
Установка из манифестов. 
В дальнейшем нам не понадобится kube-proxy, поскольку все nat преобразования возьмёт на себя calico bpf. Поэтому
выключаем его установку во время инициализации мастер ноды.  
```
```shell
kubeadm init --config /etc/kubernetes/kubeadm-config.yaml --skip-phases=addon/kube-proxy
```

Добавляем nodelocaldns (_почти все дальнейшие скрипты, конфигурационные файлы и пути к ним, взяты из плейбука_./study/K8S/ansible/kubeadm)

```shell
kubectl apply -f /etc/kubernetes/nodelocaldns-daemonset.yaml
```

Поскольку kube-proxy не установлен, добавим ConfigMap необходимый для дальнейшей работы calico, содержащий переменные
указывающие на точку подключения к kubernetes API.  ./K8S/ansible/kubeadm/roles/master/templates/kubernetes-services-endpoint.j2

```yaml
kind: ConfigMap
apiVersion: v1
metadata:
  name: kubernetes-services-endpoint
  namespace: kube-system
data:
  KUBERNETES_SERVICE_HOST: "192.168.218.171"
  KUBERNETES_SERVICE_PORT: "6443"
```

```shell
kubectl apply -f /etc/kubernetes/kubernetes-services-endpoint.yaml
```

Скачаем актуальный манифест calico. правим и помещаем сюда ./K8S/ansible/kubeadm/roles/master/templates/calico.j2

```shell
curl https://raw.githubusercontent.com/projectcalico/calico/v3.26.4/manifests/calico-typha.yaml -o calico.yaml
```

Редактируем. Ищем `- name: CALICO_IPV4POOL_CIDR`, в `value` подставляем CIDR.

Так же ставим режим VXLAN, поскольку режим IPIP в случае BPF прироста в скорости не дает.

```yaml
            # Enable IPIP
            - name: CALICO_IPV4POOL_IPIP
              value: "Never"
            # Enable or Disable VXLAN on the default IP pool.
            - name: CALICO_IPV4POOL_VXLAN
              value: "Always"
```

Применяем манифест:

```shell
kubectl apply -f calico.yaml
```

Устанавливаем утилиту `calicoctl`:

```shell
curl -L https://github.com/projectcalico/calico/releases/download/v3.26.4/calicoctl-linux-amd64 -o calicoctl
chmod +x ./calicoctl
mv calicoctl /usr/local/bin
```

На данный момент у нас BPF ещё не включен. Включаем его, добавив параметр `bpfEnabled: true` в FelixConfiguration:

```yaml
apiVersion: projectcalico.org/v3
kind: FelixConfiguration
metadata:
  name: default
spec:
  bpfLogLevel: ""
  floatingIPs: Disabled
  logSeverityScreen: Info
  reportingInterval: 0s
  bpfEnabled: true
```

```shell
calicoctl apply -f felix-configuration.yaml
```

Добавляем остальные ноды к кластеру.

Ждем когда заработают все поды в namespace `kube-system`.

```shell
watch kubectl -n kube-system get pods
```

Заходим в любой под calico-node и убеждаемся, что NAT преобразования переехали в BPF.

```shell
kubectl -n kube-system get pods | grep node
```

```shell
kubectl exec -it -n kube-system calico-node-5j8cm -- bash
```

Внутри пода выполняем команду:

```shell
calico-node -bpf nat dump
```

------------------------
#### Автоматизация описана тут  ./study/K8S/ansible/kubeadm
```
Для роли 
./K8S/ansible/kubeadm/install-1-st-control.yaml

в зависимости от настроек
./K8S/ansible/kubeadm/group_vars/k8s_cluster

### To install ePBF uncomment next line
# enableBPF: yes

./K8S/ansible/kubeadm/roles/master/tasks/main.yaml
#- name: Install Calico with BPF
#  when: enableBPF is defined
#  include_tasks: calico-bpf.yaml


```
