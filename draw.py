import pandas as pd
import matplotlib.pyplot as plt


# 讀取 CSV 檔案
file_path = "trimed_data.csv"  # 替換成你的文件路徑
df = pd.read_csv(file_path)

# 確認欄位存在
if 'pitch_type' in df.columns and 'swing' in df.columns:
    # 統計 pitch_type 的分佈
    pitch_type_counts = df['pitch_type'].value_counts()
    pitch_type_percentages = pitch_type_counts / pitch_type_counts.sum() * 100

    # 統計 swing 的分佈
    swing_counts = df['swing'].value_counts()
    swing_percentages = swing_counts / swing_counts.sum() * 100

    # 畫出 pitch_type 的圓餅圖
    plt.figure(figsize=(8, 8))
    plt.pie(pitch_type_percentages, labels=pitch_type_counts.index,
            autopct='%1.1f%%', startangle=90)
    plt.title("Pitch Type Distribution")
    plt.show()

    # 畫出 swing 的圓餅圖
    plt.figure(figsize=(8, 8))
    plt.pie(swing_percentages, labels=swing_counts.index,
            autopct='%1.1f%%', startangle=90)
    plt.title("Swing Distribution")
    plt.show()

else:
    print("CSV 文件中缺少 'pitch_type' 或 'swing' 欄位")
