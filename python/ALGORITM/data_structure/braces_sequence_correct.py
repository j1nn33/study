
# Проверка корректности скобочной последовательности
# A="" - пустое корректное скобочное выражение 
# B = (A) - А взятое в скобки будет корректным скобочным выражением
# С = АВ - будет корректным скобочным выражением
# все остальное полученное не по этим правилам 
# не будет корректным скобочным выражением
# (((())))()(((((()))))) - корректно (кол-во открытых скобок равно кол-ву закрытых)
# "())(()" не будет корректным скобочным выражением
#  10-1010 
# ( - n+1, ) - n-1
#    )(  - запрещеная ситуация n<0
#
# задача при двух видах скобок (),[]
# [(())]([]) - корректная
# [), [(]), [([[([])]]])  - не корректное
# решение
# для каждой очередной скобки проверям 
#  если она открывающаяся, то помещаем ее в стек
#  если она закрывающая то проверяам
#       если стек пуст, то сразу не корректно
#       иначе забираем скобку из стека и проверям ее тип не совпадает с очередной, то не корректно
#       иначе ОК


import A_stack


def is_braces_sequence_correct(s: str):
    """
    Проверяет корректность скобочной последовательности
    из круглых и квадратных скобок () []
    >>> is_braces_sequence_correct ("[]")
    True
    >>> is_braces_sequence_correct ("(([()]))[]")
    True
    >>> is_braces_sequence_correct ("([)]")
    False
    >>> is_braces_sequence_correct ("(")
    False
    >>> is_braces_sequence_correct ("]")
    False
    """
    A_stack.clear()
    for brace in s:   # brace - текущая скобка
        if brace not in "()[]":  # игнорирование других символов
            continue
        if brace in "([":         # открывающая скобка
            A_stack.push(brace)
        else:
            assert brace in ")]", "ERROR - ожидалась закрывающая скобка" + str(brace)
            if A_stack.is_empty():
                return False
            left = A_stack.pop()   # получае скобку из стека
            assert left in "(["  "ERROR - ожидалась открывающая скобка" + str(brace)
            if left == "(":
                right = ")"
            elif left == "[":
                right ="]"
            if right != brace:
                return False
    return A_stack.is_empty()
    """    
    return A_stack.is_empty(): - проверка что стек пустой
    if A_stack.is_empty():
        return True
    else:
        return False
    """            
        
if __name__ == "__main__":
    import doctest
    #doctest.testmod(verbose=True)
    print(doctest.testmod())
    # 2 вариант тестов
    print ('Ок',  is_braces_sequence_correct ("[]"))
    print ('Ок',  is_braces_sequence_correct ("(([()]))[]"))
    print ('Not', is_braces_sequence_correct ("([)]"))
    print ('Not', is_braces_sequence_correct ("("))
    print ('Not', is_braces_sequence_correct ("]"))
   
   