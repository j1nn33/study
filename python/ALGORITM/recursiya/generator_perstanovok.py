# Генерация всех перестановок
# {1, 2, 3, ... N } - числа
# N*(N-1)*(N-3)*...2*1 = N! - факториал
# 0.0.0.0  до   N-1.N-1.N-1.N-1

def generate_numbers (N:int, M:int, prefix = None): # N - основание системы счисления M - длина числа
    """ Генерирует все числа (с лидирующими незначащими нулями)
        в N-ричной системы счисления (N <= 10) длины M """
    prefix = prefix or [] # генерация пустого списка если prefix = None
    if M ==0:
        print (prefix)
        return
    
    for digit in range (N):
        prefix.append(digit)
        generate_numbers(N, M-1,prefix)
        prefix.pop() 

generate_numbers (4, 3)

# 2 - вариант (для двоичной системы)
def gen_bin(M, prefix=""):
    if M ==0:
        print (prefix)
    else:
        for digit in "0", "1":
            gen_bin(M-1, prefix + digit)
        

gen_bin(3)