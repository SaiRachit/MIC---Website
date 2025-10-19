// Enhanced Hover Effects for Events and Resources Pages
document.addEventListener('DOMContentLoaded', function() {
    
    // Add smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';
    
    // Enhanced hover effects for event cards
    const eventCards = document.querySelectorAll('.event-card');
    eventCards.forEach(card => {
        // Add mouse enter effect
        card.addEventListener('mouseenter', function() {
            // Add dramatic glow effect
            this.style.boxShadow = '0 30px 60px rgba(255, 107, 53, 0.4), 0 0 0 1px rgba(255, 107, 53, 0.3)';
            
            // Add stagger animation to overlay elements
            const overlay = this.querySelector('.event-overlay');
            if (overlay) {
                const elements = overlay.querySelectorAll('h3, p, .event-details');
                elements.forEach((element, index) => {
                    element.style.animationDelay = `${index * 0.15}s`;
                    element.style.animation = 'fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards';
                });
            }
        });
        
        // Add mouse leave effect
        card.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
            
            // Reset overlay animations
            const overlay = this.querySelector('.event-overlay');
            if (overlay) {
                const elements = overlay.querySelectorAll('h3, p, .event-details');
                elements.forEach(element => {
                    element.style.animation = '';
                });
            }
        });
    });
    
    // Enhanced hover effects for resource cards
    const resourceCards = document.querySelectorAll('.resource-card');
    resourceCards.forEach(card => {
        // Add mouse enter effect
        card.addEventListener('mouseenter', function() {
            // Add dramatic glow effect
            this.style.boxShadow = '0 30px 60px rgba(255, 107, 53, 0.4), 0 0 0 1px rgba(255, 107, 53, 0.3)';
            
            // Add stagger animation to overlay elements
            const overlay = this.querySelector('.resource-overlay');
            if (overlay) {
                const elements = overlay.querySelectorAll('h3, p, .resource-details');
                elements.forEach((element, index) => {
                    element.style.animationDelay = `${index * 0.15}s`;
                    element.style.animation = 'fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards';
                });
            }
        });
        
        // Add mouse leave effect
        card.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
            
            // Reset overlay animations
            const overlay = this.querySelector('.resource-overlay');
            if (overlay) {
                const elements = overlay.querySelectorAll('h3, p, .resource-details');
                elements.forEach(element => {
                    element.style.animation = '';
                });
            }
        });
    });
    
    // Add intersection observer for scroll animations
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
    
    // Observe all cards for scroll animations
    const allCards = document.querySelectorAll('.event-card, .resource-card');
    allCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94), transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        observer.observe(card);
    });
    
    // Add click effects for better interactivity
    allCards.forEach(card => {
        card.addEventListener('click', function() {
            // Add click ripple effect
            const ripple = document.createElement('div');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.3)';
            ripple.style.transform = 'scale(0)';
            ripple.style.animation = 'ripple 0.6s linear';
            ripple.style.left = '50%';
            ripple.style.top = '50%';
            ripple.style.width = '20px';
            ripple.style.height = '20px';
            ripple.style.marginLeft = '-10px';
            ripple.style.marginTop = '-10px';
            
            this.style.position = 'relative';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
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
    
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    /* Enhanced hover states */
    .event-card:hover .event-overlay h3,
    .resource-card:hover .resource-overlay h3 {
        animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
    }
    
    .event-card:hover .event-overlay p,
    .resource-card:hover .resource-overlay p {
        animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
        animation-delay: 0.15s;
    }
    
    .event-card:hover .event-overlay .event-details,
    .resource-card:hover .resource-overlay .resource-details {
        animation: fadeInUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
        animation-delay: 0.3s;
    }
    
    /* Smooth transitions for all interactive elements */
    .event-card,
    .resource-card {
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    /* Enhanced focus states for accessibility */
    .event-card:focus,
    .resource-card:focus {
        outline: 2px solid #ff6b35;
        outline-offset: 2px;
    }
`;
document.head.appendChild(style);
