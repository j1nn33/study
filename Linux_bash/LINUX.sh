man – помощь
info – тоже помощь
uptime  - время с последнего включения
lscpu – данные процессора
whatis – показывает что делает комманда
whereis – показывает где файл
locate – показывает где файл
ls   - показать что в этой директории   ls -l
ls –la –R  /    - показать все на компутере
Ctrl+Z  - отправить процесс на background
Ctrl+C – прекратить процесс вообще

ln   - создать дубликат файла 
ln –s   - создать symbolic линк на файл или директорию типа Shortcut

find  - найти файл
wc  - вывести количество строк, слов, байт
cut – вывести определенное поле из текста
sort – вывести отсортированный текст
------------------------------------------------------------------
grep  - поиск определонного слова в файле            и вывод строк с этим словом
grep pattern file.txt

-i  	Case insensative
-v 	 	Shows lines not containing pattern


grep linuxacademy filename 		 Search for linuxacademy in filename
grep "^linuxacademy" filename 	 Search for lines starting with linuxacademy
grep "linuxacademy$" filename 	 Search for lines ending with linuxacademy
grep "^[abd]" filename 			 Search for characters not contained in brackets
grep [lL]inuxacademy filename 	 Search for pattern starting with either capital or lowercase L
grep "^$" filename 				 Search for empty lines
grep -v ^# filename 			 Search for uncommented lines

Регулярные Выражения:

[A-Z]*  - любое слово из больших букв
[0-9]*   - сколько угодно подряд стоящих цифр    
[A-Za-z]*@[A-Za-z]*.com   – простое выражение емайлов с окончанием .com
www\.[a-z]*\.com  - любой вэб адресс  с окончанием .com
-----------------------------------------------------------------

tar cf  mytar.tar  Folder1   - заархивировать Folder1
tar xf mytar.tar  			 - разархивировать архив
gzip     / bzip2     / xz    – скомпрессировать файл
gunzip /  bunzip2 / unxz     – раскомпресировать файл

tar cvzf myBZIP2.bz2  Folder1    - сжать Folder1
tar xvf  myBZIP2.bz2             - распаковать архив
tar tf myBZIP2.bz2        		 - посмотреть что внутри архива

zip –r myZIP.zip Folder1 		 - Запаковать Folder1 в ZIP
unzip myZIP.zip                  - Распаковать файл myZIP.

-----------------------------------------------------------------

chown – изменить владельца файла / директории
chgrp – изменить группу файла / директории
chmod – изменить права доступа на файл / директорию

chmod  ugo+x  myfile.txt   довавить X всем
chmod  g-rw   myfile.txt   убрать RW у группы
chmod  o=rw   myfile.txt   установить RW всем остальным
 u = user
 g = group
 o = other
 a = ugo


chmod  777   myfile.txt   установить RWX всем
chmod  741   myfile.txt  установить:   RWX   владельцу, R - -    группе,  - - X   всем остальным
r = 4
w = 2
x = 1

chmod 1777 myDir    включить StickyBit
chmod 0777 myDir    выключить StickyBit
-------------------------------------------------------------------
wget    - скачать файл из интернета

Ubuntu/Debian/Kali/Mint Linux:
~~~~~~~~~~~~~~~~~~~~~
apt-get install     - скачать и установить программу
apt-get remove   - удалить программу
dpkg –i                - установить программу из файла .deb
dpkg –r                - удалить программу

RedHat/CenOS Linux:
~~~~~~~~~~~~~~
yum install          - скачать и установить программу
yum remove         - удалить программу
rpm –i                  - установить программу из файла .rpm
rpm –e                 - удалить программу
-------------------------------------------------------------------
Archive and Compress

tar • Archive files; does not handle compression
»» -c • Create new archive
»» -t • List contents of archive
»» -x • Extract files from archive
»» -z • Compress or uncompress file in gzip
»» -v • Verbose
»» -j • Compress or uncompress file in bzip2
»» -f • Read archive from or to file
»» Examples

-- tar -cf helloworld.tar hello world 		• Archive hello and world files into helloworld.tar 
											  archive
-- tar -tvf helloworld.tar 					• List all files in helloworld.tar archive
-- tar -xf helloworld.tar 					• Extract files in archive
-- tar -czvf helloworld.tar.gz hello world 	• Archive and compress (using gzip) hello and world
											  files into helloworld.tar.gz archive
-- tar -zxvf helloworld.tar.gz 				• Uncompress (in gzip) and extract files from
											  archive

gzip • Compression utility used to reduce file sized; files are unavailable until unpacked;
generally used with tar
»» -d • Decompress files
»» -l • List compression information
»» Examples:
-- gzip file1 							• Compress file1 into file1.gz
-- gzip -d file1.gz    					• Unpack file1
-- gunzip filename 						• Unpack filename

• star • Archiving utility generally used to archive large sets of data; includes pattern-matching
and searching
»» -c • Create archive file
»» -v • Verbose output
»» -n • Show results of running command, without executing the actions
»» -t • List contents of file
»» -x • Extract file
»» --diff • Show difference between files
»» -C • Change to specified directory
»» -f • Specify file name
»» Examples”
-- star -c f=archive.tar file1 file2 • Archive file1 and file2 into archive.tar
archive
-- star -c -C /home/user/ -f=archive.tar file1 file2 • Move to
/home/user and archive file1 and file2 from that directory into archive.tar
-- star -x -f=archive.tar • Extract archive.tar
-- star -t -f=archive.tar • List contents of archive.tar

-------------------------------------------------------------------
fdisk -l
lsblk – просмотр информации о дисках
blkid - List available block devices on system (даже не смонтированных)
sfdisk /dev/sdb    - аналог fdisk

sda1	sda2	sdb	sdc			PV физические диски
		VG00					VG   группа томов
root	usr	home	var			LV логические диски (нарезаются поверх группы томов)
ext3	reiserfs	xfs			файловые системы



LVM Set Up
• pvcreate • Create physical volume
• pvdisplay • Show available physical volumes
• vgcreate name /dev/disks • Create volume group
• vgdisplay • Show available volume groups
• lvcreate • Create logical volume
»» -n • Volume
»» -L • Size in bytes
• lvremove /dev/vg/volume • Remove volume
• pvremove /dev/disk • Remove physical volume
-------------------------------------------------------------------


