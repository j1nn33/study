# codewars 
# 7kyu
# List Filtering
"""
In this kata you will create a function that takes a list 
of non-negative integers and strings and returns a new 
list with the strings filtered out.

filter_list([1,2,'a','b']) == [1,2]
filter_list([1,'a','b',0,15]) == [1,0,15]
filter_list([1,2,'aasf','1','123',123]) == [1,2,123]
"""
def filter_list(l):
    final_list=[]
    for a in l:
        if type(a) is not str:
            final_list.append(a)
    return (final_list)
  

if __name__ == "__main__":
    if filter_list([1,2,'a','b']) == [1,2]:
        print ('Test 1 - OK   [1,2,\'a\',\'b\'] == [1,2]')
    else:
        print ('Test 1 - FALL [1,2,\'a\',\'b\'] == [1,2]')
    
    if filter_list([1,'a','b',0,15]) == [1,0,15]:
        print ('Test 2 - OK   [1,\'a\',\'b\',0,15] == [1,0,15]')
    else:
        print ('Test 2 - FALL [1,\'a\',\'b\',0,15] == [1,0,15]')
    
    if filter_list([1,2,'aasf','1','123',123]) == [1,2,123]:
        print ('Test 3 - OK   [1,2,\'aasf\',\'1\',\'123\',123] == [1,2,123]')
    else:
        print ('Test 3 - FALL [1,2,\'aasf\',\'1\',\'123\',123] == [1,2,123]')
        
    
        
