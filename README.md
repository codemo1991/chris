# 我的技术博客

这是一个使用 GitHub Pages 搭建的个人技术博客，专注于分享编程、AI、Web开发等技术心得。

## 🌟 特性

- **响应式设计**：完美适配桌面和移动设备
- **暗色/亮色主题**：支持一键切换
- **现代化界面**：简洁美观的UI设计
- **快速加载**：优化的静态资源
- **SEO友好**：良好的搜索引擎优化
- **易于维护**：纯静态文件，无需数据库

## 📁 项目结构

```
github-blog/
├── index.html          # 首页
├── about.html          # 关于页面
├── archive.html        # 文章归档
├── tags.html           # 标签页面
├── contact.html        # 联系页面
├── css/
│   └── style.css       # 样式文件
├── js/
│   └── script.js       # JavaScript文件
├── posts/              # 文章目录
│   ├── first-post.html # 示例文章
│   └── ...             # 更多文章
├── images/             # 图片资源
├── README.md           # 项目说明
└── CNAME              # 自定义域名配置（可选）
```

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/yourusername.github.io.git
cd yourusername.github.io
```

### 2. 本地预览
直接在浏览器中打开 `index.html` 文件，或使用本地服务器：
```bash
# 使用 Python
python -m http.server 8000

# 或使用 Node.js
npx serve .
```

### 3. 自定义配置
1. 修改 `index.html` 中的个人信息
2. 更新 `css/style.css` 调整样式
3. 编辑 `js/script.js` 添加交互功能
4. 在 `posts/` 目录下添加新文章

### 4. 部署到 GitHub Pages
1. 将代码推送到 GitHub 仓库
2. 在仓库设置中启用 GitHub Pages
3. 访问 `https://yourusername.github.io`

## 📝 添加新文章

1. 在 `posts/` 目录下创建新的 HTML 文件
2. 使用以下模板结构：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章标题 | 我的技术博客</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <!-- 导航栏 -->
    <header>
        <nav class="navbar">
            <!-- 导航内容 -->
        </nav>
    </header>

    <main class="container">
        <article class="article-content">
            <!-- 文章内容 -->
        </article>
    </main>

    <!-- 页脚 -->
    <footer>
        <!-- 页脚内容 -->
    </footer>

    <script src="../js/script.js"></script>
</body>
</html>
```

3. 在首页的 `post-grid` 部分添加文章链接

## 🎨 自定义主题

### 修改颜色主题
编辑 `css/style.css` 中的 CSS 变量：
```css
:root {
    --primary-color: #2563eb;      /* 主色调 */
    --secondary-color: #7c3aed;    /* 辅助色 */
    --text-color: #1f2937;         /* 文字颜色 */
    --bg-color: #ffffff;           /* 背景颜色 */
    --card-bg: #f9fafb;            /* 卡片背景 */
    --border-color: #e5e7eb;       /* 边框颜色 */
}
```

### 添加新功能
1. **评论系统**：集成 Disqus 或 Giscus
2. **搜索功能**：添加静态搜索或使用 Algolia
3. **分析工具**：集成 Google Analytics
4. **RSS订阅**：生成 RSS 订阅源

## 🔧 技术栈

- **HTML5**：语义化标记
- **CSS3**：现代样式和动画
- **JavaScript**：交互功能
- **Font Awesome**：图标库
- **GitHub Pages**：免费托管

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 📞 联系

- 邮箱：your.email@example.com
- GitHub：[@yourusername](https://github.com/yourusername)
- 博客：https://yourusername.github.io

---

**Happy Coding!** 🚀