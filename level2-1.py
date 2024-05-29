import os
import re
from collections import Counter

def readFile(fileName):
    with open(fileName, 'r') as file:
        return file.read().lower()

def getWordFrequencies(text, topN):
    words = re.findall(r'\b\w+\b', text)
    counter = Counter(words)
    return counter.most_common(topN)

def displayFrequencies(frequencies, label):
    print(f"{label}  ")
    for word, count in frequencies:
        print(f"{word}: {count}")

def getMatchingFrequencies(qFrequencies, kFrequencies):
    qWords = set(word for word, count in qFrequencies)
    return [(word, count) for word, count in kFrequencies if word in qWords]

def main():
    textNum = int(input("Enter the number of known texts: "))
    print()
    
    # Read and process questioned.txt
    questionedText = readFile('questioned.txt')
    increment = 20
    currentRange = increment
    qFrequencies = getWordFrequencies(questionedText, currentRange)
    
    while True:
        displayFrequencies(qFrequencies, f"Q frequence word 1～{currentRange}")
        print()
        
        for i in range(1, textNum + 1):
            knownText = readFile(f'known{i}.txt')
            kFrequencies = getWordFrequencies(knownText, currentRange)
            displayFrequencies(kFrequencies, f"known{i} frequence word 1～{currentRange}")
            
            matchingFrequencies = getMatchingFrequencies(qFrequencies, kFrequencies)
            print()
            print(f"Matching frequencies in known{i} for Q frequence word 1～{currentRange}:")
            displayFrequencies(matchingFrequencies, "")
            print()
        
        continueInput = input("Do you want to continue? ").strip().lower()
        if continueInput == 'yes':
            currentRange += increment
            qFrequencies = getWordFrequencies(questionedText, currentRange)
        else:
            break

    displayFrequencies(qFrequencies, f"Q frequence word 1～{currentRange}")

    # Find the best matching known file
    bestMatchCount = 0
    bestMatchIndex = None
    for i in range(1, textNum + 1):
        knownText = readFile(f'known{i}.txt')
        kFrequencies = getWordFrequencies(knownText, currentRange)
        matchingFrequencies = getMatchingFrequencies(qFrequencies, kFrequencies)
        if len(matchingFrequencies) > bestMatchCount:
            bestMatchCount = len(matchingFrequencies)
            bestMatchIndex = i

    if bestMatchIndex is not None:
        bestMatchText = readFile(f'known{bestMatchIndex}.txt')
        bestMatchFrequencies = getWordFrequencies(bestMatchText, currentRange)
        displayFrequencies(bestMatchFrequencies, f"known{bestMatchIndex} frequence word 1～{currentRange}")

        print()
        if qFrequencies == bestMatchFrequencies:
            print(f"questioned.txt is known{bestMatchIndex}.txt.")
        else:
            print("questioned.txt doesn't exist in known.txt list")
    else:
        print("questioned.txt doesn't exist in known.txt list")

if __name__ == "__main__":
    main()
