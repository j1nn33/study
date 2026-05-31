
#######
def func1():
    pass
    return (val1, val2)

# получение сразу значений (val1, val2) из func1

USER, PASS = func1()


#######

log_level = getattr (loggint, "DEBUG")
logging.basicConfig(level=log_level)
logger = logging.getLogger()


######

import os
os.system('pwd')

######
import os
LOG_DIR = '/var/log/hive'
log_files = [f for f in os.listdir(LOG_DIR) if 'ranger_audit' in f]
######

import logging
logging.basicConfig(level=logging.INFO, filename=argv[2]+"/app.log", filemode="a",
                    format="%(asctime)s %(levelname)-6s %(message)s")

######
subprocess.run["ls", "-la"]
# код ниже не безопасен
subprocess.run("ls -la", shell=True)

# Вводимые злоумышленником команды, приводящие к необратимой утере данных
# user_input = 'some_dir && rm -rf /some/important/directory'
my_command = "ls -l " + user_input
subprocess.run(my_command, shell=True)
# Можно полностью предотвратить подобное, запретив использование строк:
# Вводимые злоумышленником команды ни к чему плохому не приводят
user_input = 'some_dir && rm -rf /some/important/directory'
subprocess.run(["ls", "-l", user_input])


#Задание времени ожидания и работа с ним
# При написании кода, который запускает довольно долго выполняющиеся процессы, желательно указывать разумное время ожидания по умолчанию. 

import logging
import subprocess
try:
    subprocess.run(["sleep", "3"], timeout=4)
except subprocess.TimeoutExpired:
    logging.exception("Sleep command timed out")