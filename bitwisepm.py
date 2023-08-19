from bitarray import bitarray

def bitwisepm(text: str, pat: str):
    m = len(pat)
    bitv = bitarray("1" * m)
    result = []
    
    for j in range(len(text)):
        delta = bitarray(1 if text[j] != pat[i] else 0 for i in range(m - 1, -1, -1))
        bitv = (bitv << 1) | delta
        if not bitv[0]:
            result.append(j - m + 1)
    return result

print(bitwisepm("abcab" , "abcabcabc"))
