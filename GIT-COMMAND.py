GIT - COMMAND
    # ТЕХНОЛОГИЯ РАБОТЫ
1. синхронизировать локальное содержимое с GitHub
   git pull (синхронизация из GitHub в локальный репозиторий)
2. работа с файлами
3. добавить новые файлы git add . (добавить всу)

4. делаем commit с помощью git commit
5. закачать локальные изменения на GitHub
   git push


    # НАСТРОЙКА

$ git config --global user.name "username"
$ git config --global user.email "username.user@example.com"

$ git config --list

    # ИНИЦИАЛИЗАЦИЯ РЕПОЗИТОРИЯ

[~/git/first_repo]
$ git init
Initialized empty Git repository in /home/tooks/git/first_repo/.git/

    #ТЮНИНГ
Отображение статуса репозитория
 - переходим в домашний каталог
cd ~
git clone https://github.com/magicmonty/bash-git-prompt.git .bash-git-prompt --depth=1

добавить в конец файла ~/.bashrc

GIT_PROMPT_ONLY_IN_REPO=1
source ~/.bash-git-prompt/gitprompt.sh

exec bash


    # ПРОВЕРКА СТАТУСА

git status

.gitignore в текущем каталоге:  показывает что игнорировать

git add                      включает файл в слежку
git rm                       удалить файл из слежения
й
git commit -m "1 commit"     закоммитить изменения
git diff       q+Enter       посмотреть разницу с последнего коммита
git log                      когда были выполнены последние изменения

git pull                     синхронизация из github в локальный репозиторий
git push                     синхронизация из локального репозитория в github