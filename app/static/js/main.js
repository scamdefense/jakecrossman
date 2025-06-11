// ===== MOBILE NAVIGATION =====
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navToggle.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }
});

// ===== SMOOTH SCROLLING =====
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

// ===== NAVBAR SCROLL EFFECT =====
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(10, 10, 10, 0.98)';
    } else {
        navbar.style.background = 'rgba(10, 10, 10, 0.95)';
    }
});

// ===== INTERSECTION OBSERVER FOR ANIMATIONS =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', function() {
    const animateElements = document.querySelectorAll('.highlight-card, .skill-category, .news-item, .gallery-item');
    animateElements.forEach(el => {
        observer.observe(el);
    });
});

// ===== CONTACT FORM HANDLING =====
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(this);
        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });
        
        // Simple validation
        if (!formObject.name || !formObject.email || !formObject.message) {
            showNotification('Please fill in all required fields.', 'error');
            return;
        }
        
        if (!isValidEmail(formObject.email)) {
            showNotification('Please enter a valid email address.', 'error');
            return;
        }
        
        // Simulate form submission (replace with actual backend endpoint)
        showNotification('Thank you for your message! I will get back to you soon.', 'success');
        this.reset();
    });
}

// ===== EMAIL VALIDATION =====
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// ===== NOTIFICATION SYSTEM =====
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notif => notif.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#007bff'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 10000;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
        max-width: 400px;
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Close button functionality
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        removeNotification(notification);
    });
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        removeNotification(notification);
    }, 5000);
}

function removeNotification(notification) {
    notification.style.opacity = '0';
    notification.style.transform = 'translateX(100%)';
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 300);
}

// ===== GALLERY LIGHTBOX =====
function initGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const img = this.querySelector('img');
            if (img) {
                openLightbox(img.src, img.alt);
            }
        });
    });
}

function openLightbox(src, alt) {
    // Create lightbox overlay
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox-overlay';
    lightbox.innerHTML = `
        <div class="lightbox-content">
            <img src="${src}" alt="${alt}" class="lightbox-image">
            <button class="lightbox-close">&times;</button>
            <div class="lightbox-caption">${alt}</div>
        </div>
    `;
    
    // Add styles
    lightbox.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    document.body.appendChild(lightbox);
    document.body.style.overflow = 'hidden';
    
    // Animate in
    setTimeout(() => {
        lightbox.style.opacity = '1';
    }, 100);
    
    // Close functionality
    const closeBtn = lightbox.querySelector('.lightbox-close');
    closeBtn.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function(e) {
        if (e.target === this) {
            closeLightbox();
        }
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', handleLightboxKeydown);
    
    function closeLightbox() {
        lightbox.style.opacity = '0';
        setTimeout(() => {
            if (lightbox.parentNode) {
                lightbox.parentNode.removeChild(lightbox);
            }
            document.body.style.overflow = '';
            document.removeEventListener('keydown', handleLightboxKeydown);
        }, 300);
    }
    
    function handleLightboxKeydown(e) {
        if (e.key === 'Escape') {
            closeLightbox();
        }
    }
}

// ===== LAZY LOADING =====
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// ===== TYPING ANIMATION =====
function initTypingAnimation() {
    const typingElements = document.querySelectorAll('.typing-text');
    
    typingElements.forEach(element => {
        const text = element.textContent;
        element.textContent = '';
        element.style.opacity = '1';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        
        // Start typing when element comes into view
        const typingObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    typeWriter();
                    typingObserver.unobserve(entry.target);
                }
            });
        });
        
        typingObserver.observe(element);
    });
}

// ===== PARALLAX SCROLLING =====
function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const rate = scrolled * -0.5;
            element.style.transform = `translateY(${rate}px)`;
        });
    });
}

// ===== RESUME FUNCTIONALITY =====
function initResume() {
    const printBtn = document.getElementById('print-resume');
    const toggleBtn = document.getElementById('toggle-layout');
    const resumeContainer = document.getElementById('resume-container');
    
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            // Optimize for print
            document.body.classList.add('printing');
            
            // Use browser's print functionality
            window.print();
            
            // Remove print class after printing
            setTimeout(() => {
                document.body.classList.remove('printing');
            }, 1000);
        });
    }
    
    if (toggleBtn && resumeContainer) {
        toggleBtn.addEventListener('click', function() {
            const isModern = resumeContainer.classList.contains('resume-layout-modern');
            
            if (isModern) {
                resumeContainer.classList.remove('resume-layout-modern');
                resumeContainer.classList.add('resume-layout-classic');
                toggleBtn.innerHTML = '<i class="fas fa-columns"></i> Modern Layout';
            } else {
                resumeContainer.classList.remove('resume-layout-classic');
                resumeContainer.classList.add('resume-layout-modern');
                toggleBtn.innerHTML = '<i class="fas fa-file-alt"></i> Classic Layout';
            }
        });
    }
}

// ===== RESUME PAGE ANIMATIONS =====
function initResumeAnimations() {
    const resumeElements = document.querySelectorAll('.credit-item, .highlight-item, .skill-category, .metric');
    
    const resumeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                entry.target.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                
                resumeObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    resumeElements.forEach(el => resumeObserver.observe(el));
}

