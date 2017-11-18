import random
number = random.randint(0, 101)

while True:

    answer = input("Введите число : ")
    if not answer or answer == "exit":
        break

    if not answer.isdigit():
        print("input right digit")
        continue

    user_answer = int(answer)

    if user_answer > number:
        print("digit <")
    elif user_answer < number:
        print("digit >")
    else:
        print("you win")
        break

