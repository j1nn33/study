#!/bin/bash
chmod +x ./myscript
./myscript

. - The Current Directory
.. - The Parent Directory
../ - The parent Directory with slash (Used to navigate from the parent)
../../ - The parent of the parent Directory
~/ - The current users home directory
.hiddenfile - A file that starts with a dot is a hidden file. ( They are normally configuration files )

========================

# Ввод Вывод сообщений
echo "The current directory is:"
read -p "Prompt" VARIABLE_TO_BE_SET
# Example
#! /bin/bash
read -p "Type Your Username" USERNAME
echo -e "\n"
read -p "Type The IP Address" IPADDR
echo -e "Logging into host $IPADDR with user \"${USERNAME}\" \n"
ssh -p 22 ${IPADDR}@${USERNAME}

========================

# Declaration and Assignment
MY_VARIABLE="value"
# Calling Variables
$MY_VARIABLE
# Calling variables with text that precedes the variable
echo "${MY_VARIABLE} some text"
# Assign a command output to a variable
VARIABLE_NAME=$(command)
# or
VARIABLE_NAME=`command`
# Example
SERVER_NAME=$(hostname)

VAR_NAME=true
VAR_NAME=false

=================

# $ script.sh parameter1 parameter2 parameter3
# In the above example we have 4 parameters
$0 = "script.sh"
$1 = "parameter1"
$2 = "parameter2"
$3 = "parameter3"

=================
# Подстановка команд

mydir=`pwd`
# или
mydir=$(pwd)

=================
# Математические операции

var1=$(( 5 + 5 ))
echo $var1
var2=$(( $var1 * 2 ))
echo $var2

=================
Сравнение чисел

n1  -eq     n2   |n1 == n2 | Возвращает истинное значение, если n1 равно n2.
n1  -ge     n2   |n1 >= n2 | Возвращает истинное значение, если n1больше или равно n2.
n1  -gt     n2   |n1  > n2 | Возвращает истинное значение, если n1 больше n2.
n1  -le     n2   |n1 <= n2 | Возвращает истинное значение, если n1меньше или равно n2.
n1  -lt     n2   |n1  < n2 | Возвращает истинное значение, если n1 меньше n2.
n1  -ne     n2   |n1 != n2 | Возвращает истинное значение, если n1не равно n2.

val1=6
if [ $val1 -gt 5 ]

=================

Сравнение строк

str1 = str2     Проверяет строки на равенство, возвращает истину, если строки идентичны.
str1 != str2    Возвращает истину, если строки не идентичны.
str1 < str2     Возвращает истину, если str1меньше, чем str2.
str1 > str2     Возвращает истину, если str1больше, чем str2.
-n str1         Возвращает истину, если длина str1больше нуля.
-z str1         Возвращает истину, если длина str1равна нулю.


#!/bin/bash
user ="likegeeks"
if [$user = $USER]

=================

if [ condition ] OPERATOR [ condition ];
    then
        #commands to be ran if true
    elif [ condition ];
    then
        #commands to be ran if true
    else
        #commands to be ran if false
fi
=================
h=3
if [ $h == 2 ];
	then
	echo "OK"
else
	echo "NO"
fi
-------------------------
# если команда выполнилась то echo "It works"
if pwd     
then
echo "It works"
fi
-------------------------
user=likegeeks
if grep $user /etc/passwd
then
echo "The user $user Exists"
fi

=================

case "$VAR" in
    pattern_1 )
        # Commands to be executed
        ;;
    pattern_2 )
        # Commands to be executed
        ;;
    * )
        # Default
        ;;
esac

================

while [ condition ]
do
    #command(s)
    #increment
done

# Example
x=1
while [ $x -le 5 ]
do
    echo "Welcome $x times"
    x=$(( $x + 1 ))
done

================

for arg in [list]
do
    #command(s)
done


Циклы for в стиле C

for (i = 0; i < 10; i++)
{
printf("number is %d\n", i);
}

================

MyFunction()
{
	echo"ffff"
}

MyFunction

================