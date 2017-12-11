d_keys = ['hostname', 'location', 'vendor', 'model', 'IOS', 'IP']
data = {'r1': ['london_r1', '21 New Globe Walk', 'Cisco', '4451', '15.4', '10.255.0.1'],
        'r2': ['london_r2', '21 New Globe Walk', 'Cisco', '4451', '15.4', '10.255.0.2'],
       'sw1': ['london_sw1', '21 New Globe Walk', 'Cisco', '3850', '3.6.XE', '10.255.0.101']
       }
london_co = {}
for k in data.keys():
    london_co[k] = dict(zip(d_keys,data[k]))
print(london_co)