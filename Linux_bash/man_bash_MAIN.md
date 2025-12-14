BASH

#### Переменные 
#### Стандартные ввод/вывод/ошибка
#### Выполнение команд в фоновом режиме

#### ------------------

##### Переменные 
```bash
MYVAR=textforavalue
echo $MYVAR

MYVAR='here is a longer set of words'
OTHRV="either double or single quotes will work"
# Использование двойных кавычек позволит выполнять другие замены внутри строки.
firstvar=beginning
secondvr="this is just the $firstvar"
echo $secondvr

# Ввод
read MYVAR
echo "$MYVAR"
```

##### Вывод
```bash
echo "Hello World"
printf "Hello World\n"

```

##### Стандартные ввод/вывод/ошибка
```bash
# stdin —  файловый дескриптор 0
# stdout — файловый дескриптор 1
# stderr — файловый дескриптор 2

# app, читающая ввод из stdin и записывающая результаты в stdout
app < data.in > results.out
app 2> err.msgs

app < data.in >> results.out 2 >> err.msgs

# сообщения об ошибках были объединены с нормальными результатами
app < data.in >> results.out 2>>&1
# тоже самое 
app < data.in &>> results.out

app < data.in > /dev/null

# выводит результаты выполнения команды app на экран и в то же время сохраняет их
в файл results.out:
handywork < data.in | tee -a results.out
```
##### Выполнение команд в фоновом режиме
```bash

ping 192.168.10.56 > ping.log &

# получениe списка задач, которые сейчас выполняются в фоновом режиме
jobs
[1]+ Running ping 192.168.10.56 > ping.log 
# снова вывести задачу в приоритет из фонового режима
fg 1

# Для продолжения работы в фоновом режиме 
bg
```