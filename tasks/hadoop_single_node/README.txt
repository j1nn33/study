Установка hadoop на одну ноду
План
	Pre-Installation Steps:
1. Linux Operating System should be Install  1/2/30
2. Java Should be Install (Recommended is Java 8 or Later)
3. Password Less SSH Should be Setup

	Installation Steps:
Hadoop 3.x 
    HDFS: 
	   - NameNode, DataNode, SecondaryNamenode
	Post-Installations:
	   - JobTracker, ResourceManager, TaskTracker NodeManager
1. core-site.xml
2. hdfs-site.xml
3. mapred-site.xml
4. yarn-site.xml

--------------------






---------------------------
# Для быстрого тестирования 
# inventory.ini
# ansible.cfg

Запускать 
~./repo/study/ROLES/hadoop_single_node
без ключа
ansible all -i hosts.ini -m ping -k 
с ключем
ansible.cfg   private_key_file = ~/.ssh/id_rsa
ssh-copy-id username@remote_host
ansible all -i hosts.ini -m ping -k
ansible all -i hosts.ini -m shell -a 'ps -ef | grep java'
ansible all -i hosts.ini -m command -a 'systemctl status chronyd.service'

# как запустить
ansible-playbook ./prepare_task.yml -i ./hosts.ini -k 

