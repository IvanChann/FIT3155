import sys

ALPHABET_SIZE = 127 - 36

def preprocess_bwt(bwt):
    ranks = [-1] * ALPHABET_SIZE
    occurrences = [0] * ALPHABET_SIZE
    nOccurrences = [occurrences.copy()]
    
    for char in bwt:
        occurrences[ord(char) - ord('$')] += 1
        nOccurrences.append(occurrences.copy())
    
    total = 0
    ranks[0] = 0
    for i in range(ALPHABET_SIZE):
        if occurrences[i] == 0:
            continue
        ranks[i] = total
        total += occurrences[i]
    return ranks, nOccurrences
    


def bwt_approx_pat_match(bwt, pat, max_ham):
    n = len(bwt)
    rank, nOccurrences = preprocess_bwt(bwt)
    
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
            sp_ = rank[j] + nOccurrences[sp][j]
            ep_ = rank[j] + nOccurrences[ep+1][j] - 1
            
            if sp <= ep:
                if j == ord(pat[i]) - ord("$"):
                    search(i - 1, sp_, ep_, ham)
                else:
                    search(i - 1, sp_, ep_, ham + 1)
    
    search(len(pat) - 1, sp, ep)
    return matches
            
        
if __name__ == "__main__":
    bwt_filename = sys.argv[1]
    pat_filename = sys.argv[2]
    max_ham = sys.argv[3]

    with open(bwt_filename, "r") as bwt_file:
        bwt = bwt_file.read().strip()
        
    with open(pat_filename, "r") as pat_file:
        pat = pat_file.read().strip()

    matches = bwt_approx_pat_match(bwt, pat, int(max_ham))
    
    with open("output_hdbwtpm.txt", "w") as output:
        for d in range(len(matches)):
            output.write(f"d = {d}, nMatches = {matches[d]}\n")