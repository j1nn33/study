import re
regular = "0/1, 0/3, 0/10"
#regular1 = re.search('\S\S\S', regular).group()
#regular2 = re.search('(\S+)\s+(\S+)', regular).group(2)
#reg = re.search('()',regular)
#regular1 = reg.group(1)
#regular2 = reg.group(2)
#regular1 = re.findall('0/[\d]', regular)

#print ('regular1 ', regular1)
#print ('regular2 ', regular2)

#match = re.search('(\S+)\s+([\w.]+)\s+.*', line)

reg_list = []
reg_list_1 = []
reg_list = re.findall('0/[\d]\D', regular)
#myString = '_'.join(myList)
#reg_list_1 = re.findall('0/[\d]', reg_list)
print (reg_list)
myString = '_'.join(reg_list)
print (myString)

reg_list = re.findall('0/[\d]', myString)

regular1=reg_list[0]+' '
regular2=reg_list[1]

print ('regular1 ', regular1)
print ('regular2 ', regular2)