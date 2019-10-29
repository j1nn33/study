# рекурсия алгоритм сборки матрешки
def matryoshka(n):
    if n == 1:
        print ("Матрешечка самая маленькая")
    else:
        print ("Верх матрешки n = ", n)
        matryoshka (n-1)
        print ("Низ матрешки n = ", n)

matryoshka (5)

# рекурсия и обычный способ
# факториал
# f(n) = 1, при n=0, n =1
# f(n) = f(n)*n, при n>1
#
def fac(n:int):
    assert n>=0, "Факториал отрицательного не определен"  # проверка на неотрицательное число
    if n == 0:
        return 1
    else:
       return n * fac(n - 1)

print ('рекурсия ', fac(5))

def fac(n):
    f = 1
    x = 2
    while x <= n:
        f *= x
        x += 1

    return f

print ('обычный ', fac(5))

# алгоритм Евклида
# найти наибольший общий делитель
#gcd (a,b) = a, при a=b
#gcd (a-b,b), при a>b
#gcd (a,b-a), при a<b
print ('алгоритм Евклида')

def gcd (a, b):
    if a == b:
        return a
    elif a>b:
        return gcd (a-b,b)
    else:      # a<b
        return gcd (a, b-a)

print (gcd(36,12))

print ('алгоритм Евклида upgrade')

def gcd (a, b):
    if b == 0:
        return a
    else:     
        return gcd (b, a%b)

print (gcd(36,12))

# --------------------------------------------
print ('алгоритм возведения в степень (рекурсия)')

def pow (a:float, n:int):
    if n == 0:
        return 1
    else:
        return pow (a, n-1)*a

print (pow(2, 3))

