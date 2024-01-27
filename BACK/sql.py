import re
import mysql.connector

data = """ 
    {'repCode': '0000', 'repMsg': None, 'repData': {'captchaId': None, 'projectCode': None, 'captchaType': 'blockPuzzle', 'captchaOriginalPath': None, 'captchaFontType': None, 'captchaFontSize': None, 'secretKey': None, 'originalImageBase64': None, 'point': None, 'jigsawImageBase64': None, 'wordList': None, 'pointList': None, 'pointJson': 'EWgPRbFDtRBMCIG4kFrxYRmxkmylIbPJz/Lu5nS1c+eoGzc2Rkf02UwPUCMeO7cd', 'token': '4372e1cf7c0947a89454638ffabf68ab', 'result': True, 'captchaVerification': None, 'clientUid': None, 'ts': None, 'browserInfo': None}, 'success': True}
{'code': 0, 'data': {'id': 'eb50c8d755554031843940d8cba2b326', 'userId': 391997, 'userName': '袁霏宏', 'phonenumber': '17388542263', 'sex': 0, 'sexName': '男', 'avatar': None, 'internshipStatus': 3, 'internshipStatusName': '实习中', 'schoolName': '贵州轻工职业技术学院', 'collegeName': '信息工程系', 'majorName': '云计算技术与应用', 'className': '2021级云计算技术应用1班', 'schoolId': '9f7c053a1d9c451498378e2eb354ae04', 'collegeId': 'b81827cb13c04b80a9b991f4d7b0606f', 'collegeIds': None, 'majorId': 'd304501dd06c47d3817672b44f1644ea', 'classId': '48de5f6693cf4f5cb6d8a5bf8dc7ca3e', 'createTime': '2023-06-20', 'planId': 'eb1649bbe5844371a35a09446ba13faa', 'planName': '信息系2021级岗位实习云计算', 'planDistributionId': 'ae1ff9925caa4ba08c5c3ec7a8734093-56', 'teacherId': 'aa6f8d5be819454ca052375fccd3fcc1', 'teacherName': '李东丽', 'enterpriseId': '02e61ca2dc8d41ada545d9ec37c086d7', 'enterpriseName': '达运精密工业（厦门）有限公司', 'studentCode': '20210105163', 'grade': '2021', 'token': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VycyIsImlzcyI6IllHQkgtUFJBQ1RJQ0UiLCJleHAiOjE3MDY4NzY4NjksInVzZXIiOiJ7XCJjbGFzc0lkXCI6XCI0OGRlNWY2NjkzY2Y0ZjVjYjZkOGE1YmY4ZGM3Y2EzZVwiLFwiY2xhc3NOYW1lXCI6XCIyMDIx57qn5LqR6K6h566X5oqA5pyv5bqU55SoMeePrVwiLFwiY29sbGVnZUlkXCI6XCJiODE4MjdjYjEzYzA0YjgwYTliOTkxZjRkN2IwNjA2ZlwiLFwiY29sbGVnZU5hbWVcIjpcIuS_oeaBr-W3peeoi-ezu1wiLFwiY3JlYXRlVGltZVwiOlwiMjAyMy0wNi0yMFwiLFwiZW50ZXJwcmlzZUlkXCI6XCIwMmU2MWNhMmRjOGQ0MWFkYTU0NWQ5ZWMzN2MwODZkN1wiLFwiZW50ZXJwcmlzZU5hbWVcIjpcIui-vui_kOeyvuWvhuW3peS4mu-8iOWOpumXqO-8ieaciemZkOWFrOWPuFwiLFwiZXhwVGltZVwiOjE3MDY4NzY4Njk4ODIsXCJncmFkZVwiOlwiMjAyMVwiLFwiaWRcIjpcImViNTBjOGQ3NTU1NTQwMzE4NDM5NDBkOGNiYTJiMzI2XCIsXCJpbnRlcm5zaGlwU3RhdHVzXCI6MyxcImludGVybnNoaXBTdGF0dXNOYW1lXCI6XCLlrp7kuaDkuK1cIixcImxpc3RSb2xlXCI6W10sXCJtYWpvcklkXCI6XCJkMzA0NTAxZGQwNmM0N2QzODE3NjcyYjQ0ZjE2NDRlYVwiLFwibWFqb3JOYW1lXCI6XCLkupHorqHnrpfmioDmnK_kuI7lupTnlKhcIixcInBob25lbnVtYmVyXCI6XCIxNzM4ODU0MjI2M1wiLFwicGxhbkRpc3RyaWJ1dGlvbklkXCI6XCJhZTFmZjk5MjVjYWE0YmEwOGM1YzNlYzdhODczNDA5My01NlwiLFwicGxhbklkXCI6XCJlYjE2NDliYmU1ODQ0MzcxYTM1YTA5NDQ2YmExM2ZhYVwiLFwicGxhbk5hbWVcIjpcIuS_oeaBr-ezuzIwMjHnuqflspfkvY3lrp7kuaDkupHorqHnrpdcIixcInJvbGVLZXlcIjpcInh5XCIsXCJzY2hvb2xDb2xsZWdlVk9TXCI6W10sXCJzY2hvb2xJZFwiOlwiOWY3YzA1M2ExZDljNDUxNDk4Mzc4ZTJlYjM1NGFlMDRcIixcInNjaG9vbE5hbWVcIjpcIui0teW3nui9u-W3peiBjOS4muaKgOacr-WtpumZolwiLFwic2V4XCI6MCxcInNleE5hbWVcIjpcIueUt1wiLFwic3R1ZGVudENvZGVcIjpcIjIwMjEwMTA1MTYzXCIsXCJ0ZWFjaGVySWRcIjpcImFhNmY4ZDViZTgxOTQ1NGNhMDUyMzc1ZmNjZDNmY2MxXCIsXCJ0ZWFjaGVyTmFtZVwiOlwi5p2O5Lic5Li9XCIsXCJ0b2tlbklkXCI6XCI0MmQ5YmYzMC05Yjc3LTQ0ZWQtYWI5YS1lMjZiYzAxODNmODVcIixcInR5cGVcIjoxLFwidXNlcklkXCI6MzkxOTk3LFwidXNlck5hbWVcIjpcIuiigemcj-Wuj1wifSIsImlhdCI6MTcwNjI3MjA2OSwianRpIjoiNDJkOWJmMzAtOWI3Ny00NGVkLWFiOWEtZTI2YmMwMTgzZjg1In0.8hBpDqOk3B3487FOJ3E377Vb06FwsIRbMBMA9avmhj4', 'tokenId': '42d9bf30-9b77-44ed-ab9a-e26bc0183f85', 'type': 1, 'roleKey': 'xy', 'expTime': '2024-02-02 20:27:49', 'listRole': [], 'schoolCollegeVOS': []}, 'msg': '操作成功'}
"""

