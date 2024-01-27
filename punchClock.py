import json
import requests
import base64
import database

# 连接到数据库
with database.connect_to_database() as connection:
    # 创建游标
    with connection.cursor() as cursor:
        # 查询以获取用户令牌和用户名
        user_id = 391997
        sql_get_user_token = f"SELECT token FROM user WHERE userId = '{user_id}'"
        sql_get_user_name = f"SELECT userName FROM user WHERE userId = '{user_id}'"
        sql_get_user_address = f"SELECT address FROM user_info WHERE userId = '{user_id}'"
        sql_get_user_address_lite = f"SELECT address_lite FROM user_info WHERE userId = '{user_id}'"

        # 从数据库获取令牌
        cursor.execute(sql_get_user_token)
        token_result = cursor.fetchall()
        token = token_result[0][0]

        # 从数据库获取用户名
        cursor.execute(sql_get_user_name)
        user_result = cursor.fetchall()
        user_name = user_result[0][0]

        # 从数据库获取地址
        cursor.execute(sql_get_user_address)
        address_result = cursor.fetchall()
        address = address_result[0][0]

        # 从数据库获取精简地址
        cursor.execute(sql_get_user_address_lite)
        address_result = cursor.fetchall()
        address_lite = address_result[0][0]

# 使用 base64 对地址进行编码，str转化为 utf-8 编码
encoded_address64 = base64.b64encode(address.encode("utf-8")).decode("utf-8")

# 打印用户信息
# print("用户名：", user_name)
# print("精简地址：", address_lite)
# print("地址：", address)
# print("编码后的地址：", encoded_address64)
# print("Token：", token)

# 构造请求头
headers = {
    'token': token,
    'user-agent': 'Mozilla/5.0 (Linux; Android 14; LGE-AN00 Build/HONORLGE-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.210 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/30.461538)',
    'Content-Type': 'application/json',
    'Content-Length': '389',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}

# 构造请求体
payload = base64.b64decode(encoded_address64)

# 发送请求
response0 = requests.request("POST", "http://gwsxapp.gzzjzhy.com/api/workClock/punchClock", headers=headers, data=payload)

# 打印请求结果
print(response0.json())