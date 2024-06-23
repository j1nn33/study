## Структура стенда.

###### - 8 виртуальных машин.
###### - В Ubuntu установлен ansible: 192.168.1.169

```
master.kube.local               (RAM 1GB, CPU 1, 10Gb, 120GB) - вспомогательная машина. 
                                   * Кеширующий DNS сервер для машин тестового стенда.
                                   * Поддержка зоны kube.local.
                                   * NFS сервер
control[1,2,3].kube.local       (RAM 4GB, CPU 4, 20Gb) - control nodes кластера kubernetes.
worker[1,2,3].kube.local        (RAM 8GB, CPU 6, 20Gb) - общие worker nodes кластера kubernetes.
db1.kube.local                  (RAM 4GB, CPU 4, 60Gb)** - дополнительная worker node. для базы данных 
```
###### На всех машинах, кроме master, установлен AlmaLinux 8 установлено должно быть dnf install python3
###### Маршрут по умолчанию на всех машинах идёт на мой локальный роутер 192.168.1.1
###### ipv6 - не отключать amation
###### Клиенты DNS настроены на машину master. 

## DNS сервер
##### хост с ansible ubuntu 192.168.1.169
```

bastion         IN      A       192.168.1.169   ansible
master          IN      A       192.168.1.170   DNS NFS      
control1        IN      A       192.168.1.171
control2        IN      A       192.168.1.172
control3        IN      A       192.168.1.173
worker1         IN      A       192.168.1.174
worker2         IN      A       192.168.1.175
worker3         IN      A       192.168.1.176
db1             IN      A       192.168.1.177
```

##### На машине master установлен DNS server BIND.

##### В файл `/etc/named.conf` добавлена поддержка двух зон: `kube.local` и `1.168.192.in-addr.arpa`.

```
options {
        listen-on port 53 { any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        secroots-file   "/var/named/data/named.secroots";
        recursing-file  "/var/named/data/named.recursing";
        forwarders { 192.168.1.1; };
        allow-query     { any; };
        recursion yes;
        dnssec-validation no;
        managed-keys-directory "/var/named/dynamic";
        pid-file "/run/named/named.pid";
        session-keyfile "/run/named/session.key";
        include "/etc/crypto-policies/back-ends/bind.config";
};
logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};
zone "." IN {
        type hint;
        file "named.ca";
};
zone "kube.local" IN {
        type master;
        file "kube.local";
};
zone "1.168.192.in-addr.arpa" IN {
        type master;
        file "1";
};
include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```

##### Файлы описания зон находятся в директории /var/named/kube.local

```
$TTL 86400
@ IN SOA kube.local. master.kube.local. (
                                                2022120100 ;Serial
                                                3600 ;Refresh
                                                1800 ;Retry
                                                604800 ;Expire
                                                86400 ;Minimum TTL
)

@ IN NS master

master          IN      A       192.168.1.170
control1        IN      A       192.168.1.171
control2        IN      A       192.168.1.172
control3        IN      A       192.168.1.173
worker1         IN      A       192.168.1.174
worker2         IN      A       192.168.1.175
worker3         IN      A       192.168.1.176
db1             IN      A       192.168.1.177

metallb         IN      A       192.168.1.180
argocd          IN      CNAME   metallb
keycloak        IN      CNAME   metallb

kubeapi         IN      A       192.168.1.189
```

/var/named/1

```
$TTL 86400
@ IN SOA kube.local. master.kube.local. (
                                            2022120100 ;Serial
                                            3600 ;Refresh
                                            1800 ;Retry
                                            604800 ;Expire
                                            86400 ;Minimum TTL
)

@ IN NS master.kube.local.

170     IN      PTR     master.kube.local.
171     IN      PTR     control1.kube.local.
172     IN      PTR     control2.kube.local.
173     IN      PTR     control3.kube.local.
174     IN      PTR     worker1.kube.local.
175     IN      PTR     worker2.kube.local.
176     IN      PTR     worker3.kube.local.
177     IN      PTR     db1.kube.local.

180     IN      PTR     metallb.kube.local.
189     IN      PTR     kubeapi.kube.local.
```
---------------------------
##### test DNS 
##### По умолчанию, сервер Bind под CentOS хранит логи в файле /var/named/data/named.run.
##### Для его непрерывного просмотра вводим следующую команду:
```
tail -f /var/named/data/named.run

nslookup master.kube.local 127.0.0.1
nslookup master.kube.local 192.168.1.170

nslookup master 127.0.0.1
nslookup master 192.168.1.170

dig master.kube.local @192.168.1.170
```
---------------------------
## NFS сервер

##### Сервер раздаёт по сети директорию `/var/nfs-disk`.
##### Конфигурационный файл `/etc/exports`:

```
/var/nfs-disk 192.168.218.0/24(rw,sync,no_subtree_check,no_root_squash,no_all_squash,insecure)
```

### Рабочая станция UBUNTU

\etc\hosts

```
192.168.1.170 master.kube.local
192.168.1.171 control1.kube.local
192.168.1.172 control2.kube.local
192.168.1.173 control3.kube.local
192.168.1.174 worker1.kube.local
192.168.1.175 worker2.kube.local
192.168.1.176 worker3.kube.local
192.168.1.177 db1.kube.local
192.168.1.180 metallb.kube.local
192.168.1.189 kubeapi.kube.local
```

###### В Ubuntu установлен ansible: 192.168.1.169

```
sudo apt install python3.10-venv
sudo apt install python3-pip
python3 -m pip install ansible
```

### Ansible можно ставить в venv.

```
apt install python3.10-venv
python3 -m venv venv
. ~/venv/bin/activate
python3 -m pip install ansible
```

### Все файлы проекта будут находиться в домашней директории пользователя в Ubuntu.