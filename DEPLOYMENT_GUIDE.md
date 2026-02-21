# GitHub Pages 部署指南

## 博客地址
- **主页**: https://codemo1991.github.io/chris/
- **热点页面**: https://codemo1991.github.io/chris/hotspots.html

## 部署状态
✅ 已成功部署到 GitHub Pages

## 如何更新博客

### 1. 本地修改
```bash
# 克隆仓库（如果还没有）
git clone https://github.com/codemo1991/chris.git
cd chris

# 修改文件
# 编辑 index.html, hotspots.html, css/style.css 等文件

# 添加新文章
# 在 posts/ 目录下创建新的 HTML 文件
```

### 2. 更新每日热点
每日热点模块位于 `index.html` 文件的以下位置：
```html
<section class="daily-hotspots">
    <!-- 热点1 -->
    <div class="hotspot-item">
        <div class="hotspot-rank top-3">1</div>
        <h3 class="hotspot-title">
            <a href="posts/daily-hotspot-2026-02-22.html#hotspot1">标题</a>
        </h3>
        <p class="hotspot-desc">描述</p>
        <div class="hotspot-meta">
            <span class="hotspot-source">来源</span>
            <span class="hotspot-date">日期</span>
        </div>
    </div>
    <!-- 热点2-5类似 -->
</section>
```

### 3. 使用热点工具
可以使用 `hotspot_tool_fixed.py` 工具生成新的热点页面：
```bash
python hotspot_tool_fixed.py
```

### 4. 提交并推送
```bash
# 添加所有更改
git add .

# 提交更改
git commit -m "更新每日热点：日期"

# 推送到 GitHub
git push origin main
```

### 5. 等待部署
GitHub Pages 通常会在几分钟内自动部署。可以通过以下方式检查：
```bash
python check_github_pages_fixed.py
```

## 文件结构说明
```
chris/
├── index.html              # 主页（包含每日热点模块）
├── hotspots.html           # 热点页面
├── posts/
│   └── daily-hotspot-2026-02-22.html  # 今日热点详情
├── css/
│   └── style.css          # 样式文件（包含热点样式）
├── js/
│   └── script.js          # JavaScript 文件
├── hotspot_tool_fixed.py   # 热点页面生成工具
├── check_github_pages_fixed.py  # 部署检查工具
└── .nojekyll              # GitHub Pages 配置文件
```

## 自动部署
GitHub Pages 会自动部署 `main` 分支的根目录。每次推送后：
1. GitHub 会自动构建和部署
2. 部署通常需要 1-5 分钟
3. 可以通过 https://github.com/codemo1991/chris/settings/pages 查看部署状态

## 常见问题

### 1. 页面没有更新
- 等待几分钟让 GitHub Pages 更新缓存
- 清除浏览器缓存
- 检查 `.nojekyll` 文件是否存在

### 2. 样式或脚本不生效
- 检查文件路径是否正确
- 确保 CSS 和 JS 文件已正确链接
- 检查浏览器控制台是否有错误

### 3. 热点模块不显示
- 确保 `index.html` 中的热点模块代码正确
- 检查 CSS 样式是否加载
- 验证热点数据格式是否正确

## 联系方式
- GitHub: https://github.com/codemo1991
- 博客: https://codemo1991.github.io/chris/

---
*最后更新: 2026年2月22日*