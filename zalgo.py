def zalgo(string: str) -> list[int]:
    zvalues = [0 for _ in string]
    lr = [[0,0] for _ in string]
    
    zvalues[0] = len(string)
    
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
       
    
        # case 1
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
        
        # case 2
        elif i <= lr[i][1]:
    
            if zvalues[i - lr[i][0]] < lr[i][1] - i + 1:
                zvalues[i] = zvalues[i - lr[i][0]]
                
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
    print(zvalues, lr)    
                

def pat_match(txt : str, pat : str):
    string = pat + "$" + txt
    zvalues = zalgo(string)
    matches = []
    for i in range(len(pat), len(zvalues)):
        if zvalues[i] >= len(pat):
            matches += [i - len(pat) - 1]
            
    print(matches)
    
    

