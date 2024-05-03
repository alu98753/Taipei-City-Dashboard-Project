from geopy.geocoders import GoogleV3
import pandas as pd
import time
import re

#宣告 Google Maps geolocator
geolocator = GoogleV3(api_key="AIzaSyCbRrVk1gKRZRDHnQwRDcp6dw9ZINmZLfs")  # 請替換成你的 Google API 金鑰

# 读取 CSV 文件
data = pd.read_csv("C:\\Side_Project\\Tpi-Data\\monitor-raw.csv")

# 創建新的欄位來存放經緯度資訊
data["longitude"] = None
data["latitude"] = None
index_to_drop = []  # 用於儲存要刪除的行的索引


# 設定要查詢的地址
for index, row in data.iterrows():
	matches = re.search(r'(\w+[路街段道])(\d+段)?(\d+巷)?(\d+弄)?(\w+)?(\d+[-]?\d*號)?', row["安裝地址"].strip())
						# r'(\w+[路街段道])(\d+段)?(\d+巷)?(\d+弄)?(\w+)?(\d+號)'
						# r'(\w+[路街段道])(\d+段)?(\d+巷)?(\d+弄)?(\d+號)?(\d+號)?'
						# r'(\w+[路街段道])(\d+段)?(\d+巷)?(\d+弄)?(\d+號)?'

	if matches:    
		location = geolocator.geocode(matches.group(0))

		if location:
			# 更新 DataFrame 中的經緯度資訊
			data.at[index, "longitude"] = location.longitude
			data.at[index, "latitude"] = location.latitude

			# 顯示地址及其對應的經緯度
			print(row["安裝地址"], (location.longitude, location.latitude),"group(0): ",matches.group(0))
		else:
			# 如果無法找到地址對應的經緯度，則輸出錯誤訊息
			print("無法找到地址對應的經緯度:", row["安裝地址"] ,"group(0): ",matches.group(0))
			index_to_drop.append(index)
	else:
		# 如果無法找到地址對應的經緯度，則輸出錯誤訊息
		print("找不到符合格式的地址:", row["安裝地址"])
		index_to_drop.append(index)
  
# 刪除要刪除的行
data.drop(index_to_drop, inplace=True)

# 將帶有經緯度資訊的 DataFrame 保存為新的 CSV 文件
# data.to_csv("C:\\Side_Project\\Tpi-Data\\monitor-coordinates.csv", index=False)
