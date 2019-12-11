# codewars 
# 6kyu
# Sum of Digits / Digital Root
"""
In this kata, you must create a digital root function.

A digital root is the recursive sum of all the digits in a number.
Given n, take the sum of the digits of n. If that value has more 
than one digit, continue reducing in this way until a single-digit
number is produced. This is only applicable to the natural numbers.

Here's how it works:

digital_root(16)
=> 1 + 6
=> 7

digital_root(942)
=> 9 + 4 + 2
=> 15 ...
=> 1 + 5
=> 6

digital_root(132189)
=> 1 + 3 + 2 + 1 + 8 + 9
=> 24 ...
=> 2 + 4
=> 6

digital_root(493193)
=> 4 + 9 + 3 + 1 + 9 + 3
=> 29 ...
=> 2 + 9
=> 11 ...
=> 1 + 1
=> 2
"""
def digital_root(n):
    temp_str=str(n)
    x = 0
    while len (temp_str) > 1:
        x=0
        for i in range (len(temp_str)):
            x  += int (temp_str[i])
        temp_str = str(x)
      
    return(x)
    
  

if __name__ == "__main__":
    if digital_root(16) == 7:
        print ('Test 1 - OK   ')
    else:
        print ('Test 1 - FALL ')
    
    if digital_root(942) == 6:
        print ('Test 2 - OK   ')
    else:
        print ('Test 2 - FALL ')
    
    if digital_root(132189) == 6:
        print ('Test 3 - OK   ')
    else:
        print ('Test 3 - FALL ')
    if digital_root(493193) == 2:
        print ('Test 4 - OK   ')
    else:
        print ('Test 4 - FALL ')
    
