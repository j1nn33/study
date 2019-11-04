# структуры данных
# СТЕК или очередь LIFO (последний пришел - перывй выше)
"""
push      - положить
pop       - взять
size      - размер стека
top       - прочитать верхушку
is_empty  - проверить пустойли стек True, False

реализация (план)
1 - создать простой use case использования стека
  use case:
      clear ()  # очистка стека
      is_empty () --> True
      push (1)
      push (2)
      push (3)
      is_empty () --> False
      pop ()   --> 3
      pop ()   --> 2
      pop ()   --> 1
      is_empty () --> True

2 - вариант 1 на массиве list
  - 
"""


_stack = []  # сам стек


def push(x):
    """
    Добавляет элемент x в конец стека
    >>> size = len(_stack)
    >>> push(5)
    >>> len(_stack) - size  # размер увеличился на 1
    1
    >>> _stack[-1]    # top
    5
    """
    _stack.append(x)


def pop():
    """
 
    >>> push (1)
    >>> push (5)
    >>> size = len(_stack)
    >>> pop()
    5
    >>> size - len(_stack)
    1
    >>> _stack[-1]
    1

    """
    x = _stack.pop()
    return x


def clear():
    _stack.clear()


def is_empty():
    return len(_stack) == 0


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    #doctest.testmod(verbose=True)
    print(doctest.testmod())
