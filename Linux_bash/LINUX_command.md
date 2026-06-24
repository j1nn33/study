#### Комманды 
#### scp rsyns
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
```bash
ssh user@ip
ssh -i /id_rsa user@ip

scp /source_dir/ user@ip:/destination_dir

chattr -i /file


swappoff -a
# как память вернется 
swapon -a
```
# scp rsyns
```bash 
# Скопировать файл на удаленный хост
scp file.txt user@host:/path/
# Скопировать с удаленного хоста
scp user@host:/path/file.txt ./
# Синхронизировать каталоги
rsync -avz localdir/ user@host:/remotedir/
# Rsync с прогрессом
rsync -avz --progress src/ dest/
```
#### other
```bash
ssh user@ip
scp <path_source> user@ip:<path_tagert>

systemctl -a | grep fail

systemctl start\stop\restart <service_name>
systemctl list-units | grep graf

systemctl show graf*


#### Передача данных

scp some_system.tar.gz bob@10.0.0.45:/home/bob/some_system.tar.gz

# Создать архив tar
tar -cf archive.tar files/
# Создать сжатый архив
tar -czf archive.tar.gz files/
# Извлечь архив
tar -xf archive.tar
# Извлечь сжатый архив
tar -xzf archive.tar.gz
# Листинг содержимого архива
tar -tf archive.tar


# Сжать файл с помощью gzip
gzip filename
# Распаковать файл gzip
gunzip filename.gz
# Создать zip архив
zip archive.zip file1 file2
# Извлечь zip архив
unzip archive.zip
# Листинг содержимого zip
unzip -l archive.zip

# Создать архив со сжатием
tar -czvf backup.tar.gz /home/user/
# Извлечь в указанный каталог
tar -xzf archive.tar.gz -C /destination/
# Добавить файлы в существующий архив
tar -rf archive.tar newfile.txt
# Обновить архив более новыми файлами
tar -uf archive.tar files/


```
#### search   
```bash

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


# Поиск шаблона в файле
grep "pattern" filename
# Поиск без учета регистра
grep -i "pattern" filename
# Рекурсивный поиск в каталогах
grep -r "pattern" /path/
# Показать номера строк
grep -n "pattern" filename
# Посчитать совпадающие строки
grep -c "pattern" filename

# Заменить текст в файле
sed 's/old/new/g' filename
# Удалить строки, содержащие шаблон
sed '/pattern/d' filename
# Вывести указанные поля
awk '{print $1, $3}' filename
# Суммировать значения в столбце
awk '{sum += $1} END {print sum}' filename

# Сортировать содержимое файла
sort filename
# Числовая сортировка
sort -n numbers.txt
# Удалить повторяющиеся строки
uniq filename
# Сортировать и удалить дубликаты
sort filename | uniq
# Подсчет строк, слов, символов
wc filename
# Подсчет только строк
wc -l filename

```
#### cut   
```bash

# Извлечь первый столбец
cut -d',' -f1 file.csv
# Извлечь диапазон символов
cut -c1-10 filename
# Объединить файлы бок о бок
paste file1.txt file2.txt
# Использовать пользовательский разделитель
cut -d':' -f1,3 /etc/passwd

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
```bash
tree -L 1 /

# размер файлов 
du -sh *
# размер текщей папки / конкретной папки
du -sh .
du -sh /etc
# размеры разделов
df -h

du -h /tmp | grep M


# Показать размеры каталогов
du -h /path/
# Сводка общего размера
du -sh /path/
# Показать размеры всех подкаталогов
du -h --max-depth=1 /path/
# Сначала самые большие каталоги
du -h | sort -hr | head -10



```
#### DISK
```bash
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
```bash
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
```bash
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
```bash
# Тестирование DNS

dig -x <ip>
dig -x <ip> +short
dig -x <hostname> +short
dig -x <hostname> +short @<DNS_server>
dig -x <ip> +short @<DNS_server>
```
#### TIPS  
```bash
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
```bash
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
```bash
URI = URL + URN
URL - адрес ресурса в сети и способ обращения к нему
URN - имя ресурса в сети (только его название), не не как подключиться к нему

curl -k -x POST https://-------- \
     -H "Content-Type: application/json" \
     -d "{\"fields:......}"
```
#### CERT
```bash
Посмотреть сертификат на удаленном ресурсе
openssl s_client -connect host:443 -showcert
```
#### Нагрузочное тестирование  
```bash
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

# Следующая команда выполняет по 100 запросов, всего 10 000, к локальной машине, на которой запущен Nginx:

ab -c 100 -n 10000 http://localhost/
```

```bash
while true; do \
   curl -i http://$EXTERNAL_IP/sentiment \
   -H "Content-type: application/json" \
   -d '{"sentence": "I love yogobella"}' \
   --silent -w "Time: %{time_total}s \t Status: %{http_code}\n" \
   -o /dev/null; sleep .1; done
# Time: 0.153075s Status: 200
# Time: 0.137581s Status: 200
# Time: 0.139345s Status: 200
# Time: 30.291806s Status: 500

```

#### АНАЛИЗ OS
```bash
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
```bash
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
```bash
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
```bash
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
```bash
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
```bash
- ntp chrony (настройка проверка)
systemctl restart ntpdate
systemctl restart chronyd

/etc/ntp.conf
/etc/chrony.conf
ntpq -p
ntpq -q
```
#### Sysctl
```bash

sysctl -a

sysctl -w parametr=value 
echo "net.ipv4.tcp_synack_retries = 5" >> /etc/sysctl.conf
```
#### Python 
```bash
python3 -m pip install -r requirements.txt

pip install -U pip
pip install <name>
pip search 

yum install pyhton36
alternatives --config python

```
#### IPTABLES
```bash
iptables -L
iptables -L --line-numbers -n -v

ipatables -D INPUT 10
ipatables -I INPUT -s 111.222.333.4444/32 -j DROP

```