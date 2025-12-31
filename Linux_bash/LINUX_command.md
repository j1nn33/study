#### Комманды 
#### other 
#### search  
#### cut
#### Файловая система 
#### DISK
#### RPM
#### Logs
#### DNS
#### TIPS 
#### BASH 
#### REST 
#### CERT
#### Нагрузочное тестирование  
#### АНАЛИЗ OS
#### АНАЛИЗ ППО 
#### LINUX Troubleshooting
```
LOG
RPM
NETWORK
APP
```
#### Text-Editors
#### NET
#### USER
#### Time
#### Sysctl
#### Python 

 
####
```
ssh user@ip
ssh -i /id_rsa user@ip

scp /source_dir/ user@ip:/destination_dir

chattr -i /file


swappoff -a
# как память вернется 
swapon -a
```

#### other
```
ssh user@ip
scp <path_source> user@ip:<path_tagert>

systemctl -a | grep fail

systemctl start\stop\restart <service_name>
systemctl list-units | grep graf

systemctl show graf*


#### Передача данных

scp some_system.tar.gz bob@10.0.0.45:/home/bob/some_system.tar.gz

```
#### search   
```

grep "^[^#*/;]" <name_config>

grep -i error /var/log/message

find /opt/dir -name *name* -type f 

# найти где встречается строка в файлах каталога 
grep -ri "ca.ru" . 

# заменить строку 
vi
:%s/ca.ru/delta.ru/g

#### Поиск по имени файла
find /home -iname '*password*'

find /home -size +5G | sort -n -r | head -5

#### Поиск контента (файлов которые содержат password)

grep -i -r /home -e 'password'


```
#### cut   
```
cat cutfile.txt

#12/05/2017 192.168.10.14 test.html
#12/30/2017 192.168.10.185 login.html

$ cut -d' ' -f2 cutfile.txt
# 192.168.10.14
# 192.168.10.185
Параметр -d' ' указывает, что в качестве разделителя полей используется пробел  
Параметр -f2 определяет, что команде нужно вырезать и отобразить второе поле, в данном случае IP-адреса.

```

#### Файловая система   
```
tree -L 1 /

# размер файлов 
du -sh *
# размер текщей папки / конкретной папки
du -sh .
du -sh /etc
# размеры разделов
df -h

du -h /tmp | grep M

```
#### DISK
```
sda1	sda2	sdb	sdc  |  	PV физические диски
		VG00	 		 |	VG   группа томов
root	usr	home	var	 |	LV логические диски (нарезаются поверх группы томов)
ext3	reiserfs	xfs	 |	файловые системы
-----------------------------------------------------

lsblk 				– просмотр информации о дисках
sfdisk /dev/sdb    	- аналог fdisk

du -ha --time /etc/
du -sh /home/mial/
df -x tmpfs -h
df -k /tmp
iotop

du -d l -h /var/log/*
du -sh /var/log/*

vgs

# добавляет пространство +10G
lvextend -r -L +10G /dev/mapper/rootvg-lvroot

# расширяет до 10G
lvextend -r -L10G /dev/mapper/rootvg-lvroot

# Анализ дисковой подсистемы
# Определение программ, производящих запись на накопитель
iotop -obPat

# Определение файлов, в которые производится запись
fatrace -f W
```

#### RPM
```
yum update -y 
yum -y install epel-release
yum install <name>
yum remove  <name>
yum -y install epel-release

yum install <name_pack> --enablerepo=<name_repo>
yum clean all
yum update
yum update --disablerepo=* --enablerepo=<name_repo>
yum search

rm -f /var/lib/rpm/__db*
db_verify /var/lib/rpm/Packages
rpm --rebuild
yum clean all
```