// ===== DOWNLOAD RESUME AS PDF =====
function downloadResumeAsPDF() {
    // Create a clean version for PDF generation
    const resumeClone = document.getElementById('resume-container').cloneNode(true);
    
    // Create a new window for the PDF
    const printWindow = window.open('', '_blank');
    
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Jake Crossman - Resume</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
                
                * { margin: 0; padding: 0; box-sizing: border-box; }
                
                body {
                    font-family: 'Inter', sans-serif;
                    background: white;
                    color: #333;
                    line-height: 1.6;
                    font-size: 14px;
                }
                
                .resume-layout-modern {
                    display: grid;
                    grid-template-columns: 300px 1fr;
                    min-height: 100vh;
                    max-width: 1000px;
                    margin: 0;
                }
                
                .resume-sidebar {
                    background: #2a2a2a;
                    color: white;
                    padding: 2rem 1.5rem;
                }
                
                .resume-main {
                    padding: 2rem;
                    background: white;
                }
                
                .resume-name {
                    font-family: 'Playfair Display', serif;
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: white;
                    margin-bottom: 1rem;
                }
                
                .resume-title {
                    font-family: 'Playfair Display', serif;
                    font-size: 2rem;
                    font-weight: 700;
                    color: #333;
                    margin-bottom: 1rem;
                }
                
                .resume-section h3 {
                    color: #d4af37;
                    font-size: 1rem;
                    font-weight: 600;
                    margin-bottom: 1rem;
                    text-transform: uppercase;
                    border-bottom: 2px solid #d4af37;
                    padding-bottom: 0.3rem;
                }
                
                .credit-item, .highlight-item, .skill-category {
                    margin-bottom: 1rem;
                    padding: 1rem;
                    border: 1px solid #eee;
                    border-radius: 4px;
                }
                
                .credit-title { font-weight: 600; color: #333; }
                .credit-year { color: #d4af37; font-weight: 600; }
                .credit-role { color: #555; }
                .credit-type { color: #777; font-style: italic; }
                
                @page { margin: 0.5in; }
            </style>
        </head>
        <body>
            ${resumeClone.outerHTML}
        </body>
        </html>
    `);
    
    printWindow.document.close();
    
    // Wait for content to load, then print
    setTimeout(() => {
        printWindow.print();
        printWindow.close();
    }, 500);
}

// ===== ENHANCED PRINT STYLES =====
function addPrintStylesForResume() {
    const printStyles = `
        @media print {
            @page {
                margin: 0.5in;
                size: letter;
            }
            
            body.printing .resume-controls,
            body.printing .navbar,
            body.printing .footer {
                display: none !important;
            }
            
            body.printing .resume-layout-modern {
                display: grid !important;
                grid-template-columns: 250px 1fr !important;
                box-shadow: none !important;
                border: none !important;
                margin: 0 !important;
                background: white !important;
                color: black !important;
                font-size: 12px !important;
            }
            
            body.printing .resume-sidebar {
                background: #f8f9fa !important;
                color: black !important;
                border: 1px solid #ddd !important;
                padding: 1rem !important;
            }
            
            body.printing .resume-main {
                background: white !important;
                color: black !important;
                padding: 1rem !important;
            }
            
            body.printing .resume-name,
            body.printing .resume-title {
                color: black !important;
                background: none !important;
                -webkit-text-fill-color: black !important;
            }
            
            body.printing .resume-section h3 {
                color: #333 !important;
                border-bottom-color: #333 !important;
            }
            
            body.printing .credit-year {
                background: #f0f0f0 !important;
                color: #333 !important;
            }
            
            body.printing .credit-item,
            body.printing .highlight-item,
            body.printing .skill-category,
            body.printing .metric {
                break-inside: avoid !important;
                page-break-inside: avoid !important;
                background: white !important;
                border: 1px solid #ddd !important;
                margin-bottom: 0.5rem !important;
            }
        }
    `;
    
    const styleElement = document.createElement('style');
    styleElement.textContent = printStyles;
    document.head.appendChild(styleElement);
}

// ===== INITIALIZE ALL FUNCTIONS =====
document.addEventListener('DOMContentLoaded', function() {
    initGallery();
    initLazyLoading();
    initTypingAnimation();
    initParallax();
    initResume();
    initResumeAnimations();
    addPrintStylesForResume();
    
    // Add loading animation
    document.body.classList.add('loaded');
});

// ===== PERFORMANCE OPTIMIZATION =====
// Debounce function for scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Optimize scroll events
const optimizedScroll = debounce(() => {
    // Scroll-based animations go here
}, 16); // ~60fps

window.addEventListener('scroll', optimizedScroll);

// ===== ERROR HANDLING =====
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // You could send error reports to a logging service here
});

// ===== PROGRESSIVE ENHANCEMENT =====
// Check for browser capabilities and provide fallbacks
if (!window.IntersectionObserver) {
    // Fallback for older browsers
    document.querySelectorAll('.fade-in, .slide-up').forEach(el => {
        el.classList.add('visible');
    });
}