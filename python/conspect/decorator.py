# ФУНКЦИИ-ДЕКОРАТОРЫ
# Функции языка Python являются объектами, так что любая из них может принимать в качестве аргумен
# тов другие функции. Синтаксис декоратора — простой и аккуратный способ сделать это. Простейший 
# формат декоратора:
def some_decorator(wrapped_function):
    def wrapper():
        print('Do something before calling wrapped function')
        wrapped_function()
        print('Do something after calling wrapped function')
    return wrapper

# Мы можем описать другую функцию и передать ее как аргумент этой функции:
def foobat():
    print('foobat')

f = some_decorator(foobat)
f()

# Do something before calling wrapped function
# foobat
# Do something after calling wrapped function


# Синтаксис декоратора упрощает эту задачу, позволяя указать обертываемую функцию посредством 
# декорирования ее аннотацией @название_декоратора. Вот пример использования синтаксиса 
# декоратора для функции some_decorator:

@some_decorator
def batfoo():
    print('batfoo')
batfoo()

# Do something before calling wrapped function
# batfoo
# Do something after calling wrapped function

# Теперь можно вызывать обернутую функцию по ее имени, а не по имени декоратора. Готовые функции-декораторы 
# включены в состав как стандартной библиотеки языка Python (staticMethod, 
# classMethod), так и сторонних пакетов, таких как Flask и Click

# Пример использования clic для ввода аргументов коммандной строки 

#!/usr/bin/env python
"""
Простой пример использования библиотеки Click
"""
import click
@click.command()
@click.option('--greeting', default='Hiya', help='How do you want to greet?')
@click.option('--name', default='Tammy', help='Who do you want to greet?')
def greet(greeting, name):
    print(f"{greeting} {name}")
if __name__ == '__main__':
    greet()

######
# $ ./simple_click.py --greeting Privet --name Peggy
# Privet Peggy
# $ ./simple_click.py --help
# Usage: simple_click.py [OPTIONS]
# Options:
#   --greeting TEXT  How do you want to greet?
#   --name TEXT      Who do you want to greet?
#   --help           Show this message and exit
# ############################
# Реализация вложенных комманд
# ./click_example.py --help
# Usage: click_example.py [OPTIONS] COMMAND [ARGS]...
# Options:
#   --help  Show this message and exit.
# Commands:
#   sailors  Talk to a sailor
#   ships    Ship related commands
# посмотреть справку для подгруппы:
# $ ./click_example.py ships --help
# Usage: click_example.py ships [OPTIONS] COMMAND [ARGS]...
#   Ship related commands
# Options:
#   --help  Show this message and exit.
# Commands:
#   list-ships  List all of the ships
#   sail        Sail a ship

######################
#!/usr/bin/env python
"""
Утилита командной строки, использующая click
"""
import click
@click.group() # Создаем группу верхнего уровня для прочих групп и команд.

# Создаем функцию, которая будет выступать в роли группы верхнего уровня. 
# Метод click.group преобразует функцию в группу
def cli(): 
    pass
@click.group(help='Ship related commands') 
#  Создаем группу для команд ships.
def ships():
    pass
cli.add_command(ships)
# Добавляем в группу верхнего уровня группу ships в качестве команды. 
# Обратите внимание на то, что функция cli теперь представляет собой группу 
# с методом add_command
@ships.command(help='Sail a ship')
# Добавляем команду в группу ships. Обратите внимание на то, что вместо 
# click.command мы используем ships.command
def sail():
    ship_name = 'Your ship'
    print(f"{ship_name} is setting sail")
@ships.command(help='List all of the ships')
def list_ships():
    ships = ['John B', 'Yankee Clipper', 'Pequod']
    print(f"Ships: {','.join(ships)}")
@cli.command(help='Talk to a sailor') 
# Добавляем команду в группу cli.
@click.option('--greeting', default='Ahoy there', help='Greeting for sailor')
@click.argument('name')
def sailors(greeting, name):
    message = f'{greeting} {name}'
    print(message)
if __name__ == '__main__':
    # Вызываем группу верхнего уровня.
    cli()