#### Logs  
```
# если файл логов большое и не вариант его убить, то можно его обнлить
echo "" > /var/log/log.txt

/var/log/------

grep CentOS /var/log/messages
grep 'CentOS Stream' /var/log/messages
cat /var/log/dpkg.log.1 | grep status | grep curl
grep installed.python[23][.] /var/log/messages
egrep '^[^#]' /etc/passwd
grep -R <name> /etc/config

find /etc/ -type f -size +40k
grep -A 10 -B 10
find /var -mount -type f -ls 2>/dev/null | sort -rnk7 | head -10
```
#### DNS   
```
# Тестирование DNS

dig -x <ip>
dig -x <ip> +short
dig -x <hostname> +short
dig -x <hostname> +short @<DNS_server>
dig -x <ip> +short @<DNS_server>
```
#### TIPS  
```
dos2unix <file_name>    - заменить \n\r

$ cat <<EOF > file.txt
line1
line2
EOF

$$     - pid последней команды
$?     - exitcode последней команды (0 - ok)
$#     - кол-во аргументов переданных в скрипт 
$0     - имя скрипта
-$*    - все аргументы commandline ($1 $2)

```
#### BASH 
```
command1; command2                 - выполнить команды последовательно
command1 && command2               - command2 выполнится только после успешного выполнения command1
command1 || command2               - command2 выполнится только после не успешного выполнения command1
command1 && command2 || command3   - комбинация           curl <--> && echo 'ok' || echo 'error'
command1 | command2                - вывод command1 на вход command2
command1 > file                    - записать stdout в file
command1 2 > file                  - записать errout в file
command1 > file 2>&1               - записать stdout и errout в file
command < file                     - получить на вход command данные из file

set 
   -x           - вывод всех аргументов команды по мере ее выполнения
   -e           - немедленный выход при завершении команды с ненулевым статусом
   -o pipefail  - убедиться,что все комады в пайпах завершились успешно

диапазоны 

mkdir -p /opt/users/name{user1,user2,user3}/{doc,download,project{0..9}}

tree -L 1 /opt/users/
/opt/users/
├── nameuser1
├── nameuser2
└── nameuser3

# tree -L 2 /opt/users/
/opt/users/
├── nameuser1
│   ├── doc
│   ├── download
│   ├── project0
│   ├── project1



```
#### REST   
```
URI = URL + URN
URL - адрес ресурса в сети и способ обращения к нему
URN - имя ресурса в сети (только его название), не не как подключиться к нему

curl -k -x POST https://-------- \
     -H "Content-Type: application/json" \
     -d "{\"fields:......}"
```
#### CERT
```
Посмотреть сертификат на удаленном ресурсе
openssl s_client -connect host:443 -showcert
```
#### Нагрузочное тестирование  
```
# Эмуляция задержки на сетевой интерфейс
sudo tc qdisc add dev ens192 root netem delay 100ms 250ms 25%
sleep 600
sudo tc qdisc del dev ens192 root netem 

# Установка лимитов на свободные дискрипторы файлов

# Сохранеиение действующих лимитов
echo "# Increase limit for file descriptor utilization attack" > /etc/security/limits.d/30-chaosteam-nofile.conf';
# Установка лимитов 
echo "# chaostem hard nofile 150000\" > /etc/security/limits.d/30-chaosteam-nofile.conf';
echo "# chaostem soft nofile 150000\" > /etc/security/limits.d/30-chaosteam-nofile.conf';
# Перелогин
logout
# Исчерпание установленых лимитов
FILE_MAX=$(cat /proc/sys/fs/file-max);
echo $FILE_MAX > file_max.conf;
# Сохранение этого состояния на 10 мин
sudo sysctl -w fs.file-max=10000 && $HOME/utils/filedescrutilize --file 150 -time 600;
# Освобождение дескрипторов, востановление прежних значений 
sudo sysctl -w fs.file-max=$FILE_MAX
```

#### АНАЛИЗ OS
```
- анализ состояния ОС
	- systemctl
	- анализ логов (где\какие)
	- htop
	- ps
	- netstat
	- df, du

top
i - то что жрет проц

lsof /var | grep "/var/log/" | grep deleted

--------------------------------
du -d l -h /var/log | sort
du -d l -h /var/log | sort -nr | head -10


du -sh /dir/

du -mbh | sort -nr | head -10
du -a | sort -nr | head -10

```

#### АНАЛИЗ ППО
```
which <name_app>
locate <file_name>

rpm -qa | grep <name_app>
rpm -qf  /etc/pam.d

dpkg-query -S 
```
#### LINUX Troubleshooting

