## NFS
###### Установка Server
###### Со сторны клинета
###### Configure Firewall
###### установка в K8S 
###### Пример в K8S


###### Установка Server
```
yum install nfs-utils

# Используется отдельный диск на виртуальной машине 120G
# Сервер раздаёт по сети директорию /var/nfs-disk

mkdir /var/nfs-disk/
fdisk -l /dev/nvme0n2p1
mkfs.xfs /dev/nvme0n2p1
blkid
vim /etc/fstab
mount -a

lsblk
# NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
# nvme0n2                   259:3    0  120G  0 disk
# └─nvme0n2p1               259:4    0  120G  0 part /var/nfs-disk

df -h
# Filesystem                         Size  Used Avail Use% Mounted on
# /dev/nvme0n2p1                     120G  889M  120G   1% /var/nfs-disk

cat /etc/fstab
# UUID=25d9532a-XXX /var/nfs-disk     xfs     defaults        0 0

systemctl enable rpcbind nfs-server
systemctl start rpcbind nfs-server

rpcinfo -p | grep nfs
ls -la /var/nfs-disk/
chmod -R 777 /var/nfs-disk/

cat /etc/exports
# /var/nfs-disk 192.168.1.0/24(rw,sync,no_subtree_check,no_root_squash,no_all_squash,insecure)

```
###### Со сторны клинета

```
mount 192.168.1.170:/var/nfs-disk /mnt/
vi /mnt/test.txt
df -h | grep mnt
# 192.168.1.170:/var/nfs-disk  120G  889M  120G   1% /mnt
umount /mnt/

```
###### Configure Firewall
```
firewall-cmd --permanent --add-service mountd
firewall-cmd --permanent --add-service rpc-bind
firewall-cmd --permanent --add-service nfs
firewall-cmd --reload
```
###### установка в K8S 
```
kubectl apply -f nfs.yaml
```
###### Пример в K8S
```
./K8S/tasks/kryukov/pv_volumes_dynamic
```