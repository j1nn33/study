#!/bin/bash

var_date=date

#grep 'cpu' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage"%"}'
#0.51755%

var_cpu=$(grep 'cpu' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}')
var_ram=$(free  | grep Mem | awk '{usemem=($2-$4)} END {print usemem}')
var_swap=$(free  | grep Swap | awk '{usemem=($3)} END {print usemem}')

echo $var_date
echo $var_cpu
echo $var_ram
echo $var_swap
