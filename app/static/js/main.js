// Theme toggle functionality
function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.classList.contains('dark');
    
    if (isDark) {
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    }
}

// Initialize theme from localStorage
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.documentElement.classList.add('dark');
    }
}

// Newsletter subscription
function subscribeNewsletter() {
    const emailInput = document.getElementById('newsletter-email');
    const email = emailInput.value.trim();
    
    if (!email) {
        alert('Please enter your email address.');
        return;
    }
    
    if (!isValidEmail(email)) {
        alert('Please enter a valid email address.');
        return;
    }
    
    // In a real implementation, this would send to your newsletter service
    alert('Thanks for subscribing! (This is a demo - implement with ConvertKit, Mailchimp, etc.)');
    emailInput.value = '';
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Analytics helper (placeholder for real analytics)
function trackEvent(eventName, properties = {}) {
    console.log('Analytics Event:', eventName, properties);
    
    // In a real implementation, you'd send to Google Analytics, Mixpanel, etc.
    // Example:
    // gtag('event', eventName, properties);
    // mixpanel.track(eventName, properties);
}

// Page view tracking
function trackPageView() {
    const path = window.location.pathname;
    trackEvent('page_view', {
        page: path,
        title: document.title,
        url: window.location.href
    });
}

// Newsletter signup tracking
function trackNewsletterSignup() {
    trackEvent('newsletter_signup', {
        source: 'homepage'
    });
}

// Post click tracking
function trackPostClick(postTitle, postSlug) {
    trackEvent('post_click', {
        post_title: postTitle,
        post_slug: postSlug
    });
}

// Copy link functionality
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('Link copied to clipboard!');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showToast('Link copied to clipboard!');
    }
}

// Toast notification
function showToast(message, duration = 3000) {
    const toast = document.createElement('div');
    toast.className = 'fixed bottom-4 right-4 bg-gray-900 text-white px-4 py-2 rounded-lg shadow-lg z-50 transform transition-transform duration-300 translate-y-full';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => {
        toast.classList.remove('translate-y-full');
    }, 100);
    
    // Remove toast
    setTimeout(() => {
        toast.classList.add('translate-y-full');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, duration);
}

// Reading progress indicator
function initializeReadingProgress() {
    const article = document.querySelector('article');
    if (!article) return;
    
    const progressBar = document.createElement('div');
    progressBar.className = 'fixed top-0 left-0 h-1 bg-blue-600 z-50 transition-all duration-150';
    progressBar.style.width = '0%';
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
        const articleTop = article.offsetTop;
        const articleHeight = article.offsetHeight;
        const windowHeight = window.innerHeight;
        const scrollTop = window.pageYOffset;
        
        const start = articleTop - windowHeight / 2;
        const end = articleTop + articleHeight - windowHeight / 2;
        const progress = Math.max(0, Math.min(1, (scrollTop - start) / (end - start)));
        
        progressBar.style.width = `${progress * 100}%`;
    });
}

// Search functionality (placeholder)
function initializeSearch() {
    // This would implement client-side search or connect to a search API
    console.log('Search functionality would be initialized here');
}

// Performance monitoring
function initializePerformanceMonitoring() {
    if ('performance' in window) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                trackEvent('page_performance', {
                    loadTime: perfData.loadEventEnd - perfData.loadEventStart,
                    domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
                    firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0
                });
            }, 0);
        });
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    initializeSmoothScrolling();
    initializeReadingProgress();
    initializePerformanceMonitoring();
    trackPageView();
    
    // Add event listeners for newsletter signup
    const newsletterEmail = document.getElementById('newsletter-email');
    if (newsletterEmail) {
        newsletterEmail.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                subscribeNewsletter();
            }
        });
    }
});

// Handle system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
        if (e.matches) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }
});

// Export functions for use in templates
window.blogFunctions = {
    toggleTheme,
    subscribeNewsletter,
    trackEvent,
    trackPostClick,
    copyToClipboard,
    showToast
};
