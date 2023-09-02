# -*- coding: utf-8 -*-
# 森空岛-明日方舟签到活动 脚本
'''
new Env('森空岛-明日方舟');
33 6 * * * skland_arknights_checkin.py
'''
import requests
import os

# 请填写下方cred，uid，gameId的值，或在环境变量中填写skland_cred，skland_uid，skland_gameId的值，以环境变量中的为准
cred=""

if os.getenv("skland_cred"):
    cred = os.getenv("skland_cred")
if not cred:
    print("未填写cred")
    exit(0)

headers = {
    "cred": cred
}

def checkin(nickName,uid):
    url = "https://zonai.skland.com/api/v1/game/attendance"

    data = {
        "uid": uid,
        "gameId": 1
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200 & response.json()['code'] == 0:
        print(f'{nickName}签到成功，获得了{response.json()["resource"]["name"]}×{response.json()["count"]}\n')
    else:
        print(f"{nickName}签到失败:", response.status_code, response.reason,f'{response.json()["message"]}')


def get_bindingList():
    url="https://zonai.skland.com/api/v1/game/player/binding"

    response = requests.get(url, headers=headers)
    if response.json()['code'] == 0:
        print(response.json())
        for i in response.json()['data']['list']:
            if i['appCode'] == 'arknights':
                return i['bindingList']
                
    else:
        print(f"请求角色列表出现问题：{response.json()['message']}")
        if response.json()['message'] == '用户未登录':
            print(f'用户登录可能失效了，请更新cred！')

bindingList=get_bindingList()
for i in bindingList:
    checkin(i["nickName"],i["uid"])