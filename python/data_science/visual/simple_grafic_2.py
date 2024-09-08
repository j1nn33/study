from matplotlib import pyplot as pit
from collections import Counter
movies = ["Энни Холл", "Бен-Гур", "Касабланка", "Ганди", "Вестсайдская история"]
num_oscars = [5, 11, 3, 8, 10]
# ширина столбцов по умолчанию 0.8, поэтому добавим 0.1 к левым
# координатам, чтобы каждый столбец был по центру интервала
#xs = [i + 0.1 for i, _ in enumerate(movies)] 
xs = [i + 0.5 for i, _ in enumerate(movies)] 
# построить столбцы с левыми Х-координатами [xs] и высотой [num_oscars]
pit.bar(xs, num_oscars)
pit.ylabel("Количество наград")
pit.title("Мои любимые фильмы")
# добавить метки на оси X с названиями фильмов в центре каждого интервала
pit.xticks([i + 0.5 for i, _ in enumerate(movies)], movies)
pit.show()
#Столбчатая диаграмма также хорошо подходит для построения гистограмм сгруппированных значений числового ряда, что позволяет наглядно исследовать характер распределения чисел в числовом ряду (рис. 3.3):
grades = [83, 95, 91, 87, 70, 0, 85, 82, 100, 67, 73, 77, 0]
decile = lambda grade: grade // 10 * 10 # Дециль (десятая часть числа)
histogram = Counter(decile(grade) for grade in grades)
pit.bar([x - 0 for x in histogram.keys()],
        histogram.values(),
        8)
# сдвинуть столбец влево на 4
# высота столбца
# ширина каждого столбца 8
pit.axis ([-5, 105, 0, 5]) # ось X от -5 до 105,
pit.grid(True)
# ось Y от 0 до 5
pit.xticks([10 * i for i in range(11)]) # метки по оси X: 0, 10,..., 100
pit.xlabel("Дециль")
pit.ylabel("Число студентов")
pit.title("Распределение оценок за экзамен № 1")
pit.show()