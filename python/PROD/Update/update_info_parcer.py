# читаем информацию из 1 файла FILE_SOURCE.txt - актукальная информация по хостам (должна обновляться)
# читаем информацию из 2 файла FILE_UPDATE_FROM_POST.txt - (файл подгоавливается на основе информации из писем)
# обрабатыаем иформацию и пишем в 3 файл FILE_OUTPUT.txt - файл содержит какие хосты, продукты, будут обновляться 
#


# Процедура чтения из файла
def read_file (file_name):
    temp_list=[]    
    try:                                          # обработка исключения на наличие файла
        with open(file_name, 'r') as f:
            for line in f:
               temp_list.append(line.rstrip())    # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('No such file')
    
    #print (temp_list)
    return temp_list


# Процедура записи в файл  

def write_file(final_list, file_name):
     
     # определяем для открытого файла переменую f
     # и выполняет набор инструкций. После их выполнения файл автоматически закрывается. 
     # Даже если при выполнении инструкций в блоке with возникнут какие-либо исключения,
     # то файл все равно закрывается.
     temp_list = final_list
     with open(file_name, 'a') as f:        # определяем для открытого файла переменую f
         line = '---------------------------------------------'
         f.write(line+'\n') 
         for line in temp_list:
             #print (line)
             #f.write(str(line)) 
             f.write(str(line)+'\n') 
             #f.write(line+'\n')             # +'\n' для переноса строк
     f.close()

# процедура обработки информации

def executor_info (file_source, file_update_from_post, file_output):
    #print(file_source)
    #print(file_update_from_post)
    #print(file_output)
    data_source = read_file (file_source) 
    #print (data_source)
    data_update = read_file (file_update_from_post)
    #print (data_update)

    # инициализация списков
    exist_host = []
    unknown_host = []
    dev_host = []

    for i in data_source:
        #print (i)
        l = i.split(' ')
        #l = l[1]
        #print ('l= ', l)
        for j in data_update:
            #print ('j = ', j)
            #print ('i=', i)
            if (l[0] in j) or (l[1] in j):
                #print (i)
                exist_host.append(str(l[2]) +' - '+ str(j.split('\t')))
                #print ('host exist', str(l[2]) +' - '+ str(j) )
                # вспомогатлеьный список
                dev_host.append(j)
            
    print('++++++++++++++++')
    print (dev_host)
    print ('----------')
    print (data_update)   
    #print (unknown_host)
    # Нахождение разности двух списков для полученя хостов которых нет 
    unknown_host=list(set(data_update)-set(dev_host))
    print ('============')
    print (unknown_host)
    
    write_file(exist_host, file_output)
    write_file(unknown_host, file_output)


if __name__ == "__main__":

    current_dir = "D:\\CODE\\STYDI\\Update\\"
    file_source = "SOURCE.txt"
    file_update_from_post = "UPDATE_POST.txt"
    file_output = "RESULT.txt" 
    
    #print ('чтение из файла  SOURCE.txt')
    #file_name = (current_dir+file_source)
    #print ('вывод пути файла который читаем', file_name)
    #read_file (current_dir+file_source)
    #print ('чтение из файла  UPDATE_FROM_POST.txt')
    print ('процедура обработки')
    executor_info (current_dir+file_source, current_dir+file_update_from_post, current_dir+file_output)   
 
    #print ('чтение из файла  OUTPUT.txt')	
    #print ('запись в файл обработанной информации')
    #final_list = ['123']
    #write_file (final_list, current_dir+file_output)