def invert_array(A:list, N:int):
    """
    инвертирует массиы
    """
    for k in range (N//2):
        # N//2 обмен переменных до средины массива
        A[k], A[N-1-k] = A[N-1-k], A[k]
    return A

def test_invert_array():
    A1 = [1, 2, 3, 4, 5]
    print ('before', A1)
    invert_array(A1, 5)
    print ('after', A1)
    if A1 == [5, 4, 3, 2, 1]:
        print("# test_1 - ok")
    else:
        print("# test_1 - fail")

    A2 = [0, 0, 0, 0, 0, 0, 0, 0, 10]
    invert_array(A2, 9)
    if A2 == [10, 0, 0, 0, 0, 0, 0, 0, 0]:
        print("# test_1 - ok")
    else:
        print("# test_1 - fail")

test_invert_array()