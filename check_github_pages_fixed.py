#!/usr/bin/env python3
"""
检查 GitHub Pages 部署状态的脚本
"""

import requests
import time
import sys

def check_github_pages():
    url = "https://codemo1991.github.io/chris/"
    
    print("正在检查 GitHub Pages 部署状态...")
    print(f"博客地址: {url}")
    print("-" * 50)
    
    try:
        # 检查主页
        response = requests.get(url, timeout=10)
        print(f"状态码: {response.status_code}")
        print(f"内容类型: {response.headers.get('Content-Type', '未知')}")
        print(f"最后修改: {response.headers.get('Last-Modified', '未知')}")
        print(f"服务器: {response.headers.get('Server', '未知')}")
        
        if response.status_code == 200:
            print("\n[SUCCESS] GitHub Pages 正常运行！")
            
            # 检查是否包含热点模块
            if "每日热点" in response.text:
                print("[SUCCESS] 每日热点模块已部署")
            else:
                print("[WARNING] 每日热点模块可能未更新")
                
            # 检查是否有热点页面
            hotspots_url = "https://codemo1991.github.io/chris/hotspots.html"
            hotspots_response = requests.get(hotspots_url, timeout=10)
            if hotspots_response.status_code == 200:
                print("[SUCCESS] 热点页面已部署")
            else:
                print(f"[WARNING] 热点页面状态码: {hotspots_response.status_code}")
                
        else:
            print(f"\n[ERROR] GitHub Pages 可能有问题，状态码: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] 无法连接到 GitHub Pages: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("部署检查完成！")
    print("\n访问以下链接查看博客：")
    print(f"1. 主页: {url}")
    print(f"2. 热点页面: https://codemo1991.github.io/chris/hotspots.html")
    print(f"3. 今日热点详情: https://codemo1991.github.io/chris/posts/daily-hotspot-2026-02-22.html")
    
    return True

if __name__ == "__main__":
    print("GitHub Pages 部署检查工具")
    print("=" * 50)
    
    # 等待几秒钟让 GitHub Pages 更新
    print("等待 GitHub Pages 更新...")
    for i in range(3, 0, -1):
        print(f"等待 {i} 秒...")
        time.sleep(1)
    
    success = check_github_pages()
    
    if success:
        print("\n[SUCCESS] 恭喜！你的博客已成功部署到 GitHub Pages！")
        print("\n下一步：")
        print("1. 访问 https://codemo1991.github.io/chris/ 查看博客")
        print("2. 每天更新热点新闻：修改 index.html 中的热点内容")
        print("3. 添加新文章：在 posts/ 目录下创建新的 HTML 文件")
        print("4. 更新热点页面：运行 hotspot_tool_fixed.py 生成新的热点页面")
    else:
        print("\n[ERROR] 部署检查失败，请稍后重试")
        sys.exit(1)