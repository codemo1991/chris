#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日热点管理工具
用于快速创建和更新每日热点文章
"""

import os
import json
import datetime
from pathlib import Path

def create_hotspot_article(date_str=None):
    """创建每日热点文章"""
    if date_str is None:
        date_str = datetime.date.today().strftime("%Y-%m-%d")
    
    # 示例热点数据
    hotspots = [
        {
            "rank": 1,
            "title": "OpenAI发布新一代多模态模型GPT-5",
            "desc": "OpenAI正式发布GPT-5，支持更强大的多模态理解和生成能力，在图像理解、视频分析、语音识别等方面都有显著提升。",
            "source": "OpenAI官方博客",
            "url": "https://openai.com/blog/gpt-5"
        },
        {
            "rank": 2,
            "title": "微软Copilot全面集成Windows 12",
            "desc": "微软宣布Copilot AI助手将深度集成到Windows 12操作系统中，作为系统级助手可以控制所有应用、文件管理和系统设置。",
            "source": "Microsoft Build大会",
            "url": "https://blogs.microsoft.com/build"
        },
        {
            "rank": 3,
            "title": "谷歌发布Gemini Ultra 2.0",
            "desc": "谷歌发布Gemini Ultra 2.0，在多项基准测试中超越GPT-5，在数学推理、代码生成和创意写作方面表现优异。",
            "source": "Google I/O大会",
            "url": "https://blog.google/technology/ai"
        },
        {
            "rank": 4,
            "title": "苹果Vision Pro销量突破100万台",
            "desc": "苹果宣布Vision Pro头显上市首月销量突破100万台，在企业和消费市场都获得成功，AR应用生态快速发展。",
            "source": "Apple财报会议",
            "url": "https://www.apple.com/newsroom"
        },
        {
            "rank": 5,
            "title": "Meta开源Llama 4 700B参数模型",
            "desc": "Meta开源其最大的语言模型Llama 4，包含7000亿参数，在多项开源基准测试中领先，支持商业使用。",
            "source": "Meta AI博客",
            "url": "https://ai.meta.com/blog"
        }
    ]
    
    # 生成HTML内容
    html_content = generate_hotspot_html(date_str, hotspots)
    
    # 保存文件
    filename = f"daily-hotspot-{date_str}.html"
    filepath = Path("posts") / filename
    
    os.makedirs("posts", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✅ 热点文章已创建: {filepath}")
    print(f"📅 日期: {date_str}")
    print(f"📊 包含 {len(hotspots)} 条热点新闻")
    
    return filepath

def generate_hotspot_html(date_str, hotspots):
    """生成热点文章HTML"""
    
    # 生成热点列表HTML
    hotspots_html = ""
    for hotspot in hotspots:
        rank_class = "top-3" if hotspot["rank"] <= 3 else ""
        hotspots_html += f'''
                <!-- 热点{hotspot['rank']} -->
                <div class="hotspot-item">
                    <div class="hotspot-rank {rank_class}">{hotspot['rank']}</div>
                    <h3 class="hotspot-title">
                        <a href="{hotspot['url']}" target="_blank">{hotspot['title']}</a>
                    </h3>
                    <p class="hotspot-desc">{hotspot['desc']}</p>
                    <div class="hotspot-meta">
                        <span>来源：{hotspot['source']}</span>
                        <a href="{hotspot['url']}" class="hotspot-source-link" target="_blank">查看原文 →</a>
                    </div>
                </div>
        '''
    
    # 生成详细分析
    analysis_html = ""
    for hotspot in hotspots:
        analysis_html += f'''
                <h4>{hotspot['rank']}. {hotspot['title']}</h4>
                <p>详细分析内容待补充...</p>
        '''
    
    # 完整HTML模板
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{date_str} IT热点新闻 | 我的技术博客</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .article-content {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem 0;
        }}
        
        .article-header {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        
        .article-title {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: var(--text-color);
        }}
        
        .article-meta {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            color: var(--text-color);
            opacity: 0.7;
            margin-bottom: 2rem;
        }}
        
        .hotspot-source {{
            display: inline-block;
            background-color: #f97316;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.875rem;
            font-weight: 500;
            margin-left: 1rem;
        }}
        
        .hotspot-list {{
            margin: 2rem 0;
        }}
        
        .hotspot-item {{
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: var(--transition);
        }}
        
        .hotspot-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
        }}
        
        .hotspot-rank {{
            display: inline-block;
            width: 2rem;
            height: 2rem;
            background-color: var(--primary-color);
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 2rem;
            font-weight: bold;
            margin-right: 1rem;
        }}
        
        .hotspot-rank.top-3 {{
            background-color: #ef4444;
        }}
        
        .hotspot-title {{
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
            color: var(--text-color);
        }}
        
        .hotspot-title a {{
            color: var(--text-color);
            text-decoration: none;
        }}
        
        .hotspot-title a:hover {{
            color: var(--primary-color);
        }}
        
        .hotspot-desc {{
            color: var(--text-color);
            opacity: 0.8;
            margin-bottom: 1rem;
            line-height: 1.6;
        }}
        
        .hotspot-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.875rem;
            color: var(--text-color);
            opacity: 0.7;
        }}
        
        .hotspot-source-link {{
            color: var(--primary-color);
            text-decoration: none;
        }}
        
        .hotspot-source-link:hover {{
            text-decoration: underline;
        }}
        
        .hotspot-detail {{
            background-color: var(--card-bg);
            border-left: 4px solid var(--primary-color);
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 0 0.5rem 0.5rem 0;
        }}
        
        .hotspot-detail h3 {{
            font-size: 1.2rem;
            margin-bottom: 1rem;
            color: var(--text-color);
        }}
        
        .hotspot-detail p {{
            margin-bottom: 1rem;
            line-height: 1.6;
        }}
        
        .back-to-hotspots {{
            display: inline-block;
            margin-top: 2rem;
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 500;
        }}
        
        .back-to-hotspots:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <header>
        <nav class="navbar">
            <div class="container">
                <a href="../index.html" class="logo">我的博客</a>
                <ul class="nav-links">
                    <li><a href="../index.html">首页</a></li>
                    <li><a href="../hotspots.html">热点</a></li>
                    <li><a href="../about.html">关于</a></li>
                    <li><a href="../archive.html">归档</a></li>
                    <li><a href="../tags.html">标签</a></li>
                    <li><a href="../contact.html">联系</a></li>
                </ul>
                <button class="theme-toggle" id="themeToggle">
                    <i class="fas fa-moon"></i>
                </button>
            </div>
        </nav>
    </header>

    <main class="container">
        <article class="article-content">
            <header class="article-header">
                <h1 class="article-title">{date_str} IT热点新闻</h1>
                <div class="article-meta">
                    <span><i class="far fa-calendar"></i> {date_str}</span>
                    <span><i class="far fa-clock"></i> 阅读时间：10分钟</span>
                    <span><i class="far fa-folder"></i> 每日热点</span>
                    <span class="hotspot-source">热点新闻</span>
                </div>
                <div class="tags">
                    <span class="tag">AI</span>
                    <span class="tag">科技新闻</span>
                    <span class="tag">行业动态</span>
                    <span class="tag">技术趋势</span>
                </div>
            </header>

            <div class="article-body">
                <p>今日精选5条最重要的IT行业热点新闻，涵盖AI、操作系统、硬件和开源技术等领域的最新动态。</p>

                <div class="hotspot-list">
                    {hotspots_html}
                </div>

                <div class="hotspot-detail">
                    <h3>详细分析</h3>
                    {analysis_html}
                </div>

                <p>以上是今日最重要的5条IT热点新闻。技术行业正在快速发展，AI、AR和开源技术将继续引领未来几年的创新方向。</p>

                <a href="../hotspots.html" class="back-to-hotspots">
                    <i class="fas fa-arrow-left"></i> 返回热点归档
                </a>
            </div>
        </article>
    </main>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>我的博客</h3>
                    <p>记录技术成长，分享开发经验</p>
                </div>
                <div class="footer-section">
                    <h3>链接</h3>
                    <ul>
                        <li><a href="../index.html">首页</a></li>
                        <li><a href="../hotspots.html">热点</a></li>
                        <li><a href="../archive.html">归档</a></li>
                        <li><a href="../tags.html">标签</a></li>
                        <li><a href="../rss.xml">RSS订阅</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>联系</h3>
                    <ul>
                        <li><a href="https://github.com/codemo1991"><i class="fab fa-github"></i> GitHub</a></li>
                        <li><a href="mailto:your.email@example.com"><i class="fas fa-envelope"></i> 邮箱</a></li>
                    </ul>
                </div>
            </div>
            <div class="copyright">
                <p>&copy; {date_str[:4]} 我的技术博客. 保留所有权利.</p>
            </div>
        </div>
    </footer>

    <script src="../js/script.js"></script>
</body>
</html>'''
    
    return html_template

def list_hotspot_articles():
    """列出所有热点文章"""
    posts_dir = Path("posts")
    if not posts_dir.exists():
        print("posts目录不存在")
        return []
    
    hotspot_files = []
    for file in posts_dir.glob("daily-hotspot-*.html"):
        # 从文件名提取日期
        date_str = file.stem.replace("daily-hotspot-", "")
        hotspot_files.append({
            "filename": file.name,
            "date": date_str,
            "path": str(file)
        })
    
    # 按日期排序（最新的在前）
    hotspot_files.sort(key=lambda x: x["date"], reverse=True)
    
    print(f"找到 {len(hotspot_files)} 篇热点文章:")
    for article in hotspot_files:
        print(f"  {article['date']} - {article['filename']}")
    
    return hotspot_files

def update_hotspots_page():
    """更新热点归档页面"""
    articles = list_hotspot_articles()
    
    if not articles:
        print("没有找到热点文章，无法更新归档页面")
        return
    
    # 读取热点归档页面模板
    hotspots_path = Path("hotspots.html")
    if not hotspots_path.exists():
        print("hotspots.html 文件不存在")
        return
    
    with open(hotspots_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 生成热点文章卡片HTML
    articles_html = ""
    for article in articles[:10]:  # 只显示最新的10篇
        articles_html += f'''
                <!-- 热点文章 -->
                <article class="hotspot-archive-card">
                    <span class="hotspot-archive-date">{article['date']}</span>
                    <h3 class="hotspot-archive-title">
                        <a href="posts/{article['filename']}">{article['date']} IT热点新闻</a>
                    </h3>
                    <p class="hotspot-archive-desc">今日精选5条最重要的IT行业热点新闻，涵盖AI、操作系统、硬件和开源技术等领域的最新动态。</p>
                    <div class="hotspot-archive-meta">
                        <span class="hotspot-count"><i class="fas fa-fire"></i> 5条热点</span>
                        <span>阅读时间：10分钟</span>
                    </div>
                </article>
        '''
    
    print("热点归档页面需要手动更新")
    print("请将以下HTML代码复制到 hotspots.html 的合适位置:")
    print("-" * 50)
    print(articles_html)
    print("-" * 50)

def main():
    """主函数"""
    print("每日热点管理工具")
    print("=" * 50)
    print("1. 创建今日热点文章")
    print("2. 创建指定日期热点文章")
    print("3. 列出所有热点文章")
    print("4. 更新热点归档页面")
    print("5. 退出")
    print("=" * 50)
    
    while True:
        try:
            choice = input("\n请选择操作 (1-5): ").strip()
            
            if choice == "1":
                # 创建今日热点
                create_hotspot_article()
                
            elif choice == "2":
                # 创建指定日期热点
                date_str = input("请输入日期 (格式: YYYY-MM-DD): ").strip()
                try:
                    datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    create_hotspot_article(date_str)
                except ValueError:
                    print("日期格式错误，请使用 YYYY-MM-DD 格式")
                    
            elif choice == "3":
                # 列出所有热点文章
                list_hotspot_articles()
                
            elif choice == "4":
                # 更新热点归档页面
                update_hotspots_page()
                
            elif choice == "5":
                print("再见！")
                break
                
            else:
                print("无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n用户中断，退出程序")
            break
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main()