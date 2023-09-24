import sys

ALPHABET_SIZE = 127 - 36

# function to preprocess the ranks and nOccurrences
def preprocess_bwt(bwt):
    # initializing arrays
    ranks = [-1] * ALPHABET_SIZE
    occurrences = [0] * ALPHABET_SIZE
    nOccurrences = [occurrences.copy()] # list of list containing occurences before each index
    
    # counting occurrences
    for char in bwt:
        occurrences[ord(char) - ord('$')] += 1
        nOccurrences.append(occurrences.copy())
    
    total = 0
    ranks[0] = 0
    
    # populating ranks array
    for i in range(ALPHABET_SIZE):
        if occurrences[i] == 0:
            continue
        ranks[i] = total
        total += occurrences[i]
    return ranks, nOccurrences
    
# bwt approximate pattern matching
def bwt_approx_pat_match(bwt, pat, max_ham):
    n = len(bwt)
    # preproccesing arrays
    rank, nOccurrences = preprocess_bwt(bwt)
    
    sp = 0
    ep = n - 1
    
    matches = [0] * (max_ham + 1)
    
    # recursive search function
    def search(i, sp, ep, ham = 0):
        # if current hamming distance > max then break
        if ham > max_ham:
            return
        # if pattern is fully proccessed add the matches
        if i < 0:
            matches[ham] += ep - sp + 1
            return
        
        # loop through the alphabet to consider every character and every possible mismatch
        for j in range(1, ALPHABET_SIZE):
            sp_ = rank[j] + nOccurrences[sp][j]
            ep_ = rank[j] + nOccurrences[ep+1][j] - 1
            
            if sp <= ep:
                if j == ord(pat[i]) - ord("$"):
                    # if the character matches continue search with same hamming distance
                    search(i - 1, sp_, ep_, ham)
                else:
                    # increase hamming distance
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