// 主题切换功能
const themeToggle = document.getElementById('themeToggle');
const themeIcon = themeToggle.querySelector('i');

// 检查本地存储的主题设置
const currentTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', currentTheme);
updateThemeIcon(currentTheme);

// 主题切换事件
themeToggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
});

function updateThemeIcon(theme) {
    if (theme === 'dark') {
        themeIcon.className = 'fas fa-sun';
        themeIcon.title = '切换到亮色主题';
    } else {
        themeIcon.className = 'fas fa-moon';
        themeIcon.title = '切换到暗色主题';
    }
}

// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// 页面加载动画
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
    
    // 为文章卡片添加延迟显示动画
    const postCards = document.querySelectorAll('.post-card');
    postCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-in');
    });
});

// 添加一些交互效果
document.querySelectorAll('.post-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-4px)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
    });
});

// 添加CSS动画类
const style = document.createElement('style');
style.textContent = `
    .post-card {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.5s ease, transform 0.5s ease;
    }
    
    .post-card.animate-in {
        opacity: 1;
        transform: translateY(0);
    }
    
    body.loaded .post-card {
        animation: fadeInUp 0.5s ease forwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// 控制台欢迎信息
console.log('%c🎉 欢迎访问我的技术博客！', 'color: #2563eb; font-size: 16px; font-weight: bold;');
console.log('%c📚 这里分享编程、AI、Web开发等技术心得', 'color: #7c3aed; font-size: 14px;');

// 每日热点功能 - 静态版本
(function() {
    const trendsList = document.getElementById('trendsList');

    if (!trendsList) return;

    // 静态热点数据 - 请手动更新这里的内容
    const staticTrends = [
        {
            title: 'Claude 4 发布：AI 编程能力大幅提升',
            url: 'https://www.anthropic.com/news/claude-4',
            hotValue: '156万',
            desc: 'Anthropic 发布新一代 Claude 4 模型'
        },
        {
            title: 'React 19 正式版发布',
            url: 'https://react.dev/blog/2024/04/25/react-19',
            hotValue: '98万',
            desc: 'Server Components 正式可用'
        },
        {
            title: 'TypeScript 5.5 发布',
            url: 'https://devblogs.microsoft.com/typescript/announcing-typescript-5-5',
            hotValue: '87万',
            desc: '控制流 narrowing 改进'
        },
        {
            title: 'VS Code 1.90 发布',
            url: 'https://code.visualstudio.com/updates/v1_90',
            hotValue: '76万',
            desc: '更好的 AI 编程辅助'
        },
        {
            title: 'Node.js 22 发布',
            url: 'https://nodejs.org/en/blog/announcements/v22-release-announce',
            hotValue: '65万',
            desc: '支持运行 ES 模块'
        },
        {
            title: 'GitHub Copilot Workspace 发布',
            url: 'https://github.com/features/copilot',
            hotValue: '54万',
            desc: 'AI 驱动的代码审查工具'
        },
        {
            title: 'Rust 1.80 发布',
            url: 'https://blog.rust-lang.org/2024/07/25/Rust-1.80.0.html',
            hotValue: '43万',
            desc: '常量 trait 改进'
        },
        {
            title: 'Vercel AI SDK 4.0 发布',
            url: 'https://sdk.vercel.ai',
            hotValue: '38万',
            desc: '下一代 AI 应用开发框架'
        },
        {
            title: 'Docker Desktop 4.30 发布',
            url: 'https://www.docker.com/blog/docker-desktop-4-30',
            hotValue: '32万',
            desc: '资源管理优化'
        },
        {
            title: 'Next.js 15 RC 发布',
            url: 'https://nextjs.org/blog/next-15',
            hotValue: '28万',
            desc: 'TurboPack 稳定版'
        }
    ];

    // 格式化数字（热度值）
    function formatHotValue(value) {
        return value;
    }

    // 渲染热点列表
    function renderTrends(data) {
        if (!data || data.length === 0) {
            trendsList.innerHTML = '<div class="error"><i class="fas fa-exclamation-circle"></i> 暂无热点数据</div>';
            return;
        }

        const html = data.map((item, index) => {
            const rank = index + 1;
            const isTop3 = rank <= 3;
            const title = item.title || '未知标题';
            const url = item.url || '#';
            const hotValue = item.hotValue || '0';

            return `
                <a href="${url}" target="_blank" class="trend-item" title="${title}">
                    <span class="trend-rank ${isTop3 ? 'top-3' : ''}">${rank}</span>
                    <div class="trend-content">
                        <span class="trend-title">${title}</span>
                        <span class="trend-meta">${item.desc || ''}</span>
                    </div>
                    <span class="trend-hot"><i class="fas fa-fire"></i> ${formatHotValue(hotValue)}</span>
                </a>
            `;
        }).join('');

        trendsList.innerHTML = html;
    }

    // 直接使用静态数据渲染
    renderTrends(staticTrends);
})();