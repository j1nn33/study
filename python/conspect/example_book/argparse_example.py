import argparse
# Для начала работы с argparse необходимо задать парсер
parser = argparse.ArgumentParser()
# Далее, парсеру стоит указать, какие объекты Вы от него ждете.
# задание аргумента square type=int
parser.add_argument("square", type=int,
                    help="display a square of a given number")
# задание аргумента -v , action - действие для данного аргумента                     
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
# создаем объект с заданными выше характеристиками 
args = parser.parse_args()
answer = args.square**2
if args.verbose:
    print("the square of {} equals {}".format(args.square, answer))
else:
    print(answer)
    
# python3 /home/ubuntu/workspace/python/tasks/ipython.py 3 -v
# the square of 3 equals 9