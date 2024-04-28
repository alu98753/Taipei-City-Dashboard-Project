import pandas as pd

# 读取 CSV 文件
df = pd.read_csv("C:\Side_Project\Tpi-Data\TpiLight-convert.csv")

# 选择要保留的列
selected_columns = ['SerialNumber', ' Dist', ' TWD97X', ' TWD97Y', ' UpdDate','Longitude','Latitude']
df_selected = df[selected_columns]

# 保存到新的 CSV 文件
df_selected.to_csv("C:\Side_Project\Tpi-Data\TaipeiLight-conv.csv", index=False)
