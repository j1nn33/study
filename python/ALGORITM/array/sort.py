# ----------------------------------------
# SORT  Квадратичные O(N^2)

def inser_sort(A):
    """ сортировка списка А вставками """
    N = len(A)
    for top in range(1, N):  # 1 элемент не берем
        k = top 
        while k > 0 and A[k-1] > A[k]: # порядок важен т.к. and ленивый (т.е. при k=0 вторая часть выражения вчисляться не будет)
            A[k], A[k-1] = A[k-1], A[k]
            k-=1             # уменьшаем позицию на 1 

    return 

def choise_sort(A):
    """ сортировка списка А выбором"""
    N = len (A)
    for pos in range (0, N-1): # последний элемент не берем
        for k in range (pos+1, N):
            if A[k] < A[pos]:
                A[k], A[pos] = A[pos], A[k]

    return

def bubble_sort(A):
    """ сортировка списка А методом пузырька"""
    N = len(A)
    for bypass in range (1, N):
        for k in range (0, N-bypass):
            if A[k] > A[k+1]:
                 A[k], A[k+1] = A[k+1], A[k]

    return

# SORT  Подсчетом O(N)  по память O (M) где М - количество элементов
# идея подсчет частоты появления элементов
# важно знать диапазон допустимых значений и он должен быть маленьким
# A[1,2,3,4,5,6,7,1,4,5,3,4,5,6,2,5,6,4,3,2,]
def count_sort(A):
    """ сортировка подсчетом частоты появления элементов"""
    N = len (A)
    B=[]
    F= [0]*(N+1)     # у нас допустим максиму 20 разных элементов
    for i in range (0, N): # получаем массив частот для каждого элемента 
        k=A[i]
        F[k] +=1
    
    for i in range (0, len(F)):
        if F[i]>0:
            for j in range(F[i]):
                B.append(i)
      
    # копирование отсортированного массива в оригинал
    for i in range (0, N):
        A[i]=B[i]        
    return 
    
 
def test_sort(sort_algoritm):
    print ("Тестирутем: ", sort_algoritm.__doc__)
    print ("testcase #1 : ", end="")
    A = [4, 2, 5, 1, 3]
    A_sorted = [1, 2, 3, 4, 5]
    sort_algoritm(A)
    print ("Ok" if A== A_sorted else "Fail")

    print ("testcase #2 : ", end="")
    A = list(range(10, 20)) + list (range(0, 10))
    A_sorted = list (range(20))
    sort_algoritm(A)
    print ("Ok" if A== A_sorted else "Fail")

    print ("testcase #3 : ", end="")
    A = [4, 2, 4, 2, 1]
    A_sorted = [1, 2, 2, 4, 4]
    sort_algoritm(A)
    print ("Ok" if A== A_sorted else "Fail")
    

if __name__ == "__main__":
    test_sort(inser_sort)
    test_sort(choise_sort)
    test_sort(bubble_sort)
    test_sort(count_sort)