###### LOG
```bash
journalctl
journalctl /dev/vda
journalctl -b _SYSTEMD_UNIT=httpd.service
journalctl -b _SYSTEMD_UNIT=httpd.service _PID=5874

journalctl --list-boots
```
###### RPM
```bash
yum install -v <name_package>
yum deplist <name_package>
rpm -q --requires <name_package>
# Listing All Versions of a Package
yum list --showduplicates <name_package>

yum history
yum history info 7
yum history undo 7
yum history redo 7


# Решение проблемы 
# (try to add '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)

yum -v install <name_package>
yum deplist <name_package>
yum list --showduplicates <name_package>

yum versionlock
yum versionlock delete <name_package_version>
yum versionlock
yum install  <name_package>

yum update <name_package>
# (try to add '--skip-broken' to skip uninstallable packages or '--nobest' to use not only best candidate packages)
yum versionlock add <name_package>
yum versionlock

 ```
 ###### Network
 ```bash
nmcli connection show
nmcli connection show "Wired connection 1"
nmcli device

ip route

ncat mailserver 25

# monitoting traffic
iptraf-ng  
 
 ```
  
  ###### Applications
 ```bash
 
# displaying shared library information

objdump -p /usr/lib64/libpthread-2.28.so | grep SONAME

# run application
application
echo $?

which application
# /usr/bin/application

# displays all of the shared libraries that an application uses
ldd /usr/bin/application

# yum provides command identifies the package that provides the specified shared library.

yum provides '*/lib/name'

yum install 'Provide'

yum reinstall APP --downloadonly --destdir /home/user/
``` 
#### Text-Editors
```
NANO
---------------------------------------
Выделение				|	Alt-A    + стрелочка
скопировать в буффер	|	Ctrl-K
вставить текст			|	Ctrl-U

---------------------------------------
VI

вернуться в командный режим		| esc
вернуться/войти в режим ввода	| a i
выход без изменений				| :q!
сохранить и выйти				| :wq
удаление текущей строки   		| dd
создание копии текущей строки	| yy
вставить						| p

---------------------------------------
MC
SHIFT + F4		Создает новый файл.
ALT + ENTER		Вставить файл или каталог, на котором установлен курсор в командную строку.
CTRL + F  		Копировать выделенный текст в файл.
SHIFT + F5 		Вставка текста из файла.

```

#### NET 
```
nmtui

/etc/sysconfig/network-scripts/ifcfg-eth0
/etc/init.d/network restart
/etc/resolv.conf
/etc/hostname 
/etc/hosts

service network restart

ip addr show
ip a
netstat - tulpen | grep sshd
iftop   nload    -  мониторинг сетевых интерфейсов
ip route
ping  10.0.0.1 -s 1500
locate file_name


#### проверить доступность порта 

nc -zv <ip> <port>

```

#### USER
```
- работа с локальными УЗ\группами  /etc/sudores

useradd

usermod -aG <group1, group2> <user>   - накинуть групп
usermod -G <group1, group2> <user>    - грохнуть групп

groups <user>  - список групп

visudo
/etc/sudoers

root    ALL=(ALL:ALL)       ALL
<user>  host=(<от каких пользователей: от каких групп>)     какие команды

%wheel ALL=(root)NOPASSWD: /bin/mount, /bin/umount
sudo -l
```

#### TIME
```
- ntp chrony (настройка проверка)
systemctl restart ntpdate
systemctl restart chronyd

/etc/ntp.conf
/etc/chrony.conf
ntpq -p
ntpq -q
```
#### Sysctl
```

sysctl -a

sysctl -w parametr=value 
echo "net.ipv4.tcp_synack_retries = 5" >> /etc/sysctl.conf
```
#### Python 
```
python3 -m pip install -r requirements.txt

pip install -U pip
pip install <name>
pip search 

yum install pyhton36
alternatives --config python

```
#### IPTABLES
```
iptables -L
iptables -L --line-numbers -n -v

ipatables -D INPUT 10
ipatables -I INPUT -s 111.222.333.4444/32 -j DROP

```