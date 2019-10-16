# list generate 
A = [x**2 for x in range (10)]

print ('python  ', A)
A  = []
for x in range (10):
    A.append(x**2)
print ('ver - 1 ', A)

# ----------------------
print ('------------------')
A = [1,2,3,4,5,7,12,9,6]
B = []
for x in A:
    if x%2==0:
        B.append(x**2)
print ('ver - 1 ', B)

B=[x**2 for x in A if x%2 ==0]
print ('ver - 2 ', B)
B= [(0 if x<0 else x**2) for x in A if x%2 ==0]

print ('ver - 3 ', B)
