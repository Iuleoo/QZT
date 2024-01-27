import json
import requests
import base64
import database

# 连接数据库
connection = database.connect_to_database()

# 创建游标
cursor = connection.cursor()

# 查询用户 token 和 userName
user_id = 391997
sql_token = f"SELECT token FROM user WHERE userId = '{user_id}'"
sql_user = f"SELECT userName FROM user WHERE userId = '{user_id}'"
cursor.execute(sql_token)
result = cursor.fetchall()

# 构造请求头
headers = {
    'token': result[0][0],
    'user-agent': 'Mozilla/5.0 (Linux; Android 14; LGE-AN00 Build/HONORLGE-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.210 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/30.461538)',
    'Content-Type': 'application/json',
    'Content-Length': '389',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}

# 构造请求体
payload = base64.b64decode("ew0KICAgICJsYXRpdHVkZSI6IDI0LjY2NzAyNSwNCiAgICAibG9jYXRpb25OYW1lIjogIuemj+W7uuecgeWOpumXqOW4gue/lOWuieWMuuWQjOe+jumHjDk0LTEtMTAx5a6kIOWPr+WPr+mmqOi2heW4giIsDQogICAgImxvY2F0aW9uQ29kZSI6ICIiLA0KICAgICJsb25naXR1ZGUiOiAxMTguMjE4ODQ1LA0KICAgICJlbnRlcnByaXNlSWQiOiAiMDJlNjFjYTJkYzhkNDFhZGE1NDVkOWVjMzdjMDg2ZDciLA0KICAgICJsaXN0UGhvdG8iOiBbXSwNCiAgICAibGF0aXR1ZGUyIjogIjI0LjY3MzAxOCIsDQogICAgImxvbmdpdHVkMiI6ICIxMTguMjE4ODQ1IiwNCiAgICAiY2hlY2tSYW5nZSI6IDIwMDAsDQogICAgInR5cGVJZCI6IDEwLA0KICAgICJjYXJkUmVtYXJrIjogIlRFU1QwMSINCn0=")

# 发送请求
response0 = requests.request("POST", "http://gwsxapp.gzzjzhy.com/api/workClock/punchClock", headers=headers, data=payload)

# 打印请求结果
print(response0.json())

# 将返回信息保存为 JSON
with open('response_data.json', 'w') as json_file:
    json.dump(response0.json(), json_file)

# 重新加载这些 JSON 数据
with open('response_data.json', 'r') as json_file:
    response_data_loaded = json.load(json_file)

#print(response_data_loaded)
# 从数据库中获取userName
cursor.execute(sql_user)
result_user = cursor.fetchall()
user_name = result_user[0][0]
print(user_name)

# 打卡状态码
code = (response_data_loaded['code'])

if code == 0:
    code_ststus = '打卡成功'
else:
    code_ststus = '打卡失败'

# 打卡内容
msg = (response_data_loaded['msg'])
print (msg)


# 关闭连接
cursor.close()
connection.close()
