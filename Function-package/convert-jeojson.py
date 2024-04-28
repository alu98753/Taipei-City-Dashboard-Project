import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# 读取 CSV 文件
data = pd.read_csv("C:\Side_Project\Tpi-Data\TaipeiLight-conv.csv")

# 创建 GeoDataFrame
geometry = [Point(xy) for xy in zip(data['Longitude'], data['Latitude'])]
crs = {'init': 'epsg:4326'}  # 设置坐标参考系统为 WGS84
gdf = gpd.GeoDataFrame(data, crs=crs, geometry=geometry)

# 保存为 GeoJSON 文件
gdf.to_file("C:\Side_Project\Tpi-Data\TpiLight.geojson", driver='GeoJSON')
