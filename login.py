import requests
import json
import random
import uuid
import time
import cv2
import numpy as np
from aesEncode import encryptAesEcb, decryptAesEcb
import base64
import mysql.connector

# 获取当前时间戳（毫秒）
current_time_seconds = time.time()
timestamp_milliseconds = int(current_time_seconds * 1000)

# 登录函数
def login(phone, passwd, encrypted_token):
    """
    登录函数

    Args:
        phone: 手机号
        passwd: 密码
        encrypted_token: 加密后的验证码

    Returns:
        登录结果
    """
    url = "http://gwsxapp.gzzjzhy.com/api/user/login"
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6013 Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.101 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/30.47619)",
        "Content-Type": "application/json",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    data = {
        "phonenumber": phone,
        "password": passwd,
        "captchaVerification": encrypted_token
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    # 打印返回个人信息
    # print(response.json())
    return response.json()

# 验证码验证函数
def checkVerification(encryptedVerification, tokenCoordinateByte):
    """
    验证码验证函数

    Args:
        encryptedVerification: 加密后的验证码
        tokenCoordinateByte: token坐标字节

    Returns:
        验证码验证结果
    """
    url = "http://gwsxapp.gzzjzhy.com//captcha/check"
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6013 Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.101 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/30.47619)",
        "Content-Type": "application/json",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    data = {
        "captchaType": "blockPuzzle",
        "pointJson": encryptedVerification,
        "token": tokenCoordinateByte
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    # 打印返回 第一条JSON
    #print(response.json())
    return response.json()

# 获取验证码函数
def captchaGget():
    """
    获取验证码函数

    Returns:
        验证码信息
    """
    url = "http://gwsxapp.gzzjzhy.com//captcha/get"
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 10; ONEPLUS A6013 Build/QQ3A.200805.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.101 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/30.47619)",
        "Content-Type": "application/json",
        "Content-Length": "106",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    data = {
        "captchaType": "blockPuzzle",
        "clientUid": f"slider-{uuid.uuid4()}",
        "ts": int(current_time_seconds * 1000)
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    return response.json()

# 计算偏移函数
def calculateOffset(originalImgBase64, jigsawImgBase64):
    """
    计算偏移函数

    Args:
        originalImgBase64: 原始图片base64编码
        jigsawImgBase64: 拼图图片base64编码

    Returns:
        偏移量
    """
    originalEdge = cv2.Canny(cv2.imdecode(np.frombuffer(base64.b64decode(originalImgBase64), np.uint8), cv2.IMREAD_UNCHANGED), 100, 200)
    jigsawEdge = cv2.Canny(cv2.imdecode(np.frombuffer(base64.b64decode(jigsawImgBase64), np.uint8), cv2.IMREAD_UNCHANGED), 100, 200)

    _, _, _, offset = cv2.minMaxLoc(cv2.matchTemplate(originalEdge, jigsawEdge, cv2.TM_CCOEFF_NORMED))
    offset = offset[0]
    return f"{offset:.14f}"
