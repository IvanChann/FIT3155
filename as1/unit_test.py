import random
import regex as re
# from stricterBM import BoyerMoore
from boyeeemore import BoyerMoore
from bitwisepm import bitwisepm


import random
import string

def generate_random_text(length=1000):
    """Generate a random string of lowercase alphabets of given length."""
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def insert_pattern_into_text(text, pattern, num_instances=3):
    """Insert the pattern into the text at random locations."""
    for _ in range(num_instances):
        # Random index for pattern insertion
        index = random.randint(0, len(text) - len(pattern))
        text = text[:index] + pattern + text[index+len(pattern):]
    return text

def generate_test_text(pattern, text_length=1000, num_instances=3):
    """Generate a random text and insert the pattern into it at random locations."""
    random_text = generate_random_text(text_length)
    test_text = insert_pattern_into_text(random_text, pattern, num_instances)
    return test_text

def pattern_matches(pattern, text):
    """Return True if the regular expression pattern matches anywhere in the text, False otherwise."""
    return (re.findall(pattern, text, overlapped=True), BoyerMoore(text, pattern), bitwisepm(text, pattern))

def test_pattern_matching(pattern, text_length=100, num_trials=1000):
    """Test the pattern against random texts for the given number of trials."""
    

    for _ in range(num_trials):
        random_text = generate_test_text(pattern, text_length, random.randint(0,text_length//2))
        blockPrint()
        regex, bm, bw = pattern_matches(pattern, random_text)
        enablePrint()
        if len(regex) != len(bm):
            print("bm error", len(regex), len(bm))
            print(random_text)
            return True
        if len(regex) != len(bw):
            print("bw error", len(regex), len(bw))
            print(random_text)
            return True
    return False
            
import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def generateTest(pat_length, text_length):
    pattern = generate_random_text(pat_length)
    text = generate_test_text(pattern, text_length, random.randint(0,text_length//2))
    return pattern, text

# # Example usage:
# error = False
# tests = 0 
# while not error:
#     tests += 1
#     pattern = generate_random_text(10)
#     print(pattern)
#     error = test_pattern_matching(pattern, 50, 10)
# print("tests:", tests)

pattern, text = generateTest(2, 2000000)
with open("testtext.txt", "w") as output:
    output.write(text)
    
print(pattern)
