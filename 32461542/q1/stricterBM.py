import sys

def zalgo(string: str) -> list[int]:
    zvalues = [0 for _ in string] # initalize z values to 0 
    lr = [[0,0] for _ in string] # 2D array for left and rightmost positions
    
    zvalues[0] = len(string) 
    
    # compute z values from index 1
    for i in range(1, len(string)):
        # base case
        if i == 1:
            for m in range(i, len(string)):
                if string[m] == string[m-i]:
                    zvalues[i] += 1
                else: 
                    break
            
            if zvalues[i] > 0: 
                lr[i] = [i, zvalues[i] + i - 1]
                
            continue
       
    
        # case 1: i is outside of any computed z-box
        if i > lr[i][1]:
            q = 0
            for j in range(i, len(string)):
                if string[j] == string[j-i]:
                    zvalues[i] += 1
                    if j == len(string) - 1:
                        q = j + 1
                else:
                    q = j
                    break
                    
            if zvalues[i] > 0 and q > 0:
                lr[i][1] = q-1
                lr[i][0] = i
        
        # case 2: i is within a computed z-box
        elif i <= lr[i][1]:
            
            # case 2a
            if zvalues[i - lr[i][0]] < lr[i][1] - i + 1:
                zvalues[i] = zvalues[i - lr[i][0]]
                
            # case 2b
            elif zvalues[i - lr[i][0]] >= lr[i][1] - i + 1:
                q = 0
                if lr[i][1] == len(string) - 1:
                    q = len(string) 
                    
                for k in range(lr[i][1], len(string)):
                    if string[k] == string[k - i]:
                        continue
                    q = k
                    
                zvalues[i] = q - i
                lr[i][1] = k
                lr[i][0] = i
                
    return zvalues

# generates right most occurreneces of each character in pat
def r_values(pat: str) -> list:
    m = len(pat)
    r = [-1 for _ in range(ord('!'), ord('~') + 1)] # initializing list for each printable ASCII character
    result = []

    # loop through and store right more occurrence of each character in pat
    for i in range(m):
        r[ord(pat[i]) - ord('!')] = i
        result.append(r.copy())
    return result

# preproccesses the gs and mp arrays
def good_suffix(pat: str):
    m = len(pat)
    
    # computing the reversed z values
    z = zalgo(pat[::-1])
    z.reverse()
    z[-1] = 0

    
    gs = [0 for _ in range(m+1)]  
    gs_extended = []
    
    # loop through and stores each iteration of the good suffix array, allowing us to access all instances of the suffix in pat
    for i in range(m - 1):
        j = m - z[i] 
        gs[j] = i
        gs_extended.append(gs.copy())
    gs_extended.append(gs.copy())
    
    # computing the matched prefix values
    mp = [0 for _ in range(m+1)]
    mp[0] = m
    for i in range(1, m):
        mp[i] = max(z[:m - i])
        
    return z, gs_extended, mp


def BoyerMoore(text: str, pat: str):
    r = r_values(pat)
    z, gs, mp = good_suffix(pat)
    m = len(pat)
    start, stop = 0, 0  # variables for skipping previously compared characters
    
    results = []
    shift = 0 # value to shift by
    current = 0 # current index of text
    
    # traversing the text until the end is reached
    while current + m <= len(text):
        # print(text)
        # print(" " * current + pat)
        
        mismatch = -1

        # right to left scanning, skipping over pat[start:stop]
        
        for i in [_ for _ in range(m-1, stop, - 1)] + [_ for _ in range(start, -1, -1)]:
            # if mismatch found
            if pat[i] != text[current + i]:
                mismatch = i 
                break
            
        else:  # if loop doesnt break then match is found
            results.append(current)

        
        bc_shift = mismatch - r[mismatch][ord(text[current + mismatch]) - ord('!')] # using the r suffix to find the bad character shift
        gs_shift = 1
        
        # When the mismatch is at the last position of the pattern.
        if mismatch == m - 1:
            pass
        elif mismatch >= 0 : 
            if gs[m-1][mismatch + 1] > 0: # if a good suffix exists
                 
                edge = m - 1 # value used to find next good suffix to the left of edge
                while edge > 0:
                    # checking if the character immediately before the good suffixes matches with our current mismatch
                    # this is the extended rule
                    if pat[gs[edge][mismatch + 1] - m + mismatch + 1] == text[current + mismatch] or gs[edge][mismatch + 1] - m + mismatch + 1 == -1:
                        gs_shift = m - gs[edge][mismatch + 1] - 1
                        start = gs[edge][mismatch + 1] - m + mismatch + 1
                        stop = gs[edge][mismatch + 1] - 1
                        break
                    else:
                        # set edge to find next good suffix
                        edge = gs[edge][mismatch + 1] - 1
                else:
                    # if no such good suffix is found as per the extended rule, use the 'mp' array to set the shift
                    gs_shift = m - mp[mismatch + 1] - 1
                    start = 0
                    stop = mp[mismatch + 1] - 1
            else:
                # if no such good suffix is found as per the extended rule, use the 'mp' array to set the shift
                gs_shift = m - mp[mismatch + 1] - 1
                start = 0
                stop = mp[mismatch + 1] - 1
        else:
            # match is found
            gs_shift = m - mp[1] - 1
            start = stop = 0
        # Choose the maximum shift value between bad-character and good-suffix shifts.
        shift = max(gs_shift, bc_shift, 1)
        if bc_shift >= gs_shift:
            start = stop = 0
            
        # shift current by shift
        current += shift
        
    return results
    
if __name__ == "__main__":
    text_filename = sys.argv[1]
    pattern_filename = sys.argv[2]
    
    with open(text_filename, "r") as text_file:
        text = text_file.read().strip()

    with open(pattern_filename, "r") as pattern_file:
        pat = pattern_file.read().strip()

    results = BoyerMoore(text, pat)
    out_string = "\n".join(str(result + 1) for result in results)
    
    with open("output_stricterBM.txt", "w") as output:
        output.write(out_string)
        
