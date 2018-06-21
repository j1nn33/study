#!/bin/python3
#----------------------------
# Program  by Konstantin. B.
#
# Version	Date		
# 1.0 		2018
# Info
#----------------------------
# Скрипт Удаления Старых Файлов и Пустых Директорий
import os
import time


DAYS = 5  # MAX age of file? older will be deleted
FOLDERS = [
            "G:\Shared\dir1",
            "G:\Shared\dir2",
            "G:\Shared\dir3"
           ]
TOTAL_DELETED_SIZE = 0
TOTAL_DELETED_FILE = 0
TOTAL_DELETED_DIRS = 0

nowTime = time.time()             # current time
ageTime = nowTime - 60*60*24*DAYS # current time - DAYS

def delete_old_files (folder):
    """Delete file oder than X DAYS"""
    global TOTAL_DELETED_FILE
    global TOTAL_DELETED_SIZE
    for path, dirs, files in os.walk(folder):
        for file in files:
            fileName = os.path.join(path, file)  # get full PATH to file
            fileTime = os.path.getmtime(fileName)
            if fileTime < ageTime:
                sizeFile = os.path.getsize(fileName)
                TOTAL_DELETED_SIZE +=sizeFile
                TOTAL_DELETED_FILE +=1
                print("DELETE file: ", str(fileName))
                os.remove(fileName)

    return


def delete_empty_dir (folder):
    """Delete empty DIRS"""
    global TOTAL_DELETED_DIRS
    empty_folder_in_this_run =0
    for path, dirs, files in os.walk(folder):
        if (not dirs) and (not files):
            TOTAL_DELETED_DIRS +=1
            empty_folder_in_this_run +=1
            print ("DELETE EMPTY DIR: ", str(path))
            os.rmdir(path)
    if empty_folder_in_this_run >0:
        delete_empty_dir(folder)

    return


#==================MAIN================
stasttime = time.asctime()

for folder in FOLDERS:
    delete_old_files(folder)
    delete_empty_dir(folder)

finishtime = time.asctime()

print ("=======================")
print ("START TIME: ", str(stasttime))
print ("Total Deleted Size: ", str(int(TOTAL_DELETED_SIZE/1024/1024)), "MB")
print ("Total Deleted Empty folders: ", str(TOTAL_DELETED_DIRS))
print ("FINISH TIME: ", str(finishtime))
print ("FINISH")
print ("=======================")