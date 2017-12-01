# Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
# Protocol: OSPF
# Prefix: 10.0.24.0/24
# AD/Metric: 110/41
# Next-Hop: 10.0.13.3
# Last update: 3d18h
# Outbound Interface: FastEthernet0/0

ospf_route = 'O 10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0'
print ('ospf_route ', type(ospf_route),ospf_route)
ospf_route = ospf_route.replace('O', 'OSPF') # замена О на OSPF в строке

list_ospf_route = ospf_route.split(" ")      # преобразование строки в список

print ("Protocol:           ", list_ospf_route [0])
print ('Prefix:             ', list_ospf_route [1])
print ('AD/Metric           ', list_ospf_route [2].strip('[]')) # удаление []
print ('Next-Hop:           ', list_ospf_route [4])
print ('Last update:        ', list_ospf_route [5])
print ('Outbound Interface: ', list_ospf_route [6])


#ad_metric = '[110/1045]'
#ad_metric.strip('[]')