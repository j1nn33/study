# циклический сдвиг
def to_left(A:list ,N:int):
    tmp = A[0]
    for k in range(N-1):
        A[k]=A[k+1]

    A[N-1]=tmp
    return A

def to_right (A:list ,N:int):
    tmp = A[N-1]
    for k in range(N-1,-1,-1):
        A[k]=A[k-1]

    A[0]=tmp
    return A


B = [0, 1, 2, 3, 4, 5]

print ('original', B)

to_left(B, 6)
print ('to left ', B)

to_right(B, 6)

print ('to right', B)