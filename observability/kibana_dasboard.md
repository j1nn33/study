##### Создаине дашборда 
 - создаине визуализации 
 - создаине дашборда из визуализации


https://habr.com/ru/articles/441214/
https://habr.com/ru/articles/441264/
https://habr.com/ru/articles/441362/

 Создание дашборда Vertical bar
 ![alt text](/study/observability/IPA/image/kibana_image_1.png)

Выбираем нужный патерн индекса 
![alt text](/study/observability/IPA/image/kibana_image_2.png)

Добавьте ось X.
![alt text](/study/observability/IPA/image/kibana_image_3.png)

•	Aggregation: Terms - возвращает указанное количество топ-значений.
•	Field: clientip.keyword - выбираем клиента по IP-адресу.
•	Size: 10 - 10 топ значений.
•	- название визуализации.
![alt text](/study/observability/IPA/image/kibana_image_4.png)

Сохраняем визуализацию

![alt text](/study/observability/IPA/image/kibana_image_5.png)
![alt text](/study/observability/IPA/image/kibana_image_6.png)

Круговая визуализация
1.	Create new visualisation.
2.	Выберите Pie.
3.	Выбираем нужный патерн индекса Добавьте ось X.
4.	Чтобы данные отображались секторам, выберите Add bucket / Split slices.
![alt text](/study/observability/IPA/image/kibana_image_6_1.png)
![alt text](/study/observability/IPA/image/kibana_image_7.png)
Визуализация TSVB
Позволяет построить долю от чего либо (например общее число исходящий ip и доля целевого ip)
Или анализ кодов ответа http сервера 
![alt text](/study/observability/IPA/image/kibana_image_8.png)
фильтр настраиваев в дисковери 
![alt text](/study/observability/IPA/image/kibana_image_9.png)
![alt text](/study/observability/IPA/image/kibana_image_10.png)

Настройка dashboard
![alt text](/study/observability/IPA/image/kibana_image_11.png)

Сохранение 
![alt text](/study/observability/IPA/image/kibana_image_12.png)