import os
import re #単語の取り出し
from collections import Counter #リストの各要素の数え上げ

def readFile(fileName):
    with open(fileName, 'r') as file:
        return file.read().lower() #全ての文字を小文字に変換してファイルを読み込む

def getWordFrequencies(text, topN):
    words = re.findall(r'\b\w+\b', text) #空白を目印に単語を取り出し、リストにして返す
    counter = Counter(words) #単語の数を数え上げる
    return counter.most_common(topN) #テキスト内での単語の出現回数上位20のリストを返す

def displayFrequencies(frequencies, label):
    print(f"{label}  ")
    for word, count in frequencies:
        print(f"{word}: {count}")

def getMatchingFrequencies(qFrequencies, kFrequencies): # kFrequenciesの単語リストを1つずつチェックし、その単語がもしqFrequenciesに含まれる単語だったら、戻り値配列に格納
    qWords = set(word for word, count in qFrequencies)
    return [(word, count) for word, count in kFrequencies if word in qWords]

def main():
    textNum = int(input("Enter the number of known texts: "))
    print()
    
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

    # 最もqFrequenciesの単語を含むknown.txtを見つける
    bestMatchCount = 0
    bestMatchIndex = None
    for i in range(1, textNum + 1):
        knownText = readFile(f'known{i}.txt')
        kFrequencies = getWordFrequencies(knownText, currentRange)
        matchingFrequencies = getMatchingFrequencies(qFrequencies, kFrequencies)
        if len(matchingFrequencies) > bestMatchCount:
            bestMatchCount = len(matchingFrequencies)
            bestMatchIndex = i

    # bestMatchIndexがNoneでなければ、known{bestMatchIndex}.txtのkFrequenciesを表示
    if bestMatchIndex is not None:
        bestMatchText = readFile(f'known{bestMatchIndex}.txt')
        bestMatchFrequencies = getWordFrequencies(bestMatchText, currentRange)
        displayFrequencies(bestMatchFrequencies, f"known{bestMatchIndex} frequence word 1～{currentRange}")

        print()
        
        # qFrequenciesとbestMatchFrequenciesの単語ランキングと、それぞれの出現回数が全く同じなら、それは同じテキストだろう。
        if qFrequencies == bestMatchFrequencies:
            print(f"questioned.txt is known{bestMatchIndex}.txt.")
        else:
            print("questioned.txt doesn't exist in known.txt list")
    else:
        print("questioned.txt doesn't exist in known.txt list")

if __name__ == "__main__":
    main()
