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