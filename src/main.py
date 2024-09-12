import login
import json
import database
import sys


returnData = login.captchaGget()

secretKeyBytes = returnData["repData"]["secretKey"].encode('utf-8')
token = returnData["repData"]["token"].encode('utf-8')
originalImgBase64 = returnData["repData"]["originalImageBase64"]
jigsawImgBase64 = returnData["repData"]["jigsawImageBase64"]

# 计算偏移量
xOffsetResult = login.calculateOffset(originalImgBase64, jigsawImgBase64)
coordinateBytes = json.dumps({"x": xOffsetResult, "y": 5}, separators=(',', ':'))
tokenCoordinateBytes = (token.decode('utf-8') + "---" + coordinateBytes).encode('utf-8')
encryptedVerification = login.encryptAesEcb(coordinateBytes.encode("utf-8"), secretKeyBytes)
captchaVerification = login.encryptAesEcb(tokenCoordinateBytes, secretKeyBytes)

# 验证码验证
login.checkVerification(encryptedVerification, token.decode('utf-8'))

# 登录
phone = sys.argv[1]
passwd = sys.argv[2]

login_data = login.login(phone, passwd, captchaVerification)


with open('login_data.json', 'w') as json_file:
    json.dump(login_data, json_file)
with open('login_data.json', 'r') as json_file:
    login_data_loaded = json.load(json_file)


connection = database.connect_to_database()
# 创建游标
cursor = connection.cursor()

userId = login_data_loaded['data']['userId']
userName = login_data_loaded['data']['userName']
phonenumber = login_data_loaded['data']['phonenumber']
sexName = login_data_loaded['data']['sexName']
schoolName = login_data_loaded['data']['schoolName']
collegeName = login_data_loaded['data']['collegeName']
majorName = login_data_loaded['data']['majorName']
className = login_data_loaded['data']['className']
teacherName = login_data_loaded['data']['teacherName']
enterpriseId = login_data_loaded['data']['enterpriseId']
enterpriseName = login_data_loaded['data']['enterpriseName']
studentCode = login_data_loaded['data']['studentCode']
token = login_data_loaded['data']['token']
expTime = login_data_loaded['data']['expTime']


sql = f"SELECT * FROM user WHERE userId = '{userId}'"
cursor.execute(sql)
result = cursor.fetchall()

user_sql = None
user_info_sql = None

if result:
    user_sql = f"""
        UPDATE user
        SET token = '{token}'
        WHERE userId = '{userId}'
    """

    user_info_sql = f"""
        UPDATE user_info
        SET phonenumber = '{phonenumber}'
        WHERE userId = '{userId}'
    """
else:
    user_sql = f"""
    INSERT INTO user (
        userId,
        userName,
        phonenumber,
        sexName,
        schoolName,
        collegeName,
        majorName,
        className,
        teacherName,
        enterpriseId,
        enterpriseName,
        studentCode,
        token,
        expTime
    )
    VALUES (
        '{userId}',
        '{userName}',
        '{phonenumber}',
        '{sexName}',
        '{schoolName}',
        '{collegeName}',
        '{majorName}',
        '{className}',
        '{teacherName}',
        '{enterpriseId}',
        '{enterpriseName}',
        '{studentCode}',
        '{token}',
        '{expTime}'
    );
    """

    user_info_sql = f"""
    INSERT INTO user_info (userId, userName, phonenumber)
    VALUES (
        '{userId}',
        '{userName}',
        '{phonenumber}'
    );
    """

cursor.execute(user_sql)
cursor.execute(user_info_sql)

connection.commit()

cursor.close()
connection.close()