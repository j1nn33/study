"""
Пример РЕФАКТОРИНГА программы (переход от функционального подхода к ООП)

вариант - функционального подхода
процесс рисования шарика раскидан по функциям в программе
проблемма:
 - поддуржка программы затруднительна
 - дополнительный функционал внедрить сложно без переработки практически 
   всех функций
 - наличие глобальных переменных

"""

import tkinter as tk
from random import randint

WIDTH = 300
HEIGHT = 200

def canvas_click_handler(event):   
    """ функция получения координат при нажатии курсора
    """
    print('Hello World! x=', event.x, 'y=', event.y)

def tick():
	""" функция движения шарика на эране
	"""
    global x, y
    # print("move")
    x += 1
    y += 1
    canvas.move(ball_id, +1, +1)
    root.after(50, tick)


def main():
    global root, canvas
    global ball_id, x, y, z  # TODO: сделать объекно-ориентированный рефакторинг
    
    # относится к графике 
    root = tk.Tk()
    root.geometry(str(WIDTH) + "x" + str(HEIGHT))
    canvas = tk.Canvas(root)
    canvas.pack(anchor="nw", fill=tk.BOTH)
    canvas.bind('<Button-1>', canvas_click_handler)

    # относится к шарику 
    R = randint(20, 50)
    x = randint(R, WIDTH - R)
    y = randint(R, HEIGHT - R)
    ball_id = canvas.create_oval(x - R, y - R, x + R, y + R, fill="green")

    tick()
    root.mainloop()


if __name__ == "__main__":
    main()