#!/bin/python3
#----------------------------
# Program  by Konstantin. B.
#
# Version	Date		
# 1.0 		2018
# Info
# чистит логи и складывает старую информацию в др лог файлы
# purgelog.py mylog.txt 10 5
# mylog.txt
# 10 максимальный размер лог файла kb
# 5 количество лог файлов
# mylog.txt > mylog.txt_1
# mylog.txt_1 > mylog.txt_2 max 5
#----------------------------

import shutil    # For Copyfile
import os        # For GetFileSize and Check if File exist
import sys       # For CLI Arguments


# control correct start script
if(len(sys.argv) <4):
    print ("Missing arguments! : purgelog.py mylog.txt 10 5")
    exit(1)

file_name = sys.argv[1]
limitsize = int(sys.argv[2])
logsnumber = int(sys.argv[3])

if(os.path.isfile(file_name) == True):          # Check if MAIN log is exist
    logfile_size = os.stat(file_name).st_size   # Check File size in BYTES
    logfile_size = logfile_size /1024           # Convert BYTES to KiloBYTES

    if(logfile_size >= limitsize):
        if(logsnumber >0):
            for currentFileNum in range(logsnumber, 1, -1):
                src = file_name + "_" + str(currentFileNum-1)
                dst = file_name + "_" + str(currentFileNum)
                if(os.path.isfile(src) == True):
                    shutil.copy(src, dst)
                    print ("Copied: ", src , " to ", dst)

            shutil.copy(file_name,file_name + "_1")
            print("Copied: ",file_name," to ",file_name,"_1")
        # Clear MAIN File
        myfile = open(file_name,'w')
        myfile.close()