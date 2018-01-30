# МАТРИЦЫ или ДВУМЕРНЫЕ МАССИВЫ

# вложенные списки

M = [[1, 2, 3],
     [4, 5, 6,],
     [7, 8, 9]]
     
print (M)
# [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print (M[1])
# [4, 5, 6]
print (M[1][2])  # получить 2 строку, 3 элемент в этой строке
# 6

# Генераторы списков
column2 = [row[1] for row in M] # вторая колонна
print (column2)
# [2, 5, 8]

column3 = [row[1]+1 for row in M] # вторая колонна
print (column3)

# нечетные значения в колонне 2
filter1 = [row[1] for row in M if row[1]%2 == 0]
print (filter1)
#[2, 8]

# выборка элементов по диагонали
diag = [M[i][i] for i in [0, 1, 2]]
print (diag)
# [1, 5, 9]
# дублирование символов в строке
doubles = [c*2 for c in 'spam']
print (doubles)
# ['ss', 'pp', 'aa', 'mm']

# Генератор, возвращающий суммы элементов строк

G = (sum(row)for row in M)
print (G)
# <generator object <genexpr> at 0x7f4eb9754b40>
print(next(G))
# 6

# сумма на элементы
print (list(map(sum, M)))
# [6, 15, 24]