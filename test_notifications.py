#!/usr/bin/env python3
"""
测试 Bark 和 PushDeer 推送通知功能
"""
import os
import sys
import requests
from datetime import datetime
from dotenv import load_dotenv, find_dotenv

# 加载环境变量
load_dotenv(find_dotenv())


class BarkTester:
    """测试 Bark 推送服务"""
    def __init__(self, server_url):
        self.server_url = server_url.rstrip('/') if server_url else None
        self.name = "Bark"
    
    def test(self):
        """测试 Bark 推送"""
        if not self.server_url:
            return False, "❌ BARK_KEY 未配置"
        
        print(f"\n{'='*50}")
        print(f"测试 {self.name} 推送服务")
        print(f"{'='*50}")
        print(f"服务地址: {self.server_url}")
        
        # 测试1: 简单标题推送
        print("\n[测试 1] 发送简单标题...")
        title = "测试通知"
        url = f"{self.server_url}/{title}"
        
        try:
            response = requests.get(url, timeout=10)
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.text[:200]}")
            
            if response.status_code == 200:
                print("✅ 简单标题推送成功")
            else:
                return False, f"❌ 推送失败，状态码: {response.status_code}"
        except Exception as e:
            return False, f"❌ 请求失败: {str(e)}"
        
        # 测试2: 带内容的推送
        print("\n[测试 2] 发送标题+内容...")
        title = "IP更新通知"
        content = f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        url = f"{self.server_url}/{title}/{content}"
        
        try:
            response = requests.get(url, timeout=10)
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.text[:200]}")
            
            if response.status_code == 200:
                print("✅ 标题+内容推送成功")
                return True, "✅ Bark 推送服务正常"
            else:
                return False, f"❌ 推送失败，状态码: {response.status_code}"
        except Exception as e:
            return False, f"❌ 请求失败: {str(e)}"


class PushDeerTester:
    """测试 PushDeer 推送服务"""
    def __init__(self, pushkey):
        self.pushkey = pushkey
        self.api_url = "https://api2.pushdeer.com/message/push"
        self.name = "PushDeer"
    
    def test(self):
        """测试 PushDeer 推送"""
        if not self.pushkey:
            return False, "❌ PUSHDEER_KEY 未配置"
        
        print(f"\n{'='*50}")
        print(f"测试 {self.name} 推送服务")
        print(f"{'='*50}")
        print(f"API 地址: {self.api_url}")
        print(f"PushKey: {self.pushkey[:10]}...{self.pushkey[-6:]}")
        
        # 测试1: 简单文本推送
        print("\n[测试 1] 发送简单文本...")
        params = {
            'pushkey': self.pushkey,
            'text': '测试通知',
            'type': 'text'
        }
        
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.text[:200]}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    print("✅ 简单文本推送成功")
                else:
                    return False, f"❌ API 返回错误: {result.get('error', 'Unknown error')}"
            else:
                return False, f"❌ 推送失败，状态码: {response.status_code}"
        except Exception as e:
            return False, f"❌ 请求失败: {str(e)}"
        
        # 测试2: Markdown 格式推送
        print("\n[测试 2] 发送 Markdown 格式...")
        params = {
            'pushkey': self.pushkey,
            'text': '# IP更新通知',
            'desp': f'**测试时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n这是一条测试消息',
            'type': 'markdown'
        }
        
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.text[:200]}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    print("✅ Markdown 格式推送成功")
                    return True, "✅ PushDeer 推送服务正常"
                else:
                    return False, f"❌ API 返回错误: {result.get('error', 'Unknown error')}"
            else:
                return False, f"❌ 推送失败，状态码: {response.status_code}"
        except Exception as e:
            return False, f"❌ 请求失败: {str(e)}"


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print(" 📱 推送通知服务测试脚本")
    print("="*60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 从环境变量读取配置
    bark_key = os.getenv('BARK_KEY')
    pushdeer_key = os.getenv('PUSHDEER_KEY')
    
    print(f"\n配置状态:")
    print(f"  BARK_KEY: {'✓ 已配置' if bark_key else '✗ 未配置'}")
    print(f"  PUSHDEER_KEY: {'✓ 已配置' if pushdeer_key else '✗ 未配置'}")
    
    if not bark_key and not pushdeer_key:
        print("\n❌ 错误: 未找到任何推送服务配置")
        print("请在 .env 文件中配置 BARK_KEY 或 PUSHDEER_KEY")
        sys.exit(1)
    
    results = []
    
    # 测试 Bark
    if bark_key:
        bark_tester = BarkTester(bark_key)
        success, message = bark_tester.test()
        results.append(('Bark', success, message))
    else:
        print(f"\n{'='*50}")
        print("⏭️  跳过 Bark 测试（未配置）")
    
    # 测试 PushDeer
    if pushdeer_key:
        pushdeer_tester = PushDeerTester(pushdeer_key)
        success, message = pushdeer_tester.test()
        results.append(('PushDeer', success, message))
    else:
        print(f"\n{'='*50}")
        print("⏭️  跳过 PushDeer 测试（未配置）")
    
    # 输出测试结果汇总
    print("\n" + "="*60)
    print(" 📊 测试结果汇总")
    print("="*60)
    
    for service, success, message in results:
        status = "✅ 成功" if success else "❌ 失败"
        print(f"\n{service}: {status}")
        print(f"  {message}")
    
    # 统计
    total = len(results)
    passed = sum(1 for _, success, _ in results if success)
    
    print(f"\n{'='*60}")
    print(f"总计: {passed}/{total} 通过")
    print("="*60)
    
    # 返回退出码
    sys.exit(0 if passed == total else 1)


if __name__ == '__main__':
    main()
