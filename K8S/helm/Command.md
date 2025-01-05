##### Основные команды
```
# 
helm version

# создание 
helm create <name_chart>

# добавление репозитория
helm repo add <name_repo> <url>

# поиск по ключевому слову
helm search <word>

# установка / удаение / обновление
helm install <name_package> [flags] 
helm uninstall <name_package> [flags]
helm upgrade <relesase_name> <name_package> [flags]

# удаление релиза из кластера
helm delete <relesase_name> [--purge]

# список всех установленых релизов
helm list [flags]
helm list -A


# инфо о состоянии конкретного релиза
helm status <relesase_name> [flags]

# получение манифестов для конкретного релиза
helm get manifest <relesase_name> [flags] 

# генерация манифество без их установки в кластер
helm template <name_package> [flags]

# история релизов из кластера  
helm history <relesase_name> [flags] 

# проверка чарта
helm lint <path> [flags] 

# созадние пакета с чартом, в виде архива
helm package <name_chart> [flags]

# получение и выгрузка манифеста из регистри 
helm [pull|push] manifest <relesase_name> [flags] 

# авторизация в регстр
helm registry [login|logout]

# откат релиза 
helm rollback <relesase> <revision> [flags]

# запуск тестов в кластре 
helm test <relesase> [flags]

# установка или обнолвение одной командой (если чарта нет то установит)
helm upgrade --intall <relesase_name>
```
