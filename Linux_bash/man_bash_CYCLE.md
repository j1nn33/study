BASH

####  Циклы


#### -----------------------------------

##### Циклы
```bash

i=0
while (( i < 1000 ))
do
   echo $i
   let i++
done

#####

while ls | grep -q pdf
do
   echo -n 'there is a file with pdf in its name here:' 
   pwd
   cd ..
done

#####

for ((i=0; i < 100; i++))
 do
    echo $i
 done

 
 
#  Цикл for другого вида используется для перебора всех параметров, которые пере
# даются сценарию оболочки (или функции в сценарии), то есть $1, $2, $3 и.т.
 
cat args.sh
 
for ARG
do
   echo here is an argument: $ARG
done

#######

# $ ./args.sh bash is fun
# here is an argument: bash
# here is an argument: is
# here is an argument: fun 
```