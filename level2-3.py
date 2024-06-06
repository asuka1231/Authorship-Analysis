import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import math
import chardet

nltk.download('punkt')

# Function to read a text file and tokenize its content
def load_and_tokenize(filename):
    with open(filename, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            Encoding = result['encoding']
    with open(filename, 'r', encoding=Encoding, errors='replace') as file:
        text = file.read().lower()
    tokens = word_tokenize(text)
    return Counter(tokens)

# Calculate loglikelihood
def loglikelihood(f1, f2, n1, n2):
    E1 = n1 * (f1 + f2) / (n1 + n2)
    E2 = n2 * (f1 + f2) / (n1 + n2)
    G2 = 2 * ((f1 * math.log(f1 / E1) if f1 > 0 else 0) + (f2 * math.log(f2 / E2) if f2 > 0 else 0))
    return G2

def show(results):
    for result in results:
        print(f"Word: {result[0]}, Target Freq: {result[1]}, Reference Freq: {result[2]}, LL: {result[3]:.2f}, Odds Ratio: {result[4]:.2f}")


def lookupKeyness(filepath1, filepath2):
    # Load and tokenize the corpora
    reference_freq = load_and_tokenize(filepath1)
    target_freq = load_and_tokenize(filepath2)

    # Total number of words in each corpus
    total_reference = sum(reference_freq.values())
    total_target = sum(target_freq.values())

    # Calculate loglikelihood and effect size for each word in the target corpus
    results = []
    for word in target_freq:
        ref_count = reference_freq[word]
        target_count = target_freq[word]
    
        # Loglikelihood, ll is float
        ll = loglikelihood(target_count, ref_count, total_target, total_reference)

        # Effect size (Odds Ratio)
        odds_ratio = (target_count / total_target) / (ref_count / total_reference) if ref_count > 0 else float('inf')
    
        results.append((word, target_count, ref_count, ll, odds_ratio))

    # Sort results by loglikelihood value
    results.sort(key=lambda x: x[3], reverse=True)
    show(results)

# main

file1 = 'ikkome.txt'
file2 = 'nikome.txt'
lookupKeyness(file1,file2)