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
      // Add styles for overlay
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
        padding: 2rem;
        box-sizing: border-box;
    `;
    
    // Add styles for lightbox content
    const lightboxContent = lightbox.querySelector('.lightbox-content');
    lightboxContent.style.cssText = `
        position: relative;
        max-width: 35%;
        max-height: 35%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    `;
      // Add styles for the image
    const lightboxImage = lightbox.querySelector('.lightbox-image');
    lightboxImage.style.cssText = `
        max-width: 50%;
        max-height: 50%;
        width: auto;
        height: auto;
        object-fit: contain;
        border-radius: 8px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
    `;
    
    // Add styles for close button
    const closeButton = lightbox.querySelector('.lightbox-close');
    closeButton.style.cssText = `
        position: absolute;
        top: -3rem;
        right: -1rem;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: none;
        font-size: 2rem;
        width: 3rem;
        height: 3rem;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.3s ease;
        backdrop-filter: blur(10px);
    `;
    
    // Add styles for caption
    const caption = lightbox.querySelector('.lightbox-caption');
    caption.style.cssText = `
        margin-top: 1rem;
        color: #cccccc;
        text-align: center;
        font-size: 1rem;
        max-width: 500px;
        line-height: 1.4;
    `;
      // Add hover effect for close button
    closeButton.addEventListener('mouseenter', () => {
        closeButton.style.background = 'rgba(255, 255, 255, 0.3)';
    });
    closeButton.addEventListener('mouseleave', () => {
        closeButton.style.background = 'rgba(255, 255, 255, 0.2)';
    });
      // Add mobile responsiveness
    function updateLightboxForMobile() {
        if (window.innerWidth <= 768) {
            lightbox.style.padding = '2rem';
            lightboxImage.style.maxWidth = 'calc(100% - 4rem)';
            lightboxImage.style.maxHeight = 'calc(100% - 8rem)';
            closeButton.style.top = '-2.5rem';
            closeButton.style.right = '0';
            closeButton.style.fontSize = '1.5rem';
            closeButton.style.width = '2.5rem';
            closeButton.style.height = '2.5rem';
            caption.style.fontSize = '0.9rem';
            caption.style.margin = '0.8rem 0 0 0';
        } else {
            lightbox.style.padding = '4rem';
            lightboxImage.style.maxWidth = 'calc(100% - 4rem)';
            lightboxImage.style.maxHeight = 'calc(100% - 8rem)';
        }
    }
    
    // Apply mobile styles initially and on resize
    updateLightboxForMobile();
    window.addEventListener('resize', updateLightboxForMobile);
    
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
            window.removeEventListener('resize', updateLightboxForMobile);
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
    
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            // Use the enhanced PDF download function
            downloadResumeAsPDF();
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
    
    // Remove any interactive elements
    const buttons = resumeClone.querySelectorAll('button');
    buttons.forEach(btn => btn.remove());
    
    // Create a new window for the PDF with enhanced styling
    const printWindow = window.open('', '_blank', 'width=1200,height=800');
    
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Jake Crossman - Professional Resume</title>
            <meta charset="UTF-8">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
                
                * { 
                    margin: 0; 
                    padding: 0; 
                    box-sizing: border-box; 
                }
                
                body {
                    font-family: 'Inter', sans-serif;
                    background: white;
                    color: #333;
                    line-height: 1.5;
                    font-size: 12px;
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
                
                .resume-layout-modern {
                    display: grid;
                    grid-template-columns: 280px 1fr;
                    min-height: 100vh;
                    max-width: 210mm;
                    margin: 0 auto;
                    background: white;
                    box-shadow: none;
                }
                
                .resume-sidebar {
                    background: #2c3e50 !important;
                    color: white !important;
                    padding: 2rem 1.5rem;
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
                
                .resume-main {
                    padding: 2rem 1.8rem;
                    background: white;
                    color: #333;
                }
                
                .resume-name {
                    font-family: 'Playfair Display', serif;
                    font-size: 1.4rem;
                    font-weight: 700;
                    color: white !important;
                    margin-bottom: 1rem;
                    line-height: 1.2;
                    -webkit-print-color-adjust: exact;
                }
                
                .resume-title {
                    font-family: 'Playfair Display', serif;
                    font-size: 1.8rem;
                    font-weight: 700;
                    color: #2c3e50 !important;
                    margin-bottom: 1rem;
                    line-height: 1.2;
                }
                
                .resume-tagline {
                    font-size: 0.95rem;
                    line-height: 1.5;
                    color: #555;
                    margin-bottom: 1.5rem;
                }
                
                .resume-contact p {
                    display: flex;
                    align-items: center;
                    gap: 0.6rem;
                    font-size: 0.85rem;
                    color: #ecf0f1 !important;
                    margin-bottom: 0.6rem;
                    -webkit-print-color-adjust: exact;
                }
                
                .resume-contact i {
                    color: #f39c12 !important;
                    width: 14px;
                    font-size: 0.8rem;
                    -webkit-print-color-adjust: exact;
                }
                
                .resume-section {
                    margin-bottom: 2rem;
                    page-break-inside: avoid;
                }
                
                .resume-sidebar .resume-section h3 {
                    color: #f39c12 !important;
                    font-size: 0.9rem;
                    font-weight: 600;
                    margin-bottom: 1rem;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    border-bottom: 2px solid #f39c12;
                    padding-bottom: 0.3rem;
                    -webkit-print-color-adjust: exact;
                }
                
                .resume-main .resume-section h3 {
                    color: #2c3e50 !important;
                    font-size: 1.1rem;
                    font-weight: 600;
                    margin-bottom: 1.2rem;
                    display: flex;
                    align-items: center;
                    gap: 0.6rem;
                    border-bottom: 1px solid #bdc3c7;
                    padding-bottom: 0.3rem;
                }
                
                .resume-main .resume-section h3 i {
                    color: #f39c12 !important;
                    font-size: 0.9rem;
                    -webkit-print-color-adjust: exact;
                }
                
                .stats-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 0.8rem;
                }
                
                .stat-item {
                    display: flex;
                    flex-direction: column;
                    gap: 0.2rem;
                }
                
                .stat-label {
                    font-size: 0.75rem;
                    color: #bdc3c7 !important;
                    font-weight: 500;
                    -webkit-print-color-adjust: exact;
                }
                
                .stat-value {
                    font-size: 0.85rem;
                    color: white !important;
                    font-weight: 600;
                    -webkit-print-color-adjust: exact;
                }
                
                .impact-metrics {
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }
                
                .metric {
                    text-align: center;
                    padding: 1rem;
                    background: rgba(243, 156, 18, 0.15) !important;
                    border: 1px solid #f39c12;
                    border-radius: 6px;
                    -webkit-print-color-adjust: exact;
                }
                
                .metric-number {
                    display: block;
                    font-size: 1.2rem;
                    font-weight: 700;
                    color: #f39c12 !important;
                    margin-bottom: 0.3rem;
                    -webkit-print-color-adjust: exact;
                }
                
                .metric-label {
                    font-size: 0.7rem;
                    color: white !important;
                    line-height: 1.2;
                    -webkit-print-color-adjust: exact;
                }
                
                .highlights-list,
                .credits-list {
                    display: flex;
                    flex-direction: column;
                    gap: 1rem;
                }
                
                .highlight-item {
                    padding: 1rem;
                    background: #f8f9fa !important;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    border-left: 4px solid #f39c12;
                    page-break-inside: avoid;
                    -webkit-print-color-adjust: exact;
                }
                
                .highlight-item strong {
                    color: #2c3e50 !important;
                    font-weight: 600;
                    -webkit-print-color-adjust: exact;
                }
                
                .credit-item {
                    padding: 1rem;
                    background: #fdfdfd !important;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    page-break-inside: avoid;
                    -webkit-print-color-adjust: exact;
                }
                
                .credit-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 0.6rem;
                }
                
                .credit-title {
                    font-size: 0.95rem;
                    font-weight: 600;
                    color: #2c3e50 !important;
                    -webkit-print-color-adjust: exact;
                }
                
                .credit-year {
                    font-size: 0.8rem;
                    color: #f39c12 !important;
                    font-weight: 600;
                    background: rgba(243, 156, 18, 0.1) !important;
                    padding: 0.2rem 0.6rem;
                    border-radius: 3px;
                    -webkit-print-color-adjust: exact;
                }
                
                .credit-details {
                    display: flex;
                    flex-direction: column;
                    gap: 0.3rem;
                }
                
                .credit-role {
                    font-size: 0.85rem;
                    color: #555 !important;
                    font-weight: 500;
                    -webkit-print-color-adjust: exact;
                }
                
                .credit-type {
                    font-size: 0.8rem;
                    color: #777 !important;
                    font-style: italic;
                    -webkit-print-color-adjust: exact;
                }
                
                .skills-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                    gap: 1rem;
                }
                
                .skill-category {
                    padding: 1rem;
                    background: #f8f9fa !important;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    page-break-inside: avoid;
                    -webkit-print-color-adjust: exact;
                }
                
                .skill-category h4 {
                    color: #2c3e50 !important;
                    font-size: 0.85rem;
                    font-weight: 600;
                    margin-bottom: 0.6rem;
                    text-transform: uppercase;
                    letter-spacing: 0.3px;
                    -webkit-print-color-adjust: exact;
                }
                
                .skill-category p {
                    color: #555 !important;
                    font-size: 0.8rem;
                    line-height: 1.4;
                    margin: 0;
                    -webkit-print-color-adjust: exact;
                }
                
                .representation-note {
                    color: #777 !important;
                    font-style: italic;
                    text-align: center;
                    padding: 1rem;
                    background: #f8f9fa !important;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    margin: 0;
                    -webkit-print-color-adjust: exact;
                }
                
                @page { 
                    margin: 0.5in; 
                    size: letter;
                }
                
                @media print {
                    body { 
                        background: white !important;
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                    }
                    
                    .resume-sidebar {
                        background: #2c3e50 !important;
                        color: white !important;
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                    }
                    
                    * {
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                    }
                }
            </style>
        </head>
        <body>
            ${resumeClone.outerHTML}
        </body>
        </html>
    `);
    
    printWindow.document.close();
    
    // Wait for fonts and content to load, then print
    setTimeout(() => {
        printWindow.focus();
        printWindow.print();
        
        // Close the window after a delay to allow print dialog to open
        setTimeout(() => {
            printWindow.close();
        }, 1000);
    }, 800);
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

