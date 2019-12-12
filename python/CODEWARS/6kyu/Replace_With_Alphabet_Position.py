# codewars 
# 6kyu
# Replace With Alphabet Position
"""
In this kata you are required to, given a string, replace every letter with its position in the alphabet.

If anything in the text isn't a letter, ignore it and don't return it.

"a" = 1, "b" = 2, etc.

Example
alphabet_position("The sunset sets at twelve o' clock.")
Should return "20 8 5 19 21 14 19 5 20 19 5 20 19 1 20 20 23 5 12 22 5 15 3 12 15 3 11" (as a string)
"""
import string


def alphabet_position(text):
    res_list = []
    a = [i for i in range(1,len(string.ascii_lowercase)+1)]
    c = string.ascii_lowercase
    res_dict = dict(zip(c, a))
    # {'a': 1, 'b': 2, ... 'z': 26}
    for char in text.lower():
        if char in res_dict:
            res_list.append(str(res_dict[char]))
    
    result_str = ' '.join(res_list)
    return result_str


if __name__ == "__main__":

    
    if alphabet_position("Abc") == "1 2 3":
        print ('Test 1 - OK   ')
    else:
        print ('Test 1 - FALL ')
    
    if alphabet_position("The sunset sets at twelve o' clock.") == "20 8 5 19 21 14 19 5 20 19 5 20 19 1 20 20 23 5 12 22 5 15 3 12 15 3 11":
        print ('Test 2 - OK   ')
    else:
        print ('Test 2 - FALL ')
    
    if alphabet_position("The narwhal bacons at midnight.") == "20 8 5 14 1 18 23 8 1 12 2 1 3 15 14 19 1 20 13 9 4 14 9 7 8 20":
        print ('Test 3 - OK   ')
    else:
        print ('Test 3 - FALL ')
    
   