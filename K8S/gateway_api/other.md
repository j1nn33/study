###### Redirect HTTP to HTTPS
###### Path redirect
###### Rewrite
###### HTTP Header modifiers
###### Split traffic Canary
###### Split traffic Blue-green




###### Redirect HTTP to HTTPS
```
пример для ingres_nginx.yaml


http-https-route.yaml

curl -vLk http://testapp.web.local
```
###### Path redirect     /login to /auth
```
kubectl apply -f path-redirect.yaml

Пошлем запрос:
curl -vLk https://testapp.web.local/login

Rewrites изменяют компоненты запроса клиента перед его проксированием. 
Фильтр URL-перезаписи может изменить имя хоста и/или путь запроса.
```

###### HTTP Header Modifiers
```
модификация и|или удаление заголовков в HTTP запросах и ответах.
секция filters в HTTPRoute:
```

###### HTTP traffic splitting
```
запущено две версии приложения:
testapp-one - это текущая версия приложения.
новая версия testapp-two рядом со старым.

проверить работоспособность нового приложения, не выключая строго. 
можно использовать два типа расщепления трафика: Canary и Blue-green.

Canary
Метод Canary подразумевает, что весь трафик по умолчанию идет на основное приложение. На новое перенаправляется только трафик в заголовке которого присутствует заранее оговоренное поле.
для доступа к новому приложению в заголовок будем добавлять: app-version: new


kubectl apply -f canary.yaml

Доступ к старой версии приложения:
curl -vk https://testapp.web.local/

Доступ к новой версии приложения:
curl -vk -H "app-version: new" https://testapp.web.local/
```
###### Blue-green
```
При помощи Blue-green мы можем осуществить постепенный переход на новую версию приложения.

Например, сначала отправлять 10% трафика на новое приложение.
Через некоторое время 50%. Затем 80%. И в конце концов переключить весь трафик на новую версию.

kubectl apply -f blue-green.yaml

Посылаем запросы минимум 10-ть раз:
curl -vk https://testapp.web.local/

```