from collections import Counter
import re

def readFile(filePath):
    with open(filePath, 'r', encoding='utf-8') as file:
        return file.read()

def getTopWords(text, topN):
    words = re.findall(r'\b\w+\b', text.lower())
    wordCounts = Counter(words)
    return wordCounts.most_common(topN)

def displayCommonWords(qWordsSet, kTopWords):
    commonWords = [(word, count) for word, count in kTopWords if word in qWordsSet]
    for word, count in commonWords:
        print(f"{word}: {count}")
    print(f"Number of common words: {len(commonWords)}")
    return commonWords

def main():
    textNum = int(input("Enter the number of known text files(knownテキストの数を入力して下さい。): "))

    # Read questioned.txt
    qText = readFile('questioned.txt')

    # Variables to keep track of the results and continuation
    allCommonWordsCounts = []
    continueFlag = True
    start = 1
    increment = 20
    iterations = 0

    while continueFlag:
        iterations += 1
        end = iterations * increment
        qTopWords = getTopWords(qText, end)
        qTopWordsDict = dict(qTopWords[start-1:end])
        qTopWordsSet = set(qTopWordsDict.keys())

        print(f"\nQ frequence word top (questionedテキストの出現回数が多い単語トップ) {start}~{end}:")
        for word, count in qTopWords[start-1:end]:
            print(f"{word}: {count}")

        # Process each known file
        for i in range(1, textNum + 1):
            kText = readFile(f'known{i}.txt')
            kTopWords = getTopWords(kText, end)
            kTopWordsDict = dict(kTopWords[start-1:end])
            print(f"\nCommon words in known{i}.txt and Q frequence word {start}~{end} (questionedテキストとknown{i}テキストの出現回数が多い単語トップ{start}~{end}を比較し、その中で共通してる単語と、knownテキスト内での出現回数):")
            commonWords = displayCommonWords(qTopWordsSet, kTopWords[start-1:end])
            allCommonWordsCounts.append((i, len(commonWords), commonWords, kTopWordsDict))

        # Ask user if they want to continue
        continueInput = input("Do you want to continue? (yes/no): ").strip().lower()
        if continueInput != 'yes':
            continueFlag = False
        start = end + 1

    # Find the file with the most common words
    mostCommonK = max(allCommonWordsCounts, key=lambda x: x[1])

    print(f"\nMost common words found in known{mostCommonK[0]}.txt(最もquestionedテキストと共通してる単語が発見されたknownテキスト):")
    for word, count in mostCommonK[2]:
        print(f"{word}: {count}")

    print(f"Number of common words: {mostCommonK[1]}")

    # Check if the most common words are identical to the Q frequence words
    if qTopWordsDict == mostCommonK[3]:
        print(f"probably, questioned text is known{mostCommonK[0]}.txt.(多分questioned textはknown{mostCommonK[0]}.txtだろう。)")
    else:
        print("questioned text doesn't exist in known.txt list.(questioned textは読み込んだknownテキストには発見されなかった。)")

if __name__ == "__main__":
    main()