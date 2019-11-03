# Наивный поиск подстроки в строке
"""
S="abacabadabacabafabacabadabacabadabacabafaba"
sub = "dabac"
"abaf"
"""
def equal (A,B):
    """ равенства строк O(N*M)
    """
    if len(A) != len(B):
        return False
        
    for i in range (len(A)):
        if A[i] != B[i]:
            return False

    return True

def search_sub_string(S, sub):
    for i in range (0, len(S)-len(sub)):
        if equal(S[i:i+len(sub)], sub):
            print (i)

S="abacabadabacabafabacabadabacabadabacabafaba"
sub = "dabac"

search_sub_string (S, sub)

