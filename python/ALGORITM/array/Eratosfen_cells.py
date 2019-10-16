# решето Эратосфена

N=20
A =[True]*N
A[0]=A[1]=False
for k in range (2, N):
    if A [k]:     # если A [k]: True
        for m in range(2*k, N, k):
            A[m] = False

print(A)
for k in range(N):
    print (k, '-', A[k], '--', "SIMPLE " if A[k] else "COMPLEX")
