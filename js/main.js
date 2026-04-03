// Interactivity for SHINTRADING Academy

document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.getElementById('navbar');
    
    // Navbar Scroll Effect
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Smooth Scrolling for Anchors
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Intersection Observer for Slide-in Animations
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Dynamic Blog Loading
    const blogContainer = document.getElementById('blog-container');
    if (blogContainer) {
        fetch('data/posts.json')
            .then(res => res.json())
            .then(posts => {
                blogContainer.innerHTML = ''; // Clear existing
                posts.forEach(post => {
                    const article = document.createElement('article');
                    article.className = 'glass-card';
                    article.style.padding = '0';
                    article.style.overflow = 'hidden';
                    article.style.opacity = '0';
                    article.style.transform = 'translateY(30px)';
                    article.style.transition = 'all 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
                    
                    article.innerHTML = `
                        <img src="${post.image}" alt="${post.title}" style="width: 100%; height: 200px; object-fit: cover;">
                        <div style="padding: 2rem;">
                            <span style="color: var(--primary-color); font-size: 0.8rem; font-weight: 600;">${post.category}</span>
                            <h3 style="margin: 1rem 0;">${post.title}</h3>
                            <p style="color: var(--text-muted);">${post.description}</p>
                            <a href="blog/post.html?id=${post.id}" style="color: var(--primary-color); text-decoration: none; display: inline-block; margin-top: 1.5rem; font-weight: 600;">Đọc tiếp →</a>
                        </div>
                    `;
                    blogContainer.appendChild(article);
                    observer.observe(article);
                });
            })
            .catch(err => console.error('Error loading posts:', err));
    }

    // Static Cards Animation
    document.querySelectorAll('.glass-card:not(#blog-container .glass-card)').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
        observer.observe(card);
    });
});
