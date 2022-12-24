#!/bin/bash
# Получение даты в формате 2022-12-24 16:07:02.935 чтобы певставить в базу данный в колонку с типом данных timestamp
var_date=$(date +"%F %T.%3N")
var_cpu=$(grep 'cpu' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}')
var_ram=$(free  | grep Mem | awk '{usemem=($2-$4)} END {print usemem}')
var_swap=$(free  | grep Swap | awk '{usemem=($3)} END {print usemem}')

#echo $var_date
#echo $var_cpu
#echo $var_ram
#echo $var_swap

echo 'INSERT INTO monitoring (date, cpu, ram, swap) VALUES ('\'''$var_date\''', $var_cpu, $var_ram, $var_swap');' > /tmp/monotoring_out.txt
:# занесение строки в базу данных
psql -U tooks -d testdb -f /tmp/monotoring_out.txt

psql -U tooks -d testdb -c 'SELECT * FROM monitoring ORDER BY date DESC LIMIT 1' -o /tmp/my.html
