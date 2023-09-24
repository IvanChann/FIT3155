from q1 import generate_bwt

ALPHABET_SIZE = 127 - 36

def generate_ranks(bwt):
    ranks = [-1] * ALPHABET_SIZE
    occurrences = [0] * ALPHABET_SIZE
    
    for char in bwt:
        occurrences[ord(char) - ord('$')] += 1
    
    total = 0
    ranks[0] = 0
    for i in range(ALPHABET_SIZE):
        if occurrences[i] == 0:
            continue
        ranks[i] = total
        total += occurrences[i]
        
    return ranks
    

def nOccurrences(char, L):
    return L.count(char) 
    
def bwt_pat_match(string, pat):
    n = len(string) + 1
    bwt = generate_bwt(string)
    rank = generate_ranks(bwt)
    
    sp = 0
    ep = n - 1
    
    for i in range(len(pat)-1, -1, -1):
        if sp > ep:
            break
        
        sp = rank[ord(pat[i]) - ord("$")] + nOccurrences(pat[i], bwt[:sp])
        ep = rank[ord(pat[i]) - ord("$")] + nOccurrences(pat[i], bwt[:ep+1]) - 1
        print(pat[i], sp, ep)
    multiplicity = ep - sp + 1
    
    return multiplicity

def bwt_approx_pat_match(string, pat, max_ham):
    n = len(string) + 1
    bwt = generate_bwt(string)
    rank = generate_ranks(bwt)
    
    sp = 0
    ep = n - 1
    
    matches = [0] * (max_ham + 1)
    
    def search(i, sp, ep, ham = 0):
        if ham > max_ham:
            return
        if i < 0:
            matches[ham] += ep - sp + 1
            return
        
        for j in range(1, ALPHABET_SIZE):
            sp_ = rank[j] + nOccurrences(chr(j + ord("$")), bwt[:sp])
            ep_ = rank[j] + nOccurrences(chr(j + ord("$")), bwt[:ep+1]) - 1
            
            # print(chr(j + ord("$")), i, sp_, ep_, ham, rank[j])
            
            if sp <= ep:
                if j == ord(pat[i]) - ord("$"):
                    search(i - 1, sp_, ep_, ham)
                else:
                    search(i - 1, sp_, ep_, ham + 1)
    
    search(len(pat) - 1, sp, ep)
    return matches
            
        
            
    
        
        
    
string = "woolloomooloo"
pat = "olloo"


# print(bwt_pat_match(string, pat))

print(bwt_approx_pat_match(string, pat, 5))