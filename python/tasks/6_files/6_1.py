# Аналогично	заданию	3.6	обработать	строки	из	файла	ospf.txt	и	вывести	информацию
# по	каждой	в	таком	виде:

#Protocol:			    OSPF
#Prefix:				10.0.24.0/24
#AD/Metric:				110/41
#Next-Hop:				10.0.13.3
#Last update:			3d18h
#Outbound Interface:	FastEthernet0/0

#with open('/home/ubuntu/workspace/python/tasks/6_files/ospf.txt', 'r') as f:
with open('./ospf.txt', 'r') as f:
#with open('../6_files/ospf.txt', 'r') as f:
    for ospf_route in f:
        ospf_route = ospf_route.replace('O', 'OSPF') # замена О на OSPF в строке
        list_ospf_route = ospf_route.split(" ")      # преобразование строки в список
        print ("Protocol:           ", list_ospf_route [0])
        print ('Prefix:             ', list_ospf_route [8])
        print ('AD/Metric           ', list_ospf_route [9].strip('[]')) # удаление []
        print ('Next-Hop:           ', list_ospf_route [10])
        print ('Last update:        ', list_ospf_route [11])
        print ('Outbound Interface: ', list_ospf_route [12])
     
   
  