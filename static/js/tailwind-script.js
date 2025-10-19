// Smooth scrolling for navigation links
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

// Enhanced liquid glass navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('nav > div');
    const scrollY = window.scrollY;
    
    if (scrollY > 50) {
        navbar.style.background = 'rgba(255, 255, 255, 0.25)';
        navbar.style.backdropFilter = 'blur(25px)';
        navbar.style.boxShadow = '0 12px 40px rgba(31, 38, 135, 0.5)';
        navbar.style.border = '1px solid rgba(255, 255, 255, 0.3)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.1)';
        navbar.style.backdropFilter = 'blur(20px)';
        navbar.style.boxShadow = '0 8px 32px rgba(31, 38, 135, 0.37)';
        navbar.style.border = '1px solid rgba(255, 255, 255, 0.2)';
    }
});

// Mobile menu toggle
const mobileMenuButton = document.querySelector('nav button');
let mobileMenuOpen = false;

if (mobileMenuButton) {
    mobileMenuButton.addEventListener('click', () => {
        mobileMenuOpen = !mobileMenuOpen;
        
        if (mobileMenuOpen) {
            // Create mobile menu
            const mobileMenu = document.createElement('div');
            mobileMenu.className = 'fixed inset-0 z-40 bg-black bg-opacity-50 backdrop-blur-sm';
            mobileMenu.innerHTML = `
                <div class="fixed top-20 left-4 right-4 bg-white bg-opacity-20 backdrop-blur-2xl rounded-3xl p-8 border border-white border-opacity-30">
                    <div class="space-y-6">
                        <a href="index-tailwind.html#home" class="block text-white text-xl font-medium hover:text-orange-300 transition-colors">Home</a>
                        <a href="about.html" class="block text-white text-xl font-medium hover:text-orange-300 transition-colors">About Us</a>
                        <a href="events.html" class="block text-white text-xl font-medium hover:text-orange-300 transition-colors">Events</a>
                        <a href="resources.html" class="block text-white text-xl font-medium hover:text-orange-300 transition-colors">Resources</a>
                        <a href="contact.html" class="block text-white text-xl font-medium hover:text-orange-300 transition-colors">Contact</a>
                        <button class="w-full bg-gradient-to-r from-orange-primary to-orange-secondary text-white px-6 py-3 rounded-full font-medium mt-6">
                            Get Started
                        </button>
                    </div>
                </div>
            `;
            document.body.appendChild(mobileMenu);
            
            // Close on click outside
            mobileMenu.addEventListener('click', (e) => {
                if (e.target === mobileMenu) {
                    document.body.removeChild(mobileMenu);
                    mobileMenuOpen = false;
                }
            });
            
            // Close on link click
            mobileMenu.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', () => {
                    document.body.removeChild(mobileMenu);
                    mobileMenuOpen = false;
                });
            });
        }
    });
}

// Newsletter form submission
const newsletterForm = document.querySelector('footer form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = this.querySelector('input[type="email"]').value;
        
        if (email && validateEmail(email)) {
            // Submit to backend API
            fetch('/api/newsletter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email
                })
            })
            .then(response => response.json())
            .then(result => {
                if (result.message) {
                    // Create success message
                    const successMsg = document.createElement('div');
                    successMsg.className = 'fixed top-24 right-6 bg-green-500 text-white px-6 py-4 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300';
                    successMsg.textContent = result.message;
                    document.body.appendChild(successMsg);
                    
                    // Animate in
                    setTimeout(() => {
                        successMsg.style.transform = 'translateX(0)';
                    }, 100);
                    
                    // Animate out and remove
                    setTimeout(() => {
                        successMsg.style.transform = 'translateX(full)';
                        setTimeout(() => {
                            document.body.removeChild(successMsg);
                        }, 300);
                    }, 3000);
                    
                    this.querySelector('input[type="email"]').value = '';
                } else {
                    throw new Error('Failed to subscribe');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Show error
                const errorMsg = document.createElement('div');
                errorMsg.className = 'fixed top-24 right-6 bg-red-500 text-white px-6 py-4 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300';
                errorMsg.textContent = 'Sorry, there was an error subscribing. Please try again later.';
                document.body.appendChild(errorMsg);
                
                setTimeout(() => {
                    errorMsg.style.transform = 'translateX(0)';
                }, 100);
                
                setTimeout(() => {
                    errorMsg.style.transform = 'translateX(full)';
                    setTimeout(() => {
                        document.body.removeChild(errorMsg);
                    }, 300);
                }, 3000);
            });
        } else {
            // Show error
            const errorMsg = document.createElement('div');
            errorMsg.className = 'fixed top-24 right-6 bg-red-500 text-white px-6 py-4 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300';
            errorMsg.textContent = 'Please enter a valid email address';
            document.body.appendChild(errorMsg);
            
            setTimeout(() => {
                errorMsg.style.transform = 'translateX(0)';
            }, 100);
            
            setTimeout(() => {
                errorMsg.style.transform = 'translateX(full)';
                setTimeout(() => {
                    document.body.removeChild(errorMsg);
                }, 300);
            }, 3000);
        }
    });
}

// Email validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Enhanced card hover effects
document.addEventListener('DOMContentLoaded', () => {
    // Animate resource cards on scroll
    const resourceCards = document.querySelectorAll('#resources .grid > div');
    resourceCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `all 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });
    
    // Animate feature items
    const featureItems = document.querySelectorAll('#about .space-y-6 > div');
    featureItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-30px)';
        item.style.transition = `all 0.6s ease ${index * 0.2}s`;
        observer.observe(item);
    });
    
    // Enhanced resource card interactions
    resourceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.03)';
            this.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '';
        });
    });
});

// Parallax effect for hero background elements
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroBlobs = document.querySelectorAll('#home .absolute');
    
    heroBlobs.forEach((blob, index) => {
        const speed = (index + 1) * 0.2;
        blob.style.transform = `translateY(${scrolled * speed}px)`;
    });
});

// Stats counter animation
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        element.textContent = Math.floor(start);
        
        if (start < target) {
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    }
    
    updateCounter();
}

// Initialize counter animation when stats come into view
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumber = entry.target.querySelector('.text-6xl');
            if (statNumber && !statNumber.classList.contains('animated')) {
                statNumber.classList.add('animated');
                if (statNumber.textContent === '90') {
                    animateCounter(statNumber, 90);
                }
            }
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const statItems = document.querySelectorAll('#home .text-center');
    statItems.forEach(item => {
        statsObserver.observe(item);
    });
});

// Enhanced liquid glass effect on scroll
document.addEventListener('scroll', () => {
    const nav = document.querySelector('nav > div');
    const scrollY = window.scrollY;
    
    // Dynamic blur and opacity based on scroll
    const blurAmount = Math.min(25 + scrollY * 0.1, 40);
    const opacity = Math.min(0.1 + scrollY * 0.001, 0.3);
    
    nav.style.backdropFilter = `blur(${blurAmount}px)`;
    nav.style.background = `rgba(255, 255, 255, ${opacity})`;
});

// Add loading animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Magnetic effect for CTA buttons
document.querySelectorAll('button, .bg-gradient-to-r').forEach(button => {
    button.addEventListener('mousemove', (e) => {
        const rect = button.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        button.style.transform = `translate(${x * 0.1}px, ${y * 0.1}px) scale(1.05)`;
    });
    
    button.addEventListener('mouseleave', () => {
        button.style.transform = 'translate(0px, 0px) scale(1)';
    });
});

// Clean website interactions without cursor effects
// All other interactive elements remain for optimal user experience
