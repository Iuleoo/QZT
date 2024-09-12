import json
import requests
import base64
import database
import sys
import datetime

user_id = sys.argv[1]

# 连接到数据库
with database.connect_to_database() as connection:
    with connection.cursor() as cursor:
        # user_id = 391998
        sql_get_user_token = f"SELECT token FROM user WHERE userId = '{user_id}'"
        sql_get_user_name = f"SELECT userName FROM user WHERE userId = '{user_id}'"
        sql_get_user_address = f"SELECT address FROM user_info WHERE userId = '{user_id}'"
        sql_get_user_address_lite = f"SELECT address_lite FROM user_info WHERE userId = '{user_id}'"

        cursor.execute(sql_get_user_token)
        token_result = cursor.fetchall()
        token = token_result[0][0]

        cursor.execute(sql_get_user_name)
        user_result = cursor.fetchall()
        user_name = user_result[0][0]

        cursor.execute(sql_get_user_address)
        address_result = cursor.fetchall()
        address = address_result[0][0]

        cursor.execute(sql_get_user_address_lite)
        address_result = cursor.fetchall()
        address_lite = address_result[0][0]

encoded_address64 = base64.b64encode(address.encode("utf-8")).decode("utf-8")


# 构造请求头
headers = {
    'token': token,
    'user-agent': 'Mozilla/5.0 (Linux; Android 14; LGE-AN00 Build/HONORLGE-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.210 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/30.461538)',
    'Content-Type': 'application/json',
    'Content-Length': '389',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}

payload = base64.b64decode(encoded_address64)

response0 = requests.request("POST", "http://gwsxapp.gzzjzhy.com/api/workClock/punchClock", headers=headers, data=payload)
with open('response_data.json', 'w') as json_file:
    json.dump(response0.json(), json_file)
with open('response_data.json', 'r') as json_file:
    response_data_loaded = json.load(json_file)

# 打卡内容
msg = (response_data_loaded['msg'])
code = (response_data_loaded['code'])

if code == 0:
    code_ststus = '打卡成功'
else:
    code_ststus = '打卡失败'

# SELECT DATA TIMESTAMP
timestamp = datetime.datetime.now().timestamp() * 1000000 + datetime.datetime.now().microsecond
timestamp_str = str(timestamp)

titles = "{},{}".format(user_name, code_ststus)
contents = "打卡状态：{}\n打卡地址：{}\n服务器时间戳：{}".format(msg, address_lite, timestamp_str)

# pushplus 一对多推送，如需一对一删除 topic 参数即可

url = "https://www.pushplus.plus/send"

payload = json.dumps({
   "token": "87cdcff73305443c9eb690fe2169fa31",
   "title": titles,
   "content": contents,
   "topic": "2024",
   "timestamp": timestamp_str,
   "template": "html"
})
headers = {
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)