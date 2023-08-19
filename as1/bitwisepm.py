from bitarray import bitarray
import sys

"Performs bitwise pattern matching to find occurrences of pattern in text."
def bitwisepm(text: str, pat: str):
    
    m = len(pat)
    bitv = bitarray("1" * m) # initialize bitvector 
    delta = bitarray("0"  * m) # initialize delta
    
    result = []
    
    for j in range(len(text)):
        for i in range(m - 1, -1, -1):
            delta[m - i - 1] = 1 if text[j] != pat[i] else 0 # calculating delta values in place
        bitv = (bitv << 1) | delta # calculate next bitv
        if not bitv[0]: # if pattern found
            result.append(j - m + 1)
    return result

if __name__ == "__main__":
    text_filename = sys.argv[1]
    pattern_filename = sys.argv[2]
    
    with open(text_filename, "r") as text_file:
        text = text_file.read().strip()

    with open(pattern_filename, "r") as pattern_file:
        pat = pattern_file.read().strip()

    results = bitwisepm(text, pat)
    
    out_string = "\n".join(str(result + 1) for result in results)

    with open("output_bitwisepm.txt", "w") as output:
        output.write(out_string)