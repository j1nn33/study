#!/user/bin/bash

### Проверка что скрипт запущен от root

if [ $(id -u) -ne 0]: then
   echo "Need root priveleges to run script"
   exit 1
fi

# --> Install packages <--
PACKAGES="git wget curl"
yum update > /dev/null
yum install -y $PACKAGES

# --> RUN other command <--

echo "RUN cmd1"
cmd1
echo "RUN cmd2"
cmd2

echo "service is $(systemctl is-active name)"


#####
### RUN 
sudo /usr/bin/bash example.sh