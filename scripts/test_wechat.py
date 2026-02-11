#!/usr/bin/env python3
"""测试 Server 酱微信推送"""
import requests
import urllib3
urllib3.disable_warnings()

url = 'https://sctapi.ftqq.com/SCT314197TaQOHppVo3SJgbNvDZjhRXpRA.send'
proxies = {'http': 'http://127.0.0.1:7897', 'https': 'http://127.0.0.1:7897'}
data = {'title': '🧪 Python测试', 'desp': '来自Python的测试消息，Server酱推送成功！'}

r = requests.post(url, data=data, timeout=10, verify=False, proxies=proxies)
print('Status:', r.status_code)
print('Body:', r.text)
