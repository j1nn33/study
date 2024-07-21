##          Calico
######          - video                   
######          - Режимы работы                                    
######          - calicoctl (утилита управления)
######          - Calico IPAM


#### video
```
https://www.youtube.com/watch?v=GRlMC-7qZv8&list=PLmxqUDFl0XM6wDtlCkwdjU55z_WeBgBsZ&index=4
https://www.youtube.com/watch?v=4kQB6fR5vm8&list=PLmxqUDFl0XM6wDtlCkwdjU55z_WeBgBsZ&index=5
```
#### Режимы работы  
```
Когда ноды кластера в одной сети
Direct — когда поды могут обращаться к другим подам кластера через обычные сетевые соединения без использовани различных видов тунелей (инкапсуляций пакетов).

Когда ноды кластера в разных сетях (датацентрах)
IP-in-IP — используется возможность Linux: IP in IP tunneling
VXLAN — инкапсуляция L2 в UDP пакеты. Virtual eXtensible Local Area Networking documentation
```
#### calicoctl 
```
Утилиту можно поставить непосредственно в кластер kubernetes в виде отдельного пода. Или как бинарный файл непосредственно в Linux.
calicoctl get nodes
calicoctl node status
```
#### Calico IPAM  
```
использует Calico IP pool для определения каким образом выделять IP адреса для подов в кластере.
calicoctl get ippool
calicoctl ipam show

Назначение пула IP адресов
https://www.kryukov.biz/kubernetes/set-kubernetes-teoriya/calico/
```
