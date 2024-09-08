from collections import Counter # словарь Counter не загружается по умолчанию
#print ('tets_programm')

# пользоватли 
users = [  { "id": 0, "name": "Hero" },
           { "id": 1, "name": "Dunn" },
           { "id": 2, "name": "Sue" },
           { "id": 3, "name": "Chi" },
           { "id": 4, "name": "Thor" },
           { "id": 5, "name": "Clive" },
           { "id": 6, "name": "Hicks" },
           { "id": 7, "name": "Devin" },
           { "id": 8, "name": "Kate" },
           { "id": 9, "name": "Klein" },
        ]

#print ('printing sourse data')

# отношение между пользователями (0 связан с 1)
friendships = [(0, 1), (0,2), (1, 2), (1, 3), (2, 3), (3, 4),
               (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)
              ]


# интересующие темы
interests = [
(0,"Hadoop"), (0,"Big Data"), (0,"HBase"), (0,"Java"),
(0,"Spark"), (0,"Storm"), (0,"Cassandra"),
(1,"NoSQL"), (1,"MongoDB"), (1,"Cassandra"), (1,"HBase"),
(1, "Postgres"), (2,"Python"), (2,"scikit-learn"), (2,"scipy"),
(2,"numpy"), (2,"statsmodels"), (2,"pandas"), (3,"R"), (3,"Python"),
(3,"statistics"), (3,"regression"), (3,"probability"),
(4,"machine learning"), (4,"regression"), (4,"decision trees"),
(4,"libsvm"), (5,"Python"), (5,"R"), (5,"Java"), (5,"C++"),
(5,"Haskell"), (5,"programming languages"), (6,"statistics"),
(6,"probability"), (6,"mathematics"), (6,"theory"),
(7,"machine learning"), (7,"scikit-learn"), (7,"Mahout"),
(7,"neural networks"), (8,"neural networks"), (8,"deep learning"),
(8,"Big Data"), (8,"artificial intelligence"), (9,"Hadoop"),
(9,"Java"), (9,"MapReduce"), (9,"Big Data")
]


#print ('printing sourse data')
#print ('')
#print ('users')
#print (users)
#print ('')
#print ('friendships')
#print (friendships)

# обогащение users свойство friends (пустой список) содержит друзей для пользователя user
for user in users:
    user["friends"] = []

#print ('users whith add friends')
#print (users)

# заполним эти списки данными из списка кортежей friendships:
for i, j in friendships:
    users[i]["friends"].append(users[j]) # добавить j как друга для i
    users[j]["friends"].append(users[i]) # добавить i как друга для j

print ('users whith add data friends ')
print (users[i])

# число друзей
def number_of_friends(user):
    """сколько друзей есть пользователя user?"""
    print ('number of users', len(user["friends"]))
    return len(user["friends"])                      # длина списка id друзей
print ()

total_connections = sum(number_of_friends(user)  # общее число связей
                        for user in users)
print ('общее число связей total_connections', total_connections)
print ('')
num_users = len(users) # длина списка пользователей
print (' длина списка пользователей ', num_users)
avg_connections = total_connections / num_users                           

# число друзей для каждого id пользователя
# создать список в формате (id пользователя, число друзей)
num_friends_by_id = [(user["id"], number_of_friends(user))
                     for user in users]
print (num_friends_by_id)

# упорядочить по полю num_friends 
#sorted(num_friends_by_id, key=lambda (user_id, num_friends): num_friends, reverse=True)               

# не тот же самый
def not_the_same (user, other_user):
    """два пользователя не одинаковые, если их ключи имеют разные id"""
    return user["id"] !=other_user["id"]

# не друзья
def not_friends(user, other_user):
    """other_user - не друг, если он не принадлежит user["friends"], те.
    если он not_the_same (не тот же что и все люди в user["friends"])"""
    return all(not_the_same(friend, other_user)
               for friend in user["friends"])

# список id друзей пользователя user
def friends_of_friend_ids(user):
    return Counter (foaf [ "id" ]
                    for friend in user["friends"]
                    for foaf in friend["friends"]
                    if not_the_same(user, foaf)
                    and not_friends(user, foaf))
# для каждого моего друга подсчитать ИХ друзей,
# которые не являются мной  и не мои друзья
print(friends_of_friend_ids(users[3])) 
# Counter({0: 2, 5: 1})


# Функция, которая находит пользователей, интересующихся определенной темой
# аналитики, которым нравится целевая тема target_interest
def data_scientists_who_like(target_interest):
    return [user_id
            for user_id, user_interest in interests
            if user_interest == target_interest]

# Если пользователей и тем много (либо планируется выполнять
# много запросов), то лучше создать индексный список пользователей, сгруппированный по теме:
from collections import defaultdict

# id пользователей по значению темы
# ключи - это интересующие темы,
# значения - это списки из id пользователей, интересующихся этой темой

user_ids_by_interest = defaultdict(list)
for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)

# И еще индексный список тем, сгруппированный по пользователям:
# идентификаторы тем по идентификатору пользователя
# ключи - это id пользователей, значения - списки тем для конкретного id
interests_by_user_id = defaultdict(list)
for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)

# Подсчитать, сколько раз встретятся другие пользователи.
# наиболее общие интересующие темы с пользователем user
def most_coiranon_interests_with(user):
    return Counter(interested_user_id
        for interest in interests_by_user_id[user["id"]]
        for interested_user_id in user_ids_by_interest[interest]
        if interested_user_id != user["id"])

# зарплаты и стаж
salaries_and_tenures = [(83000, 8.7), (88000, 8.1),
                        (48000, 0.7), (76000, 6),
                        (69000, 6.5), (76000, 7.5), 
                        (60000, 2.5), (83000, 10),
                        (48000, 1.9), (63000, 4.2)]

# зарплата в зависимости от стажа
# ключи - это годы, значения - это списки зарплат для каждого стажа
salary_by_tenure = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    salary_by_tenure[tenure].append(salary)

# средняя зарплата в зависимости от стажа
# ключи - это годы, каждое значение - это средняя зарплата по этому стажу
average_salary_by_tenure = {
    tenure : sum (salaries) / len(salaries)
    for tenure, salaries in salary_by_tenure.items()
}

# Целесообразнее разбить продолжительности стажа на интервалы:
# стажная группа
def tenure_bucket (tenure):
    if tenure < 2:
        return "менее двух"
    elif tenure < 5:
        return "между двумя и пятью"
    else:
       return "более пяти"


# зарплата в зависимости от стажной труппы
# ключи = стажные группы, значения = списки зарплат в этой группе
# словарь содержит списки зарплат, соответствующее каждой стажной группе
salary_by_tenure_bucket = defaultdict(list)
for salary, tenure in salaries_and_tenures:
    bucket = tenure_bucket(tenure)
    salary_by_tenure_bucket[bucket].append(salary)

print ('salary_by_tenure_bucket', salary_by_tenure_bucket)
# средняя зарплата по группе
# ключи = стажные группы, значения = средняя зарплата по этой группе
average_salary_by_bucket = {
    tenure_bucket : sum (salaries) / len(salaries)
    for tenure_bucket, salaries in salary_by_tenure_bucket.items()
}
print (average_salary_by_bucket)