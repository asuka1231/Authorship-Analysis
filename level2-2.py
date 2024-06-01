import re
from collections import Counter
import chardet

def readFile(fileName):
    with open(fileName, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        print(f"Detected encoding for {fileName}: {encoding}")

        encodings_to_try = [encoding, 'utf-8', 'shift_jis', 'euc-jp', 'cp932']

        for enc in encodings_to_try:
            try:
                text = raw_data.decode(enc, errors='ignore')
                print(f"Successfully decoded {fileName} with encoding: {enc}")
                return text.lower()
            except (UnicodeDecodeError, TypeError) as e:
                print(f"Failed to decode {fileName} with encoding: {enc} due to {e}")

        raise UnicodeDecodeError(f"Unable to decode {fileName} with any of the tried encodings.")

def getWordFrequencies(text):
    words = re.findall(r'\b\w+\b', text)
    return Counter(words)

def displayFrequencies(frequencies_list, labels):
    all_words = sorted(set(word for freqs in frequencies_list for word in freqs))
    dash_groups = {0: [], 1: [], 2: []}

    for word in all_words:
        counts = [freqs[word] if freqs[word] > 0 else '-' for freqs in frequencies_list]
        dash_count = counts.count('-')
        if dash_count in dash_groups:
            dash_groups[dash_count].append((word, counts))
    
    messages = {
        0: "The words that occur in ALL texts",
        1: "The words that occur in all but one text",
        2: "The words that occur in all but two texts"
    }

    for dash_count, group in dash_groups.items():
        print(f"\n{messages[dash_count]}:")
        if not group:
            print("No words in this category.")
            continue
        print("Word: " + ", ".join(labels))

        count = 0
        row = []
        for word, counts in group:
            counts_str = [str(count) for count in counts]
            row.append(f"{word}: " + ", ".join(counts_str))
            count += 1
            if count % 5 == 0:
                print(" | ".join(row))
                row = []

        if row:  # 最後に残った行を出力
            print(" | ".join(row))

def calculateSimilarity(freq1, freq2):
    common_words = set(freq1.keys()).union(set(freq2.keys()))
    total_words = len(common_words)
    if total_words == 0:
        return 0.0
    
    similarity_score = sum(min(freq1[word], freq2[word]) for word in common_words) / sum(max(freq1[word], freq2[word]) for word in common_words)
    return similarity_score

def main():
    textNum = int(input("Enter the number of known texts: "))
    print()
    
    knownFrequencies = []
    labels = []
    
    # Read and process known files
    for i in range(textNum):
        fileName = input(f"Enter the name of text file {i+1}: ")
        labels.append(fileName)
        try:
            knownText = readFile(fileName)
            knownFrequencies.append(getWordFrequencies(knownText))
        except UnicodeDecodeError as e:
            print(f"Error: {e}")
            print(f"Failed to read file {fileName}. Exiting program.")
            return

    displayFrequencies(knownFrequencies, labels)
    
    # Calculate and display similarity scores between all pairs of known texts
    print("\nSimilarity Scores:")
    for i in range(textNum):
        for j in range(i + 1, textNum):
            similarity = calculateSimilarity(knownFrequencies[i], knownFrequencies[j])
            print(f"Similarity between {labels[i]} and {labels[j]}: {similarity:.2%}")
            if similarity > 0.8:
                print(f"Text {labels[i]} and Text {labels[j]} have a similarity of more than 80%. It is assumed that they were written by the same author.")

if __name__ == "__main__":
    main()

# This program is based on level2-1.py and was created using ChatGPT.
