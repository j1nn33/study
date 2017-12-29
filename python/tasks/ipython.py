
"""
d_keys = ['hostname', 'location', 'vendor', 'model', 'IOS', 'IP']
data = {'r1': ['london_r1', '21 New Globe Walk', 'Cisco', '4451', '15.4', '10.255.0.1'],
        'r2': ['london_r2', '21 New Globe Walk', 'Cisco', '4451', '15.4', '10.255.0.2'],
       'sw1': ['london_sw1', '21 New Globe Walk', 'Cisco', '3850', '3.6.XE', '10.255.0.101']
       }
"""
london_co = {}
#d_keys = ['x', 'y', 'z']
level_1 = {'a1':['b','cbb'],
           'aa1':['bb']}
level_2 = {'b':['c3'], 
           'cbb':['cc3']}

for k1 in level_1:
    #print('k1',k1)
    
    for k2 in level_2:
        d2={}
        d2[k2]=level_2[k2]   # сделали под словарь те 2 значение словаря
        #print ('level_1[k1]',level_1[k1])
        #print ('level_2',k2)
        print ('###################')
        print ('item_1',level_1[k1])
        print ('k2',k2)
        #print (level_2[k2])
        #london_cod=dict.fromkeys(k2,k1) 
        #london_co.update(dict(level_1,level_2[k2]))
        #london_co[k1]=(k2,level_2[k2])
        
        #print (d2)
        #if level_1[k1]==level_2:
        if k2 in level_1[k1]:
            print('BANG')
            for l in d2:
                london_co[k1]=d2[k2]
        #london_co[k1]=d2
                print (london_co)
#for k in level_1:.
    



"""
any(word in command for word in ignore)
dict[key] = value
for k in level_1:
    #print(k)
    london_co[k] = dict(zip(level_2,level_1[k]))
"""
print ('final')
print(london_co)

#london_co[k] = dict(zip(d_keys,data[k]))