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
    
    // 为热点卡片添加延迟显示动画
    const hotspotCards = document.querySelectorAll('.hotspot-card');
    hotspotCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate-in');
    });
    
    // 更新每日热点日期
    updateDailyHotspotDate();
});

// 更新每日热点日期
function updateDailyHotspotDate() {
    const dateBadge = document.querySelector('.date-badge');
    if (dateBadge) {
        const now = new Date();
        const year = now.getFullYear();
        const month = now.getMonth() + 1;
        const day = now.getDate();
        dateBadge.textContent = `${year}年${month}月${day}日`;
    }
}

// 添加一些交互效果
document.querySelectorAll('.post-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-4px)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
    });
});

// 热点卡片交互效果
document.querySelectorAll('.hotspot-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateX(4px)';
    });
    
    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateX(0)';
    });
});

// 添加CSS动画类
const style = document.createElement('style');
style.textContent = `
    .post-card, .hotspot-card {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.5s ease, transform 0.5s ease;
    }
    
    .post-card.animate-in, .hotspot-card.animate-in {
        opacity: 1;
        transform: translateY(0);
    }
    
    body.loaded .post-card,
    body.loaded .hotspot-card {
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
    
    /* 热点卡片排名动画 */
    .hotspot-rank {
        transition: transform 0.3s ease;
    }
    
    .hotspot-card:hover .hotspot-rank {
        transform: scale(1.1);
    }
    
    /* 热点卡片边框动画 */
    .hotspot-card {
        position: relative;
        overflow: hidden;
    }
    
    .hotspot-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
        transition: left 0.5s ease;
    }
    
    .hotspot-card:hover::before {
        left: 100%;
    }
`;
document.head.appendChild(style);

// 控制台欢迎信息
console.log('%c🎉 欢迎访问我的技术博客！', 'color: #2563eb; font-size: 16px; font-weight: bold;');
console.log('%c📚 这里分享编程、AI、Web开发等技术心得', 'color: #7c3aed; font-size: 14px;');
console.log('%c🔥 每日热点已更新，关注最新IT动态', 'color: #ff6b6b; font-size: 14px;');

// 模拟热点数据更新（实际项目中可以从API获取）
function simulateHotspotUpdate() {
    console.log('%c🔄 每日热点数据更新中...', 'color: #4d96ff; font-size: 14px;');
    
    // 这里可以添加从API获取热点数据的逻辑
    // 例如：
    // fetch('/api/daily-hotspots')
    //     .then(response => response.json())
    //     .then(data => updateHotspotCards(data))
    //     .catch(error => console.error('热点数据更新失败:', error));
}

// 页面加载后模拟一次热点更新
setTimeout(simulateHotspotUpdate, 2000);

// 添加键盘快捷键
document.addEventListener('keydown', (e) => {
    // Alt + T 切换主题
    if (e.altKey && e.key === 't') {
        themeToggle.click();
    }
    
    // Alt + H 滚动到热点区域
    if (e.altKey && e.key === 'h') {
        const hotspotSection = document.getElementById('daily-hotspots');
        if (hotspotSection) {
            window.scrollTo({
                top: hotspotSection.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    }
});

// 显示键盘快捷键提示
console.log('%c⌨️ 键盘快捷键:', 'color: #6bcf7f; font-size: 14px;');
console.log('%c  Alt + T: 切换主题', 'color: #999; font-size: 12px;');
console.log('%c  Alt + H: 跳转到每日热点', 'color: #999; font-size: 12px;');