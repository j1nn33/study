Параллельные сессии

threading
multiprocessing
concurrent.futures

-----------------------------------------
Измерение времени выполнения скрипта

time

$ time python thread_paramiko.py
# real 0m4.712s
# user 0m0.336s
# sys 0m0.064s

Нас интересует real время. В данном случае это 4.7 секунд.

datetime

from datetime import datetime
import time

start_time = datetime.now()
#Тут выполняются действия
time.sleep(5)
print(datetime.now() - start_time)


$ python test.py
# 0:00:05.004949
-----------------------------------------

Модуль threading

    фоновое выполнение каких-то задач:
            отправка почты во время ожидания ответа от пользователя
            параллельное выполнение задач, связанных со вводом/выводом
            ожидание ввода от пользователя
            чтение/запись файлов
            задачи, где присутствуют паузы:
                        например, паузы с помощью sleep
                        
пример: netmiko_function.py

Получение данных из потоков

      netmiko_threading_data.py
      
-----------------------------------------

multiprocessing
     
      netmiko_multiprocessing.py
      
-----------------------------------------

concurrent.futures
    - предоставляет высокоуровневый интерфейс для работы с процессами и потоками. 
    
Модуль предоставляет два класса:
    ThreadPoolExecutor - для работы с потоками
    ProcessPoolExecutor - для работы с процессами

    Модуль использует понятие future. 
    Future - это объект, который представляет отложенное вычисление.
    Этот объект можно запрашивать о состоянии (завершена работа или нет), 
    можно получать результаты или исключения, которые возникли в
    процессе работы, по мере возникновения.

Метод map - это самый простой вариант работы с concurrent.futures.
Пример использования функции map с ThreadPoolExecutor (файл netmiko_threads_map_final.py):
    
Для того чтобы предыдущий пример использовал процессы вместо потоков,
достаточно сменить ThreadPoolExecutor на ProcessPoolExecutor ():  


def threads_conn(function, devices, limit=2, command=''):
    with ProcessPoolExecutor(max_workers=limit) as executor:
        f_result = executor.map(function, devices, repeat(command))
    return list(f_result)
    
------------------------------------------------------------   
Метод submit и работа с futures

При использовании метода map объект future использовался внутри, но в итоге мы
получали уже готовый результат функции.
В модуле concurrent.futures есть метод submit, который позволяет запускать future, и
функция as_completed, которая ожидает как аргумент итерируемый объект с futures и
возвращает future по мере завершения. В этом случае порядок не будет соблюдаться,
как с map.
Теперь функция threads_conn выглядит немного по-другому (файл
netmiko_threads_submit.py    

-------------------------------------------------------------
Future
Чтобы посмотреть на future, в скрипт добавлены несколько строк с выводом
информации (netmiko_threads_submit_verbose.py)

-------------------------------------------------------------
-------------------------------------------------------------

Обработка исключений

netmiko_threads_submit_exception.py
netmiko_processes_submit_exception.py  - аналогичным образом и для процессов
