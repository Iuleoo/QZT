import requests
import json
import database
import base64


# Connect to the database
connection = database.connect_to_database()

# Create a cursor
cursor = connection.cursor()

# Query to get the user token and userName
user_id = 391997
sql_token = f"SELECT token FROM user WHERE userId = '{user_id}'"
sql_user = f"SELECT userName FROM user WHERE userId = '{user_id}'"
sql_address = f"SELECT address_lite FROM user_info WHERE userId = '{user_id}'"

# Get the token from the database
cursor.execute(sql_token)
result = cursor.fetchall()

# Get the userName from the database
cursor.execute(sql_user)
result_user = cursor.fetchall()
user_name = result_user[0][0]

# Get the address from the database
cursor.execute(sql_address)
result_address = cursor.fetchall()
address = result_address[0][0]

# Close the connection
cursor.close()
connection.close()


code = '打卡成功'
title = "{},{}".format(user_name, code)
content = {address}

url = "https://www.pushplus.plus/send"

payload = json.dumps({
   "token": "87cdcff73305443c9eb690fe2169fa31",
   "title": title,
   "content": address,
   "template": "markdown"
})
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)