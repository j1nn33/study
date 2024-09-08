диски
===========================================
lsblk – просмотр информации о дисках
sfdisk /dev/sdb    - аналог fdisk

sda1	sda2	sdb	sdc			|PV физические диски
VG00					 		|VG   группа томов
root	usr	home	var			|LV логические диски (нарезаются поверх группы томов)
ext3	reiserfs		xfs		|файловые системы

===========================================
2.  Настройка сети
	
утилиты	Nmtui	
	
/etc/sysconfig/network-scripts/ifcfg-eth0
/etc/init.d/network restart
service network restart	

dns - 	etc/resolv.conf	
Proxy		
Hostname	# hostnamectl set-hostname vsrv1

/etc/hostname 
freeipa.contosol.com

/etc/hosts
127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4
::1 localhost localhost.localdomain localhost6 localhost6.localdomain6
192.168.10.20 freeipa.contoso.com freeipa	


мониторинг	ip addr show
ip a	
======================================================
3. Обновление и добавление репозиториев и установка пакетов
	REHEL	Debian
Обновление	
yum update -y 
yum -y update && reboot	
sudo apt-get update
sudo apt-get upgrade

Добавление репозитория
yum -y install epel-release

Установка пакета	
yum install	sudo apt-get install nmap

Удаление пакета	
yum remove	sudo apt-get remove nmap
		
======================================================
Отключение selinux	
vi /etc/selinux/config	
======================================================
yum -y install epel-release
rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm
yum –y update
======================================================
4. Рабочий минимум пакетов
yum -y install mc vim ntp ssh
======================================================
5. Установка и настройка сервисов
	REHEL	Debian
Управление сервисами	
service <service>  start stop restart 

yum -y install openssh-server
systemctl enable sshd
systemctl start sshd	
======================================================
Права на папку и подкаталоги	chmod -R 755 /home/qwerty	
Владелец на папку и подкаталоги	chown -R user:group /home/user/dir/	
======================================================
Необходимые сервисы
# yum install -y ntp
Настройка почты
# yum install -y mailx
/etc/postfix/main.cf   нужно поменять на свой домен:
mydomain = example.com
# systemctl restart postfix
В /etc/aliases добавляем алиас от root на свой почтовый ящик и обновляем базу алиасов:
newaliases
Проверяем. После следующей команды должно прийти пустое письмо на ящик из алиасов:
# echo | mail root
======================================================
6. Настройка безопасности (firewall, selinux, sudo)
firewall-cmd --permanent --add-port={80/tcp,443/tcp,389/udp,53/udp,123/udp}
firewall-cmd --reload

Перенаправить входящие на 22 порт на другой хост:
# firewall-cmd --zone=external --add-forward-port=port=22:proto=tcp:toaddr=192.168.1.23
firewall-cmd --permanent --zone=public --add-service={ntp,http,https,ldap,ldaps,kerberos,kpasswd,dns}
firewall-cmd –reload
firewall-cmd --list-all --zone=public

systemctl disable firewalld
systemctl stop firewalld

# close all incoming ports
$ sudo ufw default deny incoming
# open all outgoing ports
$ sudo ufw default allow outgoing
# open ssh port
$ sudo ufw allow 2201/tcp
# open http port
$ sudo ufw allow 80/tcp
# open ntp port : to sync the clock of your machine
$ sudo ufw allow 123/udp
# turn on firewall
$ sudo ufw enable

======================================================
7. Мониторинг и логи
СИСТЕМА
top –> pid (находим) -> ps -> log (-> lsof -p 1234 (где 1234 – id  процесса))
Ps –ef|grep 1234    1234 – id процесса  (алгоритм    top –> pid -> ps)
-------------------------------------------
Ps –ax	Список сервисов
vmstat
Free –h
Iotop – для диска
Sysstat – набор утилилт
-------------------------------------------
СЕТЬ
Ping  	-> 	iptables  –L	 ->	 telnet 192.168.10.1 53	 -> netstat –tulpen	 -> log 
mtr [hostname]	Круче ping
netstat -ntlup | grep sshd

iftop   nload    -  мониторинг сетевых интерфейсов
-------------------------------------------
yum install bind-utils           днс записи
dig +short ipa.example.org A.
dig +short -x your_server_ipv4

Утилита cbm позволяет увидеть сетевой трафик в реальном времени:
apt-get install cbm
cbm


СЕРВИСЫ

ДИСКИ
df -h 
apt-get install iotop
iotop
Приблизительные значения IOPS для жестких дисков.
7,200 об/мин SATA-диски	~75-100 IOPS	SATA 3 Гбит/с
10,000 об/мин SATA-диски	~125-150 IOPS	SATA 3 Гбит/с
10,000 об/мин SAS-диски	~140 IOPS	SAS
15,000 об/мин SAS-диски	~175-210 IOPS	SAS
Приблизительные значения IOPS для SSD.
IOPS	Интерфейс
~8 600 IOPS	SATA 3 Гбит/с
~60 000 IOPS (Произвольная запись 4K)	SATA 6 Гбит/с
~200 000 IOPS (Произвольная запись 4K)	PCIe
~1 400 000 IOPS	PCIe


ЛОГИ
Чтение лог-файлов в режиме реального времени
tail -f path_to_log | grep search_term

