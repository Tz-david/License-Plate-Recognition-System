#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'david.tang'

import requests
import os
import base64
import json
import jsonpath

ACCESS_TOKEN = ''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ID,KEY的配置信息
INFO_CONFIG = {
    'ID': '25503959',
    'API_KEY': 'aasLsHrRW46GGS9TM3Uc1XfH',
    'SECRET_KEY': '4GAxhsW8Vb1tvGLLt3ZGEavOtQx6aS2W'
}

# URL配置
URL_LIST_URL = {
    # ACCESS_TOKEN_URL用于获取ACCESS_TOKEN, POST请求,
    #  grant_type必须参数,固定为client_credentials,client_id必须参数,应用的API Key,client_secre 必须参数,应用的Secret Key.
    'ACCESS_TOKEN_URL': 'https://aip.baidubce.com/oauth/2.0/token?' + 'grant_type=client_credentials&client_id={API_KEYS}&client_secret={SECRET_KEYS}&'.format(
        API_KEYS=INFO_CONFIG['API_KEY'], SECRET_KEYS=INFO_CONFIG['SECRET_KEY']),
    # 车牌识别
    'LICENSE_PLATE': 'https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate',
}


class AccessTokenSuper(object):
    pass


class AccessToken(AccessTokenSuper):
    def getToken(self):
        accessToken = requests.post(url=URL_LIST_URL['ACCESS_TOKEN_URL'])
        accessTokenJson = accessToken.json()
        if dict(accessTokenJson).get('error') == 'invalid_client':
            return '获取accesstoken错误，请检查API_KEY，SECRET_KEY是否正确！'
        return accessTokenJson


TOKEN = AccessToken().getToken()
ACCESS_TOKEN = ACCESS_TOKEN if isinstance(TOKEN, str) else TOKEN['access_token']

LICENSE_PLATE_URL = URL_LIST_URL['LICENSE_PLATE'] + '?access_token={}'.format(ACCESS_TOKEN)


class LicensePlateSuper(object):
    pass


class LicensePlate(LicensePlateSuper):

    def __init__(self, image=None, multi_detect=True):
        self.HEADER = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.IMAGE_CONFIG = {
            'multi_detect': multi_detect,
        }

        if image is not None:
            imagepath = os.path.exists(image)
            if imagepath == True:
                images = image
                with open(images, 'rb') as images:
                    self.IMAGE_CONFIG['image'] = base64.b64encode(images.read())

    def postLicensePlate(self):
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate"
        if self.IMAGE_CONFIG.get('image', None) == None:
            return 'image参数不能为空！'
        params = {"image": self.IMAGE_CONFIG['image']}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=aasLsHrRW46GGS9TM3Uc1XfH&client_secret=4GAxhsW8Vb1tvGLLt3ZGEavOtQx6aS2W'
        response = requests.get(host)
        if response:
            access_token = response.json()["access_token"]
        request_url = request_url + "?access_token=" + access_token
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            return response.json()




def api_pic(CPH):
    # 测试获取AccessToken
    testAccessToken = AccessToken()
    # print('Access_token:', testAccessToken.getToken())

    # 车牌号识别
    testLicensePlate = LicensePlate(image=CPH)
    testLicensePlatejson = testLicensePlate.postLicensePlate()

    testcolor = jsonpath.jsonpath(testLicensePlatejson, '$..color')
    testtext = jsonpath.jsonpath(testLicensePlatejson, '$..number')

    testcolorstr = "".join(testcolor)
    testtextstr = "".join(testtext)
    # print('车牌号api识别：', testcolorstr, testtextstr)
    return testcolorstr, testtextstr
