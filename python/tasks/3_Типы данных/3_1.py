
#    Обработать строку NAT таким образом, чтобы в имени интерфейса вместо
#    FastEthernet было GigabitEthernet.
#    NAT = "ip nat inside source list ACL interface FastEthernet0/1 overload"

NAT = "ip nat inside source list ACL interface FastEthernet0/1 overload"
print (NAT)
NEW_NAT = NAT.replace ('Fast', 'Gigabit')
print (NEW_NAT)
