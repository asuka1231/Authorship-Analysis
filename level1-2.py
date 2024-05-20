import re
from datetime import datetime

def Searcher(file, keyword, type_search, results):
    if type_search == "word token":
        # ファイルを行ごとに読み込み、キーワードが含まれている行をリストに追加する
        for line in file:
            words = line.strip().split()
            for i, word in enumerate(words):
                if keyword in word:
                    # キーワードの前後10語を取得
                    start = max(0, i - 10)
                    end = min(len(words), i + 11)
                    context_words = words[start:end]
                    # キーワードを赤色で表示
                    highlighted_context = ' '.join([f"\033[91m{word}\033[0m" if keyword in word else word for word in context_words])
                    results.append(highlighted_context)
                    break  # 一度キーワードを見つけたらその行の処理を終了

    elif type_search == "lemma":
        "lemma ver"
    elif type_search == "POS":
        "POS ver"
    elif type_search == "n-gram":
        "n-gram ver"
    elif type_search == "regex":
        "regex ver"
    else:
        "else"

# 使用例
type_search = input("Enter type of search (i.e. word token, lemma, POS, n-gram or regex)\n")

keyword = input("\nSearch using Key Word in Context\n")

data_num = int(input("\nInput the number of Datasets you wish to select.\n"))

loop = 0
results = []  # 結果を保存するリスト

print("")
while loop < data_num:
    loop += 1
    select_file = input("Select dataset\n")
    file = open(select_file,'r')
    with open(select_file, 'r', encoding='utf-8') as file:
         Searcher(file, keyword, type_search, results)

    if data_num - loop != 0:
        print("Please enter the remaining", data_num - loop, "times\n")
        

# 全てのファイルの読み込みが完了した後、結果をプリントする
print("\nresult: ")
for index, result in enumerate(results, 1):  # 1から始まるインデックスでenumerate
    print(f"{index}: {result}")


'''
# 以下の場合、色分けできない
# 現在の日時を取得
current_time = datetime.now()
formatted_time = current_time.strftime("%Y%m%d-%H%M")

# ファイル名を生成
filename = f"{formatted_time}-{keyword}.txt"

# 結果をファイルに保存
with open(filename, 'w', encoding='utf-8') as f:
    for index, result in enumerate(results, 1):
        f.write(f"{index}. {result}\n")

print(f"Results saved to {filename}")
'''