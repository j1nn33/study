# линейный поиск в массиве

def array_search (A:list, N:int, x:int):
    """ A - массив, N - размер массива, x - искомое число 
	    Осуществляет поиск числа x в массиве A
	    от 0 до N-1 индекса включительно.
	    Возвращает индекс элемента x в массиве А.
	    Или -1, если такого нет.
	    Если в массиве несколько одинаковых элементов
	    равных х, то вернуть индекс первого по счету.
    """
    for k in range (N):
        if A[k] ==x:
            return k
    return -1 # если элемент не найден

def test_array_search():
    A1 = [1, 2, 3, 4, 5]
    m = array_search (A1, 5, 8)
    if m ==-1:
        print ("# test_1 - ok")
    else:
        print ("# test_1 - fail")

    A2 = [-1, -2, -3, -4, -5]
    m = array_search (A2, 5, -3)
    if m == 2:
        print ("# test_2 - ok")
    else:
        print ("# test_2 - fail")

    A3 = [10, 20, 30, 10, 10]
    m = array_search (A3, 5, 10)
    if m == 0:
        print ("# test_3 - ok")
    else:
        print ("# test_3 - fail")

test_array_search()