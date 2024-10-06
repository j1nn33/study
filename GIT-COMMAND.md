GIT - COMMAND
### ТЕХНОЛОГИЯ РАБОТЫ
```
1. синхронизировать локальное содержимое с GitHub
   git pull (синхронизация из GitHub в локальный репозиторий)
2. работа с файлами
3. добавить новые файлы git add . (добавить всe)   git add --all

4. делаем commit с помощью git commit -m "1 commit"
5. закачать локальные изменения на GitHub
   git push
```

### НАСТРОЙКА
```
$ git config --global user.name "username"
$ git config --global user.email "username.user@example.com"

$ git config --list

Настройка git
- создаем папку и переходим в нее 
- git init
- git clone <LINK>

#gitignore
в папке делаем 
vi .gitignore


авторизация по ключам на github

ll ~/.ssh/
ssh-keygen

ll ~/.ssh/

копируем публичный ключ на гитхаб

cat ~/.ssh/id_rsa.pub
```
### ИНИЦИАЛИЗАЦИЯ РЕПОЗИТОРИЯ
```
[~/git/first_repo]
$ git init
Initialized empty Git repository in /home/tooks/git/first_repo/.git/


git status  # ПРОВЕРКА СТАТУСА

.gitignore в текущем каталоге:  показывает что игнорировать

===========================

генератор для git ignore
- все что он сгенерит можно кинуть в  git ignore
joe g python,linux,windows


git add                      включает файл в слежку
git rm                       удалить файл из слежения

git commit -m "1 commit"     закоммитить изменения
git diff       q+Enter       посмотреть разницу с последнего коммита
git log                      когда были выполнены последние изменения

git pull                     синхронизация из github в локальный репозиторий
git push                     синхронизация из локального репозитория в github
```

### Работа с git основные команды
```
git branch   				- посмотреть какие ветки есть
git branch test   			- создать ветку test

git checkout test			- перейти на ветку test
git checkout -b test		- создать и перейти на ветку test

git checkout master			-  возвратиться на главную ветку master
git merge test     			- слить test с master

git branch -d test     		- удалить ветку когда все изменения закомичены
git branch -D test			- удалить в любом случае

git log
git checkout <hash commit>	- возвратиться в коммит
git checkout master			- возвратиться обратно

git reset --hard HEAD~		- убить последний коммит
git reset --hard HEAD~3     - убить последние 3 коммита

git commit --amend          - внесениие изменений в последний коммит

Цикл работы с git

git clone <ssh-link>        - клонирование удаленного репозитория
git checkout -b test        - создание ветки этого репозитория

работа с репозиторием test

создание удаленного репозитория test для проверки и слияния
git push origin              
git push --set-upstream origin test

если все ОК
git checkout master			- возвратиться обратно
git branch -d test     		- удалить  локальную ветку когда изменеия приняты
git push origin --delete test - удалить ветку удаленно
```