# 去除前后的空白字符
data = data.strip()

# 用户ID
user_id = re.search(r"'userId': (\d+)", data).group(1)
# 用户名  
user_name = re.search(r"'userName': '(.+?)'", data).group(1)  
# 手机号
phone = re.search(r"'phonenumber': '(.+?)'", data).group(1)
# 性别  
sex_name = re.search(r"'sexName': '(.+?)'", data).group(1)
# 实习状态  
intern_status = re.search(r"'internshipStatusName': '(.+?)'", data).group(1)
# 学校名称
school_name = re.search(r"'schoolName': '(.+?)'", data).group(1)
# 学院名称
college_name = re.search(r"'collegeName': '(.+?)'", data).group(1) 
# 专业名称  
major_name = re.search(r"'majorName': '(.+?)'", data).group(1)
# 班级名称
class_name = re.search(r"'className': '(.+?)'", data).group(1)
# 年级
grade = re.search(r"'grade': '(.+?)'", data).group(1)  
# 学号  
stu_code = re.search(r"'studentCode': '(.+?)'", data).group(1)
# 实习计划ID
plan_id = re.search(r"'planId': '(.+?)'", data).group(1)
# 实习计划名称  
plan_name = re.search(r"'planName': '(.+?)'", data).group(1)
# 实习单位ID
enterprise_id = re.search(r"'enterpriseId': '(.+?)'", data).group(1)
# 实习单位名称
enterprise_name = re.search(r"'enterpriseName': '(.+?)'", data).group(1)
# 指导教师ID
teacher_id = re.search(r"'teacherId': '(.+?)'", data).group(1)
# 指导教师姓名
teacher_name = re.search(r"'teacherName': '(.+?)'", data).group(1)
# 提取两个token
tokens = [token for token in re.findall(r"'token': '(.+?)'", data)]

# 连接数据库
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="qzt",
    port=3306
)

# 创建游标
cursor = connection.cursor()

# 执行SQL语句
outsql = f"""
INSERT INTO user_info (user_id, user_name, phone, sex_name, internship_status_name, school_name, college_name, major_name, class_name, grade, student_code, plan_id, plan_name, enterprise_id, enterprise_name, teacher_id, teacher_name, token1, token2)
VALUES (
    '{user_id}',
    '{user_name}',
    '{phone}',
    '{sex_name}',
    '{intern_status}',
    '{school_name}',
    '{college_name}',
    '{major_name}',
    '{class_name}',
    '{grade}',
    '{stu_code}',
    '{plan_id}',
    '{plan_name}',
    '{enterprise_id}',
    '{enterprise_name}',
    '{teacher_id}',
    '{teacher_name}',
    '{tokens[0]}',
    '{tokens[1]}'
);
"""
cursor.execute(outsql)

# 提交事务
connection.commit()

# 关闭连接
cursor.close()
connection.close()