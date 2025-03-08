# ----------------------------------- 題目內容 ----------------------------------- #
# 
# 國泰銀行要慶祝六十周年，需要買字母貼紙來布置活動空間，文字為"Hello welcome to Cathay 60th year anniversary"，請寫一個程式計算每個字母(大小寫視為同個字母)出現次數
# 
# ----------------------------------- 預期結果 ----------------------------------- #
# "輸出：
# 0 1
# 6 1
# A 4
# C 2
# E 5
# H 3
# ....(繼續印下去)"
# ---------------------------------------------------------------------------- #

def count_letters(text):
    # text 轉大寫，去空格
    char = text.upper().replace(" ", "")
    # 建立字典
    char_dict = {}
    # 計算字母出現次數
    for i in char:
        if i in char_dict:
            char_dict[i] += 1
        else:
            char_dict[i] = 1
    # 依照字母順序 print 出字母及次數
    for key, value in sorted(char_dict.items()):
        print(key, value)

sentence  = "Hello welcome to Cathay 60th year anniversary"
count_letters(sentence)