// ===== SMART IMAGE SUPPORT =====
function initSmartImages() {
    // Check browser support for WebP
    function supportsWebP() {
        return new Promise((resolve) => {
            const webP = new Image();
            webP.onload = webP.onerror = function () {
                resolve(webP.height === 2);
            };
            webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
        });
    }

    // Initialize image loading optimization
    async function setupImageOptimization() {
        const webpSupported = await supportsWebP();
        
        // Add class to body to indicate WebP support
        if (webpSupported) {
            document.body.classList.add('webp-supported');
        } else {
            document.body.classList.add('webp-not-supported');
        }

        // Setup lazy loading for smart images
        const images = document.querySelectorAll('img[loading="lazy"]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            });

            images.forEach(img => {
                imageObserver.observe(img);
            });
        } else {
            // Fallback for older browsers
            images.forEach(img => {
                img.classList.add('loaded');
            });
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupImageOptimization);
    } else {
        setupImageOptimization();
    }
}

// ===== CUSTOM VIDEO PLAY BUTTON =====
function initVideoPlayButtons() {
    // Find all video containers with play overlays
    const videoContainers = document.querySelectorAll('.video-container');
    
    videoContainers.forEach(container => {
        const video = container.querySelector('video');
        const playOverlay = container.querySelector('.video-play-overlay');
        
        if (!video || !playOverlay) return;
        
        // Initially show the overlay
        playOverlay.style.display = 'flex';
        
        // Handle play overlay click
        playOverlay.addEventListener('click', function() {
            video.play();
            container.classList.add('playing');
        });
        
        // Handle video play event
        video.addEventListener('play', function() {
            container.classList.add('playing');
        });
        
        // Handle video pause event
        video.addEventListener('pause', function() {
            container.classList.remove('playing');
        });
        
        // Handle video ended event
        video.addEventListener('ended', function() {
            container.classList.remove('playing');
        });
        
        // Handle when video can play through (loaded enough)
        video.addEventListener('canplaythrough', function() {
            // Video is ready to play - this helps avoid the spinning wheel
            console.log('Video ready to play');
        });
        
        // Handle video loading states
        video.addEventListener('loadstart', function() {
            console.log('Video loading started');
        });
        
        video.addEventListener('loadeddata', function() {
            console.log('Video data loaded');
        });
    });
}

// Initialize smart images
initSmartImages();

// ===== INITIALIZE ALL FUNCTIONS =====
document.addEventListener('DOMContentLoaded', function() {
    initGallery();
    initLazyLoading();
    initTypingAnimation();
    initParallax();
    initResume();
    initResumeAnimations();
    addPrintStylesForResume();
    initVideoPlayButtons(); // Add this line
    
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