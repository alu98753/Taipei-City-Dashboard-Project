import requests

# 設置目標URL
url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-061?Authorization=CWA-64E4685F-C286-42E2-BFF9-290C61EB7465&limit=10&format=json"


# 提供API金鑰
# api_key = "CWA-D31EC832-ADFA-465F-A266-30229B00A185"
			 
res = requests.get(url)

if res.history:
	print("Request was redirected")
	for resp in res.history:
		print(resp.status_code, resp.url)
		print("Final destination:")
		print(res.status_code, res.url)
else:
 	print("Request was not redirected")
#write file
with open('output.xml', 'wb') as f:
	f.write(res.content)



# 發送GET請求，並在標頭中傳遞API金鑰
try:
    # 發送GET請求
    response = requests.get(url)

    # 檢查響應狀態碼
    print( response.status_code)

    # 解析JSON格式的響應資料
    data = response.json()
    
    # 處理JSON資料以獲取天氣預報資訊
    # 在這裡，您可以根據API的資料結構和您的需求來提取所需的資訊
    # 例如：data['result']['records'] 可能包含了天氣預報的詳細資訊
    
    # 輸出或處理天氣預報資訊
    print(data)
    
except requests.exceptions.HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except requests.exceptions.JSONDecodeError as json_err:
    print(f'JSON decoding error occurred: {json_err}')
except Exception as err:
    print(f'An error occurred: {err}')