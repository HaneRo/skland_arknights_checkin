# -*- coding: utf-8 -*-
# 森空岛-明日方舟签到活动 脚本
'''
new Env('森空岛-明日方舟');
33 6 * * * skland_arknights_checkin.py
'''
import requests
import os

# 请填写下方cred的值，或在环境变量中填写skland_cred，以环境变量中的为准
cred=""

if os.getenv("skland_cred"):
    cred = os.getenv("skland_cred")
if not cred:
    print("未填写cred")
    exit(0)

headers = {
    "cred": cred,
    "vName": "1.0.1",
    "vCode": "100001014",
    'Accept-Encoding': 'gzip',
    'Connection': 'close',
    "dId": "de9759a5afaa634f",
    "platform": "1",
    "user-agent": "Skland/1.0.1 (com.hypergryph.skland; build:100001014; Android 33; ) Okhttp/4.11.0"
}

def checkin(nickName,uid,gameId):
    url = "https://zonai.skland.com/api/v1/game/attendance"

    data = {
        "uid": uid,
        "gameId": gameId
    }

    response = requests.post(url, headers=headers, json=data)
    if response.json()['code'] == 0:
        for award in response.json().get('data', {}).get('awards', []):
            count = award.get('count', None)
            name = award.get('resource', {}).get('name', None)
            print(f'{nickName}签到成功，获得了{name}×{count}\n')
    else:
        print(f"{nickName}签到失败:", response.status_code, response.reason,f'{response.json()["message"]}')

def isCheckined(uid,gameId):
    url = f"https://zonai.skland.com/api/v1/game/attendance?gameId={gameId}&uid={uid}"

    response = requests.get(url, headers=headers)

    # 检查"data"和"calendar"键是否存在，并获取"calendar"列表
    if "data" in response.json() and "calendar" in response.json()["data"]:
        calendar_list = response.json()["data"]["calendar"]
        
        # 遍历"calendar"列表，检查是否有"available"为True的项
        for item in calendar_list:
            if item.get("available", False):
                return True
        else:
            return False
    else:
        print("ERROR 未获取到签到记录")
        return False

def get_bindingList():
    url="https://zonai.skland.com/api/v1/game/player/binding"

    response = requests.get(url, headers=headers)
    if response.json()['code'] == 0:
        for i in response.json()['data']['list']:
            if i['appCode'] == 'arknights':
                return i['bindingList']
                
    else:
        print(f"请求角色列表出现问题：{response.json()['message']}")
        if response.json()['message'] == '用户未登录':
            print(f'用户登录可能失效了，请更新cred！')

bindingList=get_bindingList()
for i in bindingList:
    if isCheckined(i["uid"],i["channelMasterId"]):
        checkin(i["nickName"],i["uid"],i["channelMasterId"])
    else:
        print(f'{i["nickName"]}已签到')