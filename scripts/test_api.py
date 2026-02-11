#!/usr/bin/env python3
"""
简单的测试脚本 - 验证 Gemini API 和 Server 酱连接
"""

import os
import sys
import requests
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_gemini():
    """测试 Gemini API"""
    print("\n" + "=" * 60)
    print("🤖 测试 Gemini API")
    print("=" * 60)
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ 未设置 GEMINI_API_KEY")
        return False
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # 尝试列出可用模型
        print("📋 获取可用模型列表...")
        models = []
        try:
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    models.append(model.name)
                    print(f"   - {model.name}")
        except Exception as e:
            print(f"   ⚠️  无法列出模型: {e}")
        
        # 尝试使用 gemini-2.5-flash 生成内容
        print("\n🧪 测试内容生成...")
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Hello! Please respond with 'OK' if you can read this.")
        
        print(f"✅ Gemini API 响应成功:")
        print(f"   {response.text[:100]}")
        return True
        
    except Exception as e:
        print(f"❌ Gemini API 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_serverchan():
    """测试 Server 酱"""
    print("\n" + "=" * 60)
    print("📱 测试 Server 酱")
    print("=" * 60)
    
    sendkey = os.getenv('SERVERCHAN_KEY')
    if not sendkey:
        print("❌ 未设置 SERVERCHAN_KEY")
        return False
    
    url = f"https://sctapi.ftqq.com/{sendkey}.send"
    
    data = {
        "title": "🧪 测试消息",
        "desp": "这是来自 arXiv 论文系统的测试消息"
    }
    
    try:
        print("📤 发送测试消息...")
        response = requests.post(url, data=data, timeout=10, verify=False)
        result = response.json()
        
        if result.get('code') == 0:
            print(f"✅ Server 酱推送成功!")
            print(f"   Push ID: {result.get('data', {}).get('pushid', 'N/A')}")
            print(f"   请查收你的微信消息")
            return True
        else:
            print(f"❌ 推送失败: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Server 酱测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║          API 连接测试                                      ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    gemini_ok = test_gemini()
    serverchan_ok = test_serverchan()
    
    print("\n" + "=" * 60)
    print("📊 测试结果")
    print("=" * 60)
    print(f"Gemini API: {'✅ 通过' if gemini_ok else '❌ 失败'}")
    print(f"Server 酱:  {'✅ 通过' if serverchan_ok else '❌ 失败'}")
    print("=" * 60)
    
    sys.exit(0 if (gemini_ok and serverchan_ok) else 1)
