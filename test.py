# encoding:utf-8

import requests
import base64

'''
车牌识别
'''

request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"
# 二进制方式打开图片文件
f = open('D:\Code\python_PlateRecogntion\car_pic\car4.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image": img}
# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=aasLsHrRW46GGS9TM3Uc1XfH&client_secret=4GAxhsW8Vb1tvGLLt3ZGEavOtQx6aS2W'
response = requests.get(host)
if response:
    access_token = response.json()["access_token"]
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print(response.json())



