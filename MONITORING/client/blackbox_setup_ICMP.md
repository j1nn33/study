### Настройка Blackbox Exporter

```
По умолчанию, Blackbox Exporter ищет конфигурационный файл с именем blackbox.yml,
в том же каталоге, что и бинарный файл.

Общая структура конфигурационного файла blackbox.yml 
```
```yaml
module:
  icmp_slurm: 
    prober: icmp
      icmp:
        preferred_ip_protocol: ip4

```
```
icmp_slurm – имя, по которому будет запускаться проверка. Это позволяет осуществить
несколько проверок одного типа, с разными настройками.

пример с использованием ipv4 и ipv6 протоколов:
```
```yaml

module:
  icmp_v4_slurm:
    prober: icmp
      icmp:
        preferred_ip_protocol: ip4
  icmp_v6_slurm:
    prober: icmp
      icmp:
        preferred_ip_protocol: ip6
```
```
prober: задает, какой протокол будет использован для проверки. 
icmp | dns | tcp | http
```
#### icmp

```
Добавляем в конфигурационный файл проверку с использованием протокола ICMP и именем icmp_slurm
Для преобразования имен в ip используется dns, без учета файла hosts
```
```bash

cat <<EOF >> /etc/blackbox_exporter/blackbox.yml
  icmp_slurm:
    prober: icmp
    timeout: 2s
    icmp:
      preferred_ip_protocol: ip4
EOF

```
```bash
systemctl restart blackbox_exporter

# Проверяем работу

curl -is "http://localhost:9115/probe?module=icmp_slurm&target=ya.ru" | grep probe_success
# # HELP probe_success Displays whether or not the probe was a success
# # TYPE probe_success gauge
# probe_success 1

```
```bash 
#список параметров для проверки по ICMP протоколу:

timeout
Default: scrape_timeout
# Время, после которого проверка будет считаться неудачной. Если значение не
# задано, используется scrape_timeout, который передал Prometheus

preferred_ip_protocol
Default: ip6
# Какой протокол используется для проверки. Допустимые значения: ip4| ip6.

source_ip_address
Default: -
# Если на сервере несколько IP адресов, можно указать, с какого ip будет проводиться проверка.

dont_fragment
Default: false
# Разрешен ли бит фрагментации пакетов. Работает только с linux и IPv4.

payload_size
Default: -
# Размер пакета, который отправляется при выполнении проверки.
```
