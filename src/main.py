import login
import json
import database
import sys

# 获取验证码信息
returnData = login.captchaGget()

# 获取密钥和令牌
secretKeyBytes = returnData["repData"]["secretKey"].encode('utf-8')
token = returnData["repData"]["token"].encode('utf-8')

# 获取原始图片和拼图图片的base64编码
originalImgBase64 = returnData["repData"]["originalImageBase64"]
jigsawImgBase64 = returnData["repData"]["jigsawImageBase64"]

# 计算偏移量
xOffsetResult = login.calculateOffset(originalImgBase64, jigsawImgBase64)

# 生成坐标字节
coordinateBytes = json.dumps({"x": xOffsetResult, "y": 5}, separators=(',', ':'))

# 生成令牌坐标字节
tokenCoordinateBytes = (token.decode('utf-8') + "---" + coordinateBytes).encode('utf-8')

# 加密验证码
encryptedVerification = login.encryptAesEcb(coordinateBytes.encode("utf-8"), secretKeyBytes)

# 加密令牌坐标
captchaVerification = login.encryptAesEcb(tokenCoordinateBytes, secretKeyBytes)

# 验证码验证
login.checkVerification(encryptedVerification, token.decode('utf-8'))

# 登录
# phone = 17388542263
# passwd = "06180136"
# Get the phone number and password from the command-line arguments
# python3 xxx.py 17388542263 06180136
phone = sys.argv[1]
passwd = sys.argv[2]

login_data = login.login(phone, passwd, captchaVerification)

# 将得到的登录信息保存为JSON
with open('login_data.json', 'w') as json_file:
    json.dump(login_data, json_file)

# 重新加载这些JSON数据
with open('login_data.json', 'r') as json_file:
    login_data_loaded = json.load(json_file)

# 连接数据库
connection = database.connect_to_database()

# 创建游标
cursor = connection.cursor()

# 提取登录信息
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

# 检查用户是否存在于 user 表中
sql = f"SELECT * FROM user WHERE userId = '{userId}'"
cursor.execute(sql)
result = cursor.fetchall()

# 准备 SQL 语句
user_sql = None
user_info_sql = None

# 根据用户是否存在，准备相应的 SQL 语句
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

# 执行 SQL 语句
cursor.execute(user_sql)
cursor.execute(user_info_sql)

# 提交事务
connection.commit()

# 关闭连接
cursor.close()
connection.close()