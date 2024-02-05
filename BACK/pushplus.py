# 导入必要的库
import requests
import json
import database
import base64
import datetime


# 连接到数据库
with database.connect_to_database() as connection:
    # 创建游标
    with connection.cursor() as cursor:
        # 查询以获取用户令牌和用户名
        user_id = 391997
        sql_token = f"SELECT token FROM user WHERE userId = '{user_id}'"
        sql_user = f"SELECT userName FROM user WHERE userId = '{user_id}'"
        sql_address = f"SELECT address_lite FROM user_info WHERE userId = '{user_id}'"

        # 从数据库获取令牌
        cursor.execute(sql_token)
        token_result = cursor.fetchall()
        token = token_result[0][0]

        # 从数据库获取用户名
        cursor.execute(sql_user)
        user_result = cursor.fetchall()
        user_name = user_result[0][0]

        # 从数据库获取地址
        cursor.execute(sql_address)
        address_result = cursor.fetchall()
        address = address_result[0][0]

# 打印用户信息
print(f"用户名：{user_name}")
print(f"地址：{address}")
#print(f"Token：{token}")

# SELECT DATA TIMESTAMP
timestamp = datetime.datetime.now().timestamp() * 1000000 + datetime.datetime.now().microsecond

# 转换为字符串
timestamp_str = str(timestamp)
print(timestamp_str)

# pushplus 一对多推送

url = "https://www.pushplus.plus/send"

payload = json.dumps({
   "token": "87cdcff73305443c9eb690fe2169fa31",
   "title": "消息推送-DEBUG",
   "content": user_name,
   "topic": "2024",
   "timestamp": timestamp_str,
   "template": "html"
})
headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)