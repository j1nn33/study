
# пример многословного выражения
long_winded_computation = (1+2+3+4+5+6+7+8+9+10+
                           11 + 12 + 13 + 14 + 15 + 16 + 17 + 18 + 19 + 20)


# СПИСОК СПИСКОВ
list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# такой список списков легче читается
easier_to_read_list_of_lists = [ [1, 2, 3],
                                 [4, 5, 6],
                                 [7, 8, 9] ]

two_plus_three = 2 + \
                 3

# Строки
single_quoted_string = 'наука о данных' 
double_quoted_string = "наука о данных"

tab_string = "\t"      # обозначает символ табуляции
len(tab_string)        # = 1

not_tab_string = r"\t" # обозначает символы '\' и 't'
len(not_tab_string)    # = 2

multi_line_string = """Это первая строка.
                       это вторая строка
                       это третья строка"""

try:
    print(0 / 0)
except ZeroDivisionError:
    print("нельзя делить на ноль")

integer_list =[1,2,3]                                    # список целых чисел
heterogeneous_list = ["строка", 0.1, True]               # разнородный список
list_of_lists = [ integer_list, heterogeneous_list, [] ] # список списков
list_length = len(integer_list)                          # длина списка = 3
list_sum = sum(integer_list)                             # сумма значений в списке = 6

x = list(range(10)) # задает список [0, 2, ..., 9]

first_three = x[:3]                 # первые три = [-1, 1, 2]
three_to_end = x[3:]                # с третьего до конца = [3, 4, 9]
one_to_four = x[1:5]                # с первого по четвертый = [1, 2, 3, 4]
last_three = x[-3:]                 # последние три = [7, 8, 9]
without_first_jand_last = x[1:-1]   # без первого и последнего = [1, 2,
copy_of_x = x[:]                    # копия списка х = [-1, 1, 2, 9]
x = [1, 2, 3]
x.extend([4, 5, 6]) # теперь х = [1, 2, 3, 4, 5, 6]

x = [1, 2, 3]
y = x + [4, 5, 6] # у - [1, 2, 3, 4, 5, 6]; х не изменился
x, y = [1, 2] # теперь х = 1, у = 2

# Кортежи обеспечивают удобный способ для возвращения из функций нескольких значений:
# функция возврашдет сумму и произведение двух параметров
def sum_and_product(x, y) :
    return (x + y),(x * y)
sp = sum_and_product(2, 3)     # = (5, 6)
s, p = sum_and_product(5, 10)  # s = 15, р = 50

empty_dict = {}                     # задать словарь по-питоновски
grades = {"Joel" : 80, "Tim" : 95}  # литерал словаря (оценки за экзамены)
# Доступ к значению по ключу можно получить при помощи квадратных скобок:
joels_grade = grades["Joel"] # = 80
# При попытке запросить значение, которое в словаре отсутствует, будет выдано сообщение об ошибке KeyError:
try:
    kates_grade = grades["Kate"]
except KeyError:
    print("оценки для Кэйт отсутствуют!")

# Проверить наличие ключа можно при помощи оператора in:
joel_has_grade = "Joel" in grades # True
kate_has_grade = "Kate" in grades # False
# Словари имеют метод get(), который при поиске отсутствующего ключа вместо
# вызова исключения возвращает значение по умолчанию:
joels_grade = grades.get("Joel", 0)  # =80
kates_grade = grades.get("Kate", 0)  # =0
no_ones_grade = grades.get("No One") # значение по умолчанию = None
grades ["Tim"] =99 # заменяет старое значение
grades["Kate"] = 100 # добавляет третью запись

# простого способа представить структурные данные:
tweet = {
    "user" : "joelgrus",
    "text" : "Наука данных - потрясающая тема",
    "retweet_count" : 100,
     "hashtags" : ["#data", "#science", "#datascience", "#awesome", "#yolo"]
} 

# Помимо поиска отдельных ключей можно обратиться ко всем сразу

tweet_keys = tweet.keys()       # список ключей
tweet_values = tweet.values()   # список значении
tweet__items = tweet.items()    # список кортежей (ключ, значение)

# Множества будут использоваться по двум причинам. Во-первых, операция in на
# множествах очень быстрая. Если необходимо проверить большую совокупность
# элементов на принадлежность некоторой последовательности, то структура данных
# set подходит для этого лучше, чем список:
# список стоп-слов

stopwords_list = ["a","an","at"] + ["hundreds_of_other_words"] + ["yet", "you"]
"zip" in stopwords_list # False, но проверяется каждый элемент
# множество стоп-слов
stopwords_set = set(stopwords_list)
"zip" in stopwords_set , # очень быстрая проверка

# Вторая причина — получение уникальных элементов в наборе данных:
item_list = [1, 2, 3, 1, 2, 3]          # список
num_items = len(item_list)              # количество = 6
item_set = set(item_list)               # вернет множество {1, 2, 3}
num_distinct_iterns = len(item_set)     # число недублирукщихся = 3
distinct_item_list = list(item_set)     # назад в список = [1, 2, 3]











