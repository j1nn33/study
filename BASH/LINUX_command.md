#### Комманды  
#### search  
#### Файловая система 
#### Logs
#### DNS
#### TIPS 
#### BASH 
#### REST 
#### CERT
#### Нагрузочное тестирование  
 

#### search   
```
# найти где встречается строка в файлах каталога 
grep -ri "ca.ru" . 

# заменить строку 
vi
:%s/ca.ru/delta.ru/g

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

```
#### Logs  
```
# если файл логов большое и не вариант его убить, то можно его обнлить
echo "" > /var/log/log.txt
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