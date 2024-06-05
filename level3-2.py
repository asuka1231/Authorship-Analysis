import chardet
import sqlite3
import time

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

# ユーザー入力
textName = input("Enter the File name of the txt file to which you want to add the footer: ")
userName = input("Enter the User name: ")
caseNumber = input("Enter the Case number: ")
caseName = int(input("Enter the Case name as an integer: "))

# ファイル読み込み
text = readFile(textName)

# 現在時刻取得
current_time = time.strftime('%Y/%m/%d %H:%M:%S')

# フッターを追加
footer = f"\n\n---\nUsername: {userName}\nCase number: {caseNumber}\nCase name: {caseName}\nDate: {current_time}"
text_with_footer = text + footer

# 新しいファイルに保存
output_file_name = f"output_{textName}"
with open(output_file_name, 'w', encoding='utf-8') as file:
    file.write(text_with_footer)

# データベースに保存
conn = sqlite3.connect('authorship.db')
c = conn.cursor()

# テーブル作成
c.execute('''CREATE TABLE IF NOT EXISTS authorship (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             textName TEXT,
             userName TEXT,
             caseNumber TEXT,
             caseName INTEGER,
             Date TEXT)''')

# データ挿入
c.execute("INSERT INTO authorship (textName, userName, caseNumber, caseName, Date) VALUES (?, ?, ?, ?, ?)",
          (textName, userName, caseNumber, caseName, current_time))

# コミットして変更を保存
conn.commit()

# データベースからデータ取得
c.execute("SELECT * FROM authorship")
collection = c.fetchall()

# 取得したデータを標準出力で表示
for element in collection:
    print(element)

# 接続を閉じる
conn.close()
