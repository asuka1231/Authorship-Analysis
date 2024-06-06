import os
import shutil
import tkinter as tk
import re
import sys
from tkinter import ttk
from tkinter import filedialog, simpledialog, messagebox
from datetime import datetime
from collections import Counter
import chardet


# ディレクトリの作成
def create_directory(entry, file_listbox=None):
    directory_path = entry.get()
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        messagebox.showinfo("Success", f"Directory: '{directory_path}' created")
        if file_listbox:
            file_listbox.insert(tk.END, f"Directory created: {directory_path}")
    else:
        messagebox.showinfo("Information", f"Directory: '{directory_path}' already exists")

# ファイルの選択
def select_files(entry, file_listbox):
    directory_path = entry.get()
    if not directory_path or not os.path.exists(directory_path):
        messagebox.showerror("Error", "Please enter a valid directory path and create it first.")
        return
    selected_files = filedialog.askopenfilenames(title="Select datasets")
    for select_file in selected_files:
        if select_file:
            dest_file = os.path.join(directory_path, os.path.basename(select_file))
            shutil.copy(select_file, dest_file)
            file_listbox.insert(tk.END, dest_file)
            global selected_files_global
            selected_files_global.append(select_file)  # 選択されたファイルをグローバルリストに追加

# ファイルの処理
def load_files(directory):
    files = os.listdir(directory)
    return files

####################################################
# データの処理(search)
def searcher(file, keyword, type_search, results):
    if type_search == "word token":
        for line in file:
            words = line.strip().split()
            for i, word in enumerate(words):
                if keyword in word:
                    start = max(0, i - 10)
                    end = min(len(words), i + 11)
                    context_words = words[start:end]
                    highlighted_context = ' '.join([f'"{word}"' if keyword in word else word for word in context_words])
                    results.append(highlighted_context)
                    break
    elif type_search == "lemma":
        pass  # 省略
    elif type_search == "POS":
        pass  # 省略
    elif type_search == "n-gram":
        pass  # 省略
    elif type_search == "regex":
        pass  # 省略
    else:
        pass  # 省略

# "Search"での処理
def on_search(selected_files, entry, file_listbox):
    directory_path = entry.get()
    selected_search_type = search_type.get()  # 選択された検索タイプを取得
    root3.withdraw()  # ウィンドウを隠す
    keyword = simpledialog.askstring("Keyword", "Search using Key Word in Context")
    if not keyword:
        root3.destroy()
        return
    
    results = []
    for select_file in selected_files:
        if select_file:
            dest_file = os.path.join(directory_path, os.path.basename(select_file))
            shutil.copy(select_file, dest_file)
            file_listbox.insert(tk.END, dest_file)
            # ファイルを読み込み、searcher関数を呼び出す
            with open(dest_file, 'r', encoding='utf-8') as file:
                searcher(file, keyword, selected_search_type, results)

    # 結果をファイルに保存
    storeFile(results, selected_search_type)

    root3.destroy()  # 全ての処理が終わった後にウィンドウを完全に閉じる


####################################################
# Compare
def readFile(fileName):
    selected_compare_type = compare_type.get()  # 選択された比較タイプを取得
    if selected_compare_type == "Q vs K":
        with open(fileName, 'r', encoding='utf-8') as file:
            return file.read().lower()
    elif selected_compare_type == "K vs K":
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

def getWordFrequencies(text, topN):
    selected_compare_type = compare_type.get()  # 選択された比較タイプを取得
    if selected_compare_type == "Q vs K":
        words = re.findall(r'\b\w+\b', text)
        counter = Counter(words)
        return counter.most_common(topN)
    elif selected_compare_type == "K vs K":
        words = re.findall(r'\b\w+\b', text)
        return Counter(words)

def displayFrequencies(frequencies, label):
    selected_compare_type = compare_type.get()  # 選択された比較タイプを取得
    if selected_compare_type == "Q vs K":
        print(f"{label}  ")
        for word, count in frequencies:
            print(f"{word}: {count}")
    elif selected_compare_type == "K vs K":
        all_words = sorted(set(word for freqs in frequencies for word in freqs))
        dash_groups = {0: [], 1: [], 2: []}

        for word in all_words:
            counts = [freqs[word] if freqs[word] > 0 else '-' for freqs in frequencies]
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
            print("Word: " + ", ".join(label))

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

# Q vs Kで使用
def getMatchingFrequencies(qFrequencies, kFrequencies):
    selected_compare_type = compare_type.get()  # 選択された比較タイプを取得
    qWords = set(word for word, count in qFrequencies)
    return [(word, count) for word, count in kFrequencies if word in qWords]

# K vs Kで使用
def calculateSimilarity(freq1, freq2):
    common_words = set(freq1.keys()).union(set(freq2.keys()))
    total_words = len(common_words)
    if total_words == 0:
        return 0.0
    
    similarity_score = sum(min(freq1[word], freq2[word]) for word in common_words) / sum(max(freq1[word], freq2[word]) for word in common_words)
    return similarity_score

