def compute_z_values(string):
    n = len(string)
    z = [0] * n
    z[0] = n
    l, r = 0, 0

    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        
        while i + z[i] < n and string[z[i]] == string[i + z[i]]:
            z[i] += 1

        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1

    return z

def compute_r_values(pat):
    m = len(pat)
    r = {ch: -1 for ch in set(pat)}

    for i in range(m):
        r[pat[i]] = i

    return r

def compute_good_suffix(pat):
    m = len(pat)
    rev_pat = pat[::-1]
    z = compute_z_values(rev_pat)
    z.reverse()

    gs = [0] * (m + 1)
    mp = [0] * (m + 1)
    mp[0] = m
    
    for i in range(1, m):
        mp[i] = max(z[:m - i])
        j = m - z[i]
        gs[j] = i
    
    return gs, mp

def BoyerMoore(text, pat):
    m = len(pat)
    n = len(text)
    r = compute_r_values(pat)
    gs, mp = compute_good_suffix(pat)
    results = []

    current = 0
    while current + m <= n:
        mismatch = -1
        for i in range(m - 1, -1, -1):
            if pat[i] != text[current + i]:
                mismatch = i
                break
        else:
            results.append(current)
        
        bc_shift = mismatch - r.get(text[current + mismatch], -1)
        
        if mismatch >= 0:   
            mp_shift = m - gs[mismatch + 1] - 1 if gs[mismatch + 1] > 0 else m - mp[mismatch + 1] - 1
        else:
            mp_shift = m - mp[1]
        
        shift = max(bc_shift, mp_shift)
        current += shift
  
    return results

# print(BoyerMoore("nwmpnphvphtkaphdaafphpevfphpaephigxgphllnphphvfvfp", "p"))
