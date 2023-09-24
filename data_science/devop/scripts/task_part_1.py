#  Напишите функцию Python, принимающую название в качестве аргумента и выводящую его в консоль.
#  Напишите функцию Python, принимающую строку в качестве аргумента и выводящую в консоль информацию о ее регистре.
#  Напишите списковое включение для получения списка букв слова smogtether в верхнем регистре.
#  Напишите генератор, попеременно возвращающий слова «Четное» и «Нечетное».


def funk_1 (a): 
   print(a)
   
def funk_2 (var_string):
   if var_string.islower():
      print ("LOW")
   else: 
       if var_string.isupper():
          print("UPPER")
       else:
          print("Shuffle")   
        
def funk_3 (var_string):
    var_list = []
    var_string_1 = var_string.upper()
    for i in var_string_1:
        var_list.append(i)
    
    print (var_list)

def funk_4():
    n = 0
    while (n<10):
       n+=1
       x = "Нечетное"
       if n%2: 
           print (n)
           x = "Нечетное"
       else:
           print (n)
           x = "Четное"  
       yield x 

if __name__ == "__main__":
   var_name = "SOMETHING"
   
   var_string_1 = "Someting"
   var_string_2 = "SOMETHING"
   var_string_3 = "someting"
   
   var_string_4 = "smogtether"
   
   funk_1 (var_name)
   
   funk_2 (var_string_1)
   funk_2 (var_string_2)
   funk_2 (var_string_3)
   
   funk_3 (var_string_4)

   for i in funk_4():
      print (i)