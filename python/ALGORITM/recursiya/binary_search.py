# бинарный поиск  O(log2N)
# требование: массив должен быть отсортированный (наш пример по возрастанию)
# ищем левую границу (меньше текущего) и правую границу (больше текущего) от искомого индекса
#   -1  0  1  2  3     N-1 N
#  А = [1, 3, 3, 6, 7, 9] ищем key =5
# левая граница 3
# правая граница 6
# ищем эти границы в разных функциях
#
#  пример для 3 
#  left_bound  : left = A[0] right =A[1] 
#  right_bound : left = A[2] right =A[3] 

# данные функции можно использовать для поиска элемент в массиве
# если разница между границами больше 1
# или находить место вставки элемента в массив

def left_bound (A, key):
    left =-1
    right = len(A)
    while right-left > 1:
        middle = (left+right)//2
        if A[middle]<key:
            left=middle
        else:
            right=middle

    return left

def right_bound (A, key):
    left =-1
    right = len(A)
    while right-left > 1:
        middle = (left+right)//2
        if A[middle]<=key:
            left=middle
        else:
            right=middle

    return right

def search_element (A, key):
    if right_bound(A, key) - left_bound(A, key) > 1:
        print ('element is exist')
        print ('left_bound', left_bound(A, key))
        print ('right_bound', right_bound(A, key))
        print ('индекс искомого элемента в массиве', left_bound(A, key)+1)
    else:
        print ('element is not exist')
    
    return

A = [1, 3, 3, 6, 7, 9]
search_element(A, 6)
