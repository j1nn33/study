работа с конфигурационными файлами

    - открытие файла
    - удаление (или пропуск) строк, которые начинаются на знак восклицания (для Cisco)
    - удаление (или пропуск) пустых строк
    - удаление символов перевода строки в конце строк
    - преобразование полученного результата в список
    
    
    
""" РЕАЛИЗАЦИЯ """
    - удаление (или пропуск) строк, которые начинаются на знак восклицания (для Cisco)

def delete_exclamation_from_cfg(in_cfg, out_cfg):
    with open(in_cfg) as in_file:
        result = in_file.readlines()
    with open(out_cfg, 'w') as out_file:
        for line in result:
            if not line.startswith('!'):
                out_file.write(line)
                

delete_exclamation_from_cfg('input.txt', 'result.txt')

"""получает файл проверяет надо ли удалять ! 
   в строке справа удаляются символы перевода строки, и
   строка добавляется в словарь result.
"""

def cfg_to_list(cfg_file, delete_exclamation):
    result = []
    with open( cfg_file ) as f:
        for line in f:
            if delete_exclamation and line.startswith('!'):
                pass
            else:
                result.append(line.rstrip())
    return result
    
cfg_to_list('r1.txt', True)

