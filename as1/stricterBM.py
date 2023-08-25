from zalgo import zalgo
import sys

# generate right most occurreneces
def r_values(pat: str) -> list:
    m = len(pat)
    r = [-1 for _ in range(ord('!'), ord('~') + 1)]
    result = []
    for i in range(m):
        r[ord(pat[i]) - ord('!')] = i
        result.append(r.copy())
    return result

def good_suffix(pat: str):
    m = len(pat)
    z = zalgo(pat[::-1])
    z.reverse()
    z[-1] = 0

    gsi = []
    gs = [0 for _ in range(m+1)]  
    for i in range(m - 1):
        j = m - z[i] 
        gs[j] = i
        gsi.append(gs.copy())
    
    mp = [0 for _ in range(m+1)]
    mp[0] = m
    
    for i in range(1, m):
        mp[i] = max(z[:m - i])
    return z, gsi, mp


def BoyerMoore(text: str, pat: str):
    n = 0
    text = text
    pat = pat
    r = r_values(pat)
    z, gs, mp = good_suffix(pat)
    m = len(pat)
    start, stop = 0, 0
    comparisons = 0
    
            
    # print(suffix_pos)
    # print("z: ", z)
    # print("gs: ", gs)
    # print("mp: ", mp)
    results = []

    shift = 0
    current = 0
    while current + m <= len(text):
        # print(text)
        # print(" " * current + pat)
        mismatch = -1
        for i in [_ for _ in range(m-1, stop - 1, - 1)] + [_ for _ in range(start, -1, -1)]:
            comparisons += 1
                  
            if pat[i] != text[current + i]:
                mismatch = i 
                break
        else:  # This runs if the loop completes without a break (i.e., a match is found)
            results.append(current)
        
        bc_shift = mismatch - r[mismatch][ord(text[current + mismatch]) - ord('!')]
        
        gs_shift = 0
        if mismatch == m-1:
            pass
        
        elif mismatch >= 0: 
            if gs[m-2][mismatch + 1] > 0:
                edge = m - 2
                while edge > 0:
                    if pat[gs[edge][mismatch + 1] - m + mismatch + 1] == text[current + mismatch]:
                        gs_shift = m - gs[edge][mismatch + 1] - 1
                        start = gs[edge][mismatch + 1] - m + mismatch
                        stop = gs[edge][mismatch + 1]
                        break
                    else:
                        edge = edge - m + mismatch + 1
                else:
                    gs_shift = m - mp[mismatch + 1]
                    start = 0
                    stop = mp[mismatch + 1]
            else:
                gs_shift = m - mp[mismatch + 1]
                start = 0
                stop = mp[mismatch + 1]
        else:  
            gs_shift = m - mp[1]
            start = 0
            stop = mp[1]
            
        if gs_shift >= bc_shift:
            shift = gs_shift
        else: 
            shift = stop = bc_shift
            start = stop - 1
            
            
        current += shift
        n += 1
    # print(n, "shifts")
    # print(comparisons, "comparisons")
    # print(len(results), "results")
    return results
    
# if __name__ == "__main__":
#     text_filename = sys.argv[1]
#     pattern_filename = sys.argv[2]
    
#     with open(text_filename, "r") as text_file:
#         text = text_file.read().strip()

#     with open(pattern_filename, "r") as pattern_file:
#         pat = pattern_file.read().strip()

#     results = BoyerMoore(text, pat)
#     out_string = "\n".join(str(result + 1) for result in results)
    
#     with open("output_stricterBM.txt", "w") as output:
#         output.write(out_string)
        
# print(BoyerMoore("aaacacabaaacaacabaaaaaacababaa", "acabaaaaaacaba"))