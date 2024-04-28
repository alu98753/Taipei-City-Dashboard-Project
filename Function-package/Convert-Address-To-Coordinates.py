# 地址转换服务流程如 Google 地图 API 或 OpenStreetMap Nominatim API，
# 
# 将地址转换为经纬度坐标。然后，你可以使用 Python 脚本来将 CSV 文件中的地址转换为经纬度坐标，并将其保存到新的 CSV 文件中。以下是一个示例代码：

import pandas as pd
from geopy.geocoders import Nominatim

# 读取 CSV 文件
data = pd.read_csv("C:\Side_Project\Tpi-Data\safe112.csv")

# 创建 Geocoder 对象
geolocator = Nominatim(user_agent="geoapiExercises")

# 定义一个函数来获取地点的经纬度坐标
def get_coordinates(address):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

# 将地址转换为经纬度坐标
data['Latitude'], data['Longitude'] = zip(*data['地點位置'].apply(get_coordinates))

# 保存为新的 CSV 文件
data.to_csv('SafeHavenSpot112.csv', index=False)


# 这段代码将从你的 CSV 文件中读取地址信息，然后使用 Nominatim API 将地址转换为经纬度坐标，并将它们添加到 DataFrame 中。最后，它将保存包含经纬度信息的新 CSV 文件。记得替换 `'your_file.csv'` 为你的 CSV 文件路径。