import pandas as pd

# 讀取 CSV 檔案
input_file = "pitches.csv"  # 替換為你的 CSV 檔案名稱
output_file = "output.csv"  # 指定輸出的檔案名稱

# 只保留的欄位
columns_to_keep = ["ab_id", "code", "type", "pitch_type"]

# 讀取 CSV 並過濾欄位
df = pd.read_csv(input_file, usecols=columns_to_keep)

# 將結果寫入新的 CSV 檔案
df.to_csv(output_file, index=False)

print(f"已成功將資料保存到 {output_file}，只包含以下欄位: {columns_to_keep}")
