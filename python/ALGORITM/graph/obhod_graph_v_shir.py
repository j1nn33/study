# Обход графов в ширину (BFS)
"""
0    2   {0:{1,4},
| \/ |    1:{0,3,4},
|  4 |    2:{3,4},
|/   |    3:{1,2},
1----3    4:{0,1,2}}
"""

"""
N, M = map(int, input().split())      # считываем кол-во вершин и кол-во ребер

graph = {i:set() for i in range(N)}   # хранение графа в виде словаря с множествами 
for i in range (M):
    v1, v2 = map(int,input().split()) # считываение ребра
    graph[v1].add(v2)                 # добавление смежности двух вершин
    graph[v2].add(v1)
"""
N = 15
M = 16
graph = {0 :{1, 10, 11, 12},
         1 :{0, 7},
         2 :{6},
         3 :{11},
         4 :{10},
         5 :{8, 13},
         6 :{2, 4, 10},
         7 :{1, 13},
         8 :{5, 12},
         9 :{11},
         10:{0, 4, 6},
         11:{0, 3, 9, 12, 14},
         12:{0, 8, 11},
         13:{5, 7},
         14:{11}}

from collections import deque         # deque – это обобщение стеков и очередей
distances = [None] * N                # массив расстоянией, по умолчанию неизвестно
start_vertex = 0                      # начинаем с 0 вершины
distances[start_vertex] = 0               # расстояние до себя равно 0
queue = deque([start_vertex])         # создание очередь

while queue:                                             # пока очередь не пуста
    cur_v = queue.popleft()                              # достаем первый элемент
    for neight_v in graph[cur_v]:                        # перебераем его соседей
        if distances[neight_v] is None:                  # если сосед еще не посещен (=> расстояние None)
            #print(neight_v)
            #print(distances[neight_v])
            distances[neight_v]= distances[cur_v] + 1    # подсчет расстояния
            queue.append(neight_v)                       # добавление в очередь чтобы проверить и его соседей

print(distances)                                         

# восстановление кратчайшего расстояния
start_vertex = 0
end_vertex = 2

parents = [None] * N
distances = [None] * N
distances[start_vertex]=0
queue = deque ([start_vertex])

while queue:
    u = queue.popleft()
    for v in graph[u]:
        if distances[v] is None:
            distances[v] = distances [u] +1
            parents[v] = u
            queue.append(v)

path = [end_vertex]
parent = parents[end_vertex]
while not parent is None:
    path.append(parent)
    parent = parents[parent]
print(path[::-1])
