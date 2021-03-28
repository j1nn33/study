# Создали список из словарей книг
# Программа для парсинга файла и получения из него данных согласно полученным параметрам
#
"""
[
  {'title' : 'Game of Thrones', 'published' : '1996-08-01', 'pages': 694},
  {'title' : 'Clash of Kings', 'published' : '1998-11-16', 'pages': 761},
  {'title' : 'Storm of Swords', 'published' : '2000-08-08', 'pages': 973},
  {'title' : 'Feast for Crows', 'published' : '2005-10-17', 'pages': 753},
  {'title' : 'Dance with Dragons', 'published' : '2011-07-12', 'pages': 1016}
]
"""




def read_fromfile(file):
  print ('OPEN FILE  - ', file)
  mas = []
  with open("D:\CODE\STYDI\\file.txt", "r") as f:
        mas_str = f.read()
  #print (mas_str, type(mas_str))
  mas=eval(mas_str)
  return mas

def analys (list_of_data, tuz):
  db_list=[]
  db_tmp=[]
  for i in list_of_data:
    #print(type(i),i)
    if tuz in i.values():
      db_tmp.append(i)
      db_list.append(i.get('pages'))
  #print('db_tmp',db_tmp)
  print(db_list)


  
 #print (mas[1], type(mas))



if __name__ == "__main__":
    #print ('read file')
    file = 'D:\CODE\STYDI\\file.txt'
    tuz= 'Game of Thrones'
    list_of_data=[]    
    list_of_data = read_fromfile(file)
    #print (list_of_data)
    #print (list_of_data.get('title'))
    analys(list_of_data, tuz)

