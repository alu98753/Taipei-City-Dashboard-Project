import geopandas as gpd
import json
from shapely.geometry import Point

df = gpd.read_file('car_accident.csv', encoding="utf-8")
df['geometry'] = df.apply(lambda row: Point(float(row['座標-X']), float(row['座標-Y'])) ,axis=1)
df=df.drop("座標-X", axis=1)
df=df.drop("座標-Y", axis=1)
print(df.head())
gdf = gpd.GeoDataFrame(df, geometry='geometry')
gdf.to_file('car_accident.geojson', driver='GeoJSON')

