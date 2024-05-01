import csv
from pyproj import Proj, transform
import time

# 定义TWD97投影坐标系和WGS84经纬度坐标系
twd97 = Proj(init='epsg:3826')  # TWD97坐标系
wgs84 = Proj(init='epsg:4326')  # WGS84坐标系

# 打开CSV文件
with open(r'C:\Side_Project\Tpi-Data\TaipeiLight.csv', 'r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    # 创建新的CSV文件，用于存储转换后的数据
    with open(r'C:\Side_Project\Tpi-Data\TpiLight-convert.csv', 'w', newline='', encoding='utf-8') as converted_file:
        fieldnames = csvreader.fieldnames + ['Longitude', 'Latitude']
        csvwriter = csv.DictWriter(converted_file, fieldnames=fieldnames)
        csvwriter.writeheader()
   		       
        # 逐行读取CSV文件
        for row in csvreader:
            try:
                start_time = time.time()     
                twd97_x_str = row[' TWD97X'].strip()  # 去除空白字符
                twd97_y_str = row[' TWD97Y'].strip()  # 去除空白字符
                
                if twd97_x_str and twd97_y_str:  # 如果不是空字符串
                    twd97_x = float(twd97_x_str)
                    twd97_y = float(twd97_y_str)
                
                    # 转换为经度和纬度
                    lon, lat = transform(twd97, wgs84, twd97_x, twd97_y)
                    
                    # 将转换后的结果写入新的CSV文件
                    row['Longitude'] = lon
                    row['Latitude'] = lat
                    csvwriter.writerow(row)
                    
                    # 计算转换时间并打印
                    elapsed_time = time.time() - start_time
                    print(f"Longitude: {lon}, Latitude: {lat}, Cost time: {elapsed_time} sec")
                else:
                    print("TWD97X or TWD97Y 为空字符串，跳过此行.")
            except KeyError as e:
                print(f"行缺少键: {e}, 跳过此行.")
            except ValueError as e:
                print(f"无法将值转换为浮点数: {e}, 跳过此行.")