# "Compare"での処理
def on_compare():
    selected_compare_type = compare_type.get()  # 選択された比較タイプを取得
    root3.withdraw()  # ウィンドウを隠す

    if selected_compare_type == "Q vs K":
        textNum = simpledialog.askinteger("Input", "Enter the number of known texts:")
        if textNum is None:
            messagebox.showerror("Error", "You must enter a number.")
            return

        # Read and process questioned.txt
        questionedText = readFile('questioned.txt')
        increment = 20
        currentRange = increment
        qFrequencies = getWordFrequencies(questionedText, currentRange)

        while True:
            displayFrequencies(qFrequencies, f"Q frequency word 1～{currentRange}")
        
            for i in range(1, textNum + 1):
                knownText = readFile(f'known{i}.txt')
                kFrequencies = getWordFrequencies(knownText, currentRange)
                displayFrequencies(kFrequencies, f"known{i} frequency word 1～{currentRange}")
            
                matchingFrequencies = getMatchingFrequencies(qFrequencies, kFrequencies)
                displayFrequencies(matchingFrequencies, f"Matching frequencies in known{i} for Q frequency word 1～{currentRange}")
        
            continueInput = simpledialog.askstring("Continue", "Do you want to continue? (yes/no)").strip().lower()
            if continueInput == 'yes':
                currentRange += increment
                qFrequencies = getWordFrequencies(questionedText, currentRange)
            else:
                break

        displayFrequencies(qFrequencies, f"Q frequency word 1～{currentRange}")

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
            displayFrequencies(bestMatchFrequencies, f"known{bestMatchIndex} frequency word 1～{currentRange}")

            if qFrequencies == bestMatchFrequencies:
                messagebox.showinfo("Result", f"questioned.txt is known{bestMatchIndex}.txt.")
            else:
                messagebox.showinfo("Result", "questioned.txt doesn't exist in known.txt list")
        else:
            messagebox.showinfo("Result", "questioned.txt doesn't exist in known.txt list")

    ###############################################

    elif selected_compare_type == "K vs K":
        textNum = simpledialog.askinteger("Enter the number of known texts: ")
        if textNum is None:
            messagebox.showerror("Error", "You must enter a number.")
            return
    
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


    root3.destroy()  # 全ての処理が終わった後にウィンドウを完全に閉じる

# 結果を保存
def storeFile(results, type_search, filename=None):
    if filename is None:
        # 現在の日付を取得
        current_date = datetime.now().strftime("%Y%m%d")
        # ファイル名を設定
        filename = f"{type_search}_{current_date}_results.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(result + "\n")

    print(f"Results saved to {filename}")  # ファイル名を出力して確認


def main():
    try:
        global root1, root2, root3, type_command, selected_files_global, file_listbox, entry

        root1 = tk.Tk()
        root1.title("Authorship-Analysis Application")
        root1.geometry("600x600")

        label = tk.Label(root1, text="Directory Creation (Enter the directory path)")
        label.pack(pady=10)

        entry = tk.Entry(root1, width=50)
        entry.pack(pady=5)

        file_listbox = tk.Listbox(root1, width=50, height=10)
        file_listbox.pack(pady=10)

        selected_files_global = []  # グローバルリストの初期化

        create_dir_button = tk.Button(root1, text="Create Directory", command=lambda: create_directory(entry, file_listbox))
        create_dir_button.pack(pady=10)

        select_files_button = tk.Button(root1, text="Select Files", command=lambda: select_files(entry, file_listbox))
        select_files_button.pack(pady=10)

        next_button = tk.Button(root1, text="Next", command=lambda: show_next_window(root1, root2))
        next_button.pack(pady=10)

        ####################################################

        root2 = tk.Toplevel(root1)
        root2.title("Authorship-Analysis Application - Step 2")
        root2.geometry("600x400")
        tk.Label(root2, text="Command Type").pack(pady=10)
        type_command_list = ["Compare(ex. Q vs K, K vs K, keyness tab)", "Search(ex. word token, lemma, etc)"]
        type_command = ttk.Combobox(root2, values=type_command_list)
        type_command.pack(pady=5)
        type_command.bind("<<ComboboxSelected>>", on_command_type_change)
        root2.withdraw()

        next_button2 = tk.Button(root2, text="Next", command=lambda: show_next_window(root2, root3))
        next_button2.pack(pady=20)

        ####################################################

        root3 = tk.Toplevel(root2)
        root3.title("Authorship-Analysis Application - Step 3")
        root3.geometry("600x400")
        root3.withdraw()

        root1.mainloop()
        root1.destroy()  # GUIを閉じる

    except KeyboardInterrupt:
        print("Program interrupted by user.")
        
    finally:
        root1.destroy()  # アプリケーション・ウィンドウを閉じる
        sys.exit()       # プログラムを終了

# コマンド選択
def on_command_type_change(event):
    global compare_label, compare_type, compare_button, search_label, search_type, search_button

    # Clear the existing widgets in root3
    for widget in root3.winfo_children():
        widget.destroy()

    if type_command.get() == "Compare(ex. Q vs K, K vs K, keyness tab)":
        compare_label = tk.Label(root3, text="Compare Type")
        compare_label.pack(pady=10)
        compare_type_list = ["Q vs K", "K vs K", "keyness tab"]
        compare_type = ttk.Combobox(root3, values=compare_type_list)
        compare_type.pack(pady=5)

        compare_button = tk.Button(root3, text="Start Compare", command=on_compare)
        compare_button.pack(pady=20)

    elif type_command.get() == "Search(ex. word token, lemma, etc)":
        search_label = tk.Label(root3, text="Search Type")
        search_label.pack(pady=10)
        search_type_list = ["word token", "lemma", "POS", "n-gram", "regex"]
        search_type = ttk.Combobox(root3, values=search_type_list)
        search_type.pack(pady=5)

        search_button = tk.Button(root3, text="Start Search", command=lambda: on_search(selected_files_global, entry, file_listbox))
        search_button.pack(pady=20)


# GUIのウィンドウ切り替え
def show_next_window(current_root, next_root):
    current_root.withdraw()
    next_root.deiconify()


main()
