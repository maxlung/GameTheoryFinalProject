import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_distributions(csv_file, columns):
    """
    繪製指定欄位值的分布圖。

    Args:
        csv_file (str): CSV 文件的路徑。
        columns (list): 欲繪製分布的欄位列表。
    """
    # 讀取 CSV 檔案
    df = pd.read_csv(csv_file)

    for column in columns:
        if column not in df.columns:
            print(f"Column '{column}' not found in the CSV file.")
            continue

        # 計算值的分布
        value_counts = df[column].value_counts()

        # 繪圖
        plt.figure(figsize=(10, 6))
        sns.barplot(x=value_counts.index,
                    y=value_counts.values, palette="viridis")
        plt.title(f"Distribution of '{column}'", fontsize=16)
        plt.xlabel(column, fontsize=14)
        plt.ylabel("Count", fontsize=14)
        plt.xticks(rotation=45, fontsize=12)
        plt.tight_layout()
        plt.show()


# 使用範例
csv_file = "trimed_data.csv"  # 替換為你的 CSV 檔案名稱
columns_to_plot = ["code", "type", "pitch_type"]  # 欲分析的欄位
plot_distributions(csv_file, columns_to_plot)
