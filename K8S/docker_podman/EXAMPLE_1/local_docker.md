###### LOCAL TO DOKER
```
Flask приложение выводящее Hello, World! (from a Docker container)

-  app/
     |
     |-- app.py
     |-- requirements.txt
     |-- Dockerfile



cat app.py
```python
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, World! from a Docker container'
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```	
```	
cat requirements.txt
Flask==3.0.0
gunicorn==22.0.0

cat Dockerfile
# 1. Используем официальный образ Python как основу
FROM python:3.11-slim
# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app
# 3. Копируем файл с зависимостями и устанавливаем их (используем кэш)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# 4. Копируем весь остальной код приложения
COPY . .
# 5. "Сообщаем" Docker, что наше приложение будет работать на порту 5000
EXPOSE 5000
# 6. Указываем команду, которая запустится при старте контейнера
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

```
Сборка образа 
. (точка в конце): Это очень важная часть. Точка указывает на контекст сборки. Она говорит Docker: "Ищи Dockerfile в текущей директории (.) и отсюда же бери все файлы для копирования в образ (например, app.py и requirements.txt)".
```
cd ./app/
docker build -t flask_web_hello-world-docker .

docker run --rm -d -v `pwd`:/app -p 5000:5000 flask_web_hello-world-docker
docker run --rm -d -v `pwd`:/app -p 5000:5000 --name flask_web flask_web_hello-world-docker

```
-d:  запускает контейнер в фоновом режиме.
-p 5000:5000: привязывает первый (локальный) из указанных портов (5000) ко второму порту (5000) внутри контейнера.
--name flask_web  (останавливать, смотреть логи и т.д.).
  flask_web_hello-world-docker  имя образа,

```
docker ps -a
docker logs flask_web
http://192.168.1.175:5000/



# исмениения в коде app.py (чтобы применились )

docker stop <CONTAINER ID>
docker start <CONTAINER ID>

  2 docker stop flask_web_hello-world-docker



