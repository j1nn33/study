## DNS

###### Установка 
```
dnf install net-tools
dnf install vim mc bind bind-utils
systemctl status named
systemctl enable named
vim /etc/named.conf
---
//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

options {
        listen-on port 53 { any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        forwarders { 192.168.1.1; };
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        secroots-file   "/var/named/data/named.secroots";
        recursing-file  "/var/named/data/named.recursing";
        allow-query     { any; };

        /*
         - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.
         - If you are building a RECURSIVE (caching) DNS server, you need to enable
           recursion.
         - If your recursive DNS server has a public IP address, you MUST enable access
           control to limit queries to your legitimate users. Failing to do so will
           cause your server to become part of large scale DNS amplification
           attacks. Implementing BCP38 within your network would greatly
           reduce such attack surface
        */
        recursion yes;
        dnssec-validation no;

        managed-keys-directory "/var/named/dynamic";
        geoip-directory "/usr/share/GeoIP";

        pid-file "/run/named/named.pid";
        session-keyfile "/run/named/session.key";

        /* https://fedoraproject.org/wiki/Changes/CryptoPolicy */
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
---

vim /var/named/kube.local
---
$TTL 86400
@ IN SOA kube.local. master.kube.local. (
                                                2022120100
                                                3600
                                                1800
                                                604800
                                                86400
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
---

vim /var/named/1
---
$TTL 86400
@ IN SOA kube.local. master.kube.local. (
                                            2022120100
                                            3600
                                            1800
                                            604800
                                            86400
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
---

systemctl restart named
journalctl -xeu named.service

# Проверки 
nslookup master.kube.local 192.168.1.170
# Server:         192.168.1.170
# Address:        192.168.1.170#53
# Name:   master.kube.local
# Address: 192.168.1.170

dig master.kube.local @127.0.0.1
dig master.kube.local @192.168.1.170

dig -x <ip>
dig -x <ip> +short
dig -x <hostname> +short
dig -x <hostname> +short @<DNS_server>
dig -x <ip> +short @<DNS_server>

# ;; ANSWER SECTION:
# master.kube.local.      86400   IN      A       192.168.1.170

ping control1.kube.local
ping master.kube.local
ping control1.kube.local
nslookup control1 192.168.1.170
systemctl firewalld stop
systemctl stop firewalld
systemctl disable firewalld
tail -f /var/named/data/named.run
ping ya.ru
tail -f /var/named/data/named.run
 
```

