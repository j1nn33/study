"""
Для обработки вывода команд по шаблону в разделе используется скрипт
parse_output.py. Он не привязан к конкретному шаблону и выводу: шаблон и вывод
команды будут передаваться как аргументы

$ python parse_output.py template command_output

Обработка данных по шаблону всегда выполняется одинаково. Поэтому скрипт будет
одинаковый, только шаблон и данные будут отличаться.
"""


import sys
import textfsm
from tabulate import tabulate

template = sys.argv[1]
output_file = sys.argv[2]



with open(template) as f, open(output_file) as output:
    re_table = textfsm.TextFSM(f)
    header = re_table.header
    result = re_table.ParseText(output.read())
    print(result)
    print(tabulate(result, headers=header))


# $ python parse_output.py template command_output