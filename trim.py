import pandas as pd


def filter_pitch_data(csv_file, output_file=None):
    """
    過濾指定的 pitch_type 和 code 資料。

    Args:
        csv_file (str): 原始 CSV 檔案路徑。
        output_file (str, optional): 篩選後的 CSV 輸出路徑，若為 None 則不儲存。

    Returns:
        pd.DataFrame: 過濾後的資料框。
    """
    # 讀取 CSV 檔案
    df = pd.read_csv(csv_file)

    # 定義要保留的條件
    valid_pitch_types = ["FF", "SL", "FT", "CH", "SI", "CU", "FC"]
    valid_codes = ["B", "C", "X", "S", "D", "E", "H"]

    # 過濾資料
    filtered_df = df[df["pitch_type"].isin(
        valid_pitch_types) & df["code"].isin(valid_codes)]

    # 新增 "揮棒" 欄位
    filtered_df["swing"] = filtered_df["code"].apply(
        lambda x: 1 if x in ["F", "X", "S", "D", "E"] else 0)

    # 新增 "結果" 欄位
    def calculate_result(row):
        if row["swing"] == 0:
            # 壞球是 1，好球是 0
            return 1 if row["code"] == "B" or row["code"] == "H" else 0
        else:
            return 1 if row["code"] in ["X", "D", "E"] else 0  # 打中是 1，沒打中是 0

    def convert_pitch_type(row):
        if row["pitch_type"] == "FF" or row["pitch_type"] == "FT" or row["pitch_type"] == "FC" or row["pitch_type"] == "SI":
            return "F"  # 壞球是 1，好球是 0
        elif row["pitch_type"] == "SL" or row["pitch_type"] == "CU":
            return "B"  # 打中是 1，沒打中是 0
        elif row["pitch_type"] == "CH":
            return "O"

    filtered_df["bat_result"] = filtered_df.apply(calculate_result, axis=1)
    filtered_df["pitch_type"] = filtered_df.apply(convert_pitch_type, axis=1)
    # 若指定了輸出檔案，將結果儲存
    if output_file:
        filtered_df.to_csv(output_file, index=False)
        print(f"Filtered data saved to {output_file}")

    return filtered_df


# 使用範例
csv_file = "output.csv"  # 替換為你的輸入檔案
output_file = "trimed_data.csv"  # 替換為你的輸出檔案名稱
filtered_data = filter_pitch_data(csv_file, output_file)

# 顯示過濾後的資料
print(filtered_data)
