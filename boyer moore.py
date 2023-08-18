from zalgo import zalgo


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
    
    suffix_pos = {}
    # for i in range(len(z)):
    #     if z[i] not in suffix_pos.keys():
    #         suffix_pos[z[i]] = [i]
    #     else:
    #         suffix_pos[z[i]] += [i]

    gs = [0 for _ in range(m+1)]  
    for i in range(m-1):
        j = m - z[i] 
        gs[j] = i
    
    mp = [0 for _ in range(m+1)]
    mp[0] = m
    
    for i in range(1, m):
        mp[i] = max(z[:m - i])
        
    return suffix_pos , z, gs, mp


def BoyerMoore(text: str, pat: str):
    n = 0
    text = text
    pat = pat
    r = r_values(pat)
    suffix_pos, z, gs, mp = good_suffix(pat)
    m = len(pat)
    start, stop = 0,-1

    comparisons = 0
            
    print(suffix_pos)
    print("z: ", z)
    print("gs: ", gs)
    print("mp: ", mp)
    results = []

    shift = 0
    current = 0
    while current + m <= len(text):
        print(text)
        print(" " * current + pat)
        mismatch = -1
        # for i in range(m - 1, -1, -1):
        ran = [_ for _ in range(m-1, stop, -1)] + [_ for _ in range(start - 1, -1, -1)]
        for i in ran:
            comparisons += 1
            if pat[i] != text[current + i]:
                mismatch = i 
                break
        else:  # This runs if the loop completes without a break (i.e., a match is found)
            results.append(current)
        
        bc_shift = mismatch - r[mismatch][ord(text[current + mismatch]) - ord('!')]
        
        mp_shift = 0
        if mismatch >= 0:   
            if gs[mismatch + 1] > 0: 
                mp_shift = m - gs[mismatch + 1] - 1
                start = gs[mismatch + 1] - m + mismatch
                stop = gs[mismatch + 1]
            else:
                mp_shift = m - mp[mismatch + 1]
                start = 0
                stop = mp[mismatch + 1]
        else: 
            mp_shift = m - mp[1] 
            start = 0
            stop = mp[1]
        
        
        if mp_shift >= bc_shift:
            shift = mp_shift
        else: 
            shift = start = stop = bc_shift

        current += shift
  
        n += 1
    print(n, "shifts")
    print(comparisons, "comparisons")
    
    return results
    


print(BoyerMoore("babaabcaaabcacvabvabasbabaabcacvabvababaabcacvabvabasbabaabcacvabvababaabcacvabvabasbabaabcacvabvababaabcacvabvabasbabaabcacvabvababaabcacvabvabasbabaabcacvabvababaabcacvabvabasbabaabcacvabvababcvabvabasbabaabcacvabvabab", "babaabcacvabvabab"))