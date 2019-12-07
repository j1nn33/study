# codewars 
# 6kyu
# Duplicate Encoder
"""
The goal of this exercise is to convert a string to a 
new string where each character in the new string is "(" 
if that character appears only once in the original string, or ")" 
if that character appears more than once in the original string.
Ignore capitalization when determining if a character is a duplicate.

"din"      =>  "((("
"recede"   =>  "()()()"
"Success"  =>  ")())())"
"(( @"     =>  "))((" 
"""

def duplicate_encode(word):
    final = []
    word=word.lower()             
    for i in word:
        k = 0         # counter for char
        j = 0         
        for j in range(0, len(word)):
            if i == word[j]:
                k +=1
        if k == 1:
            final.append ('(')
        else:
            final.append(')')

    final = ''.join(final)
    return final

if __name__ == "__main__":
    if duplicate_encode("din") == "(((":
        print ('Test 1 - OK   "din"      =>  "((("')
    else:
        print ('Test 1 - FALL "din"      =>  "((("')
    
    if duplicate_encode("recede") == "()()()":
        print ('Test 2 - OK   "recede"   =>  "()()()"')
    else:
        print ('Test 2 - FALL "recede"   =>  "()()()"')
    
    if duplicate_encode("Success") == ")())())":
        print ('Test 3 - OK   "Success"  =>  ")())())"')
    else:
        print ('Test 3 - FALL "Success"  =>  ")())())"')
        
    if duplicate_encode("(( @") == "))((":
        print ('Test 4 - OK   "(( @"     =>  "))(("')
    else:
        print ('Test 4 - FALL "(( @"     =>  "))(("')

        
