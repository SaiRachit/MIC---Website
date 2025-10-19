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
const mobileMenuButton = document.getElementById('mobile-menu-btn');
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
                        <a href="index.html" class="block text-white text-xl font-medium hover:text-orange-300 transition-colors">Home</a>
                        <a href="#about" class="block text-white text-xl font-medium hover:text-orange-300 transition-colors">About Us</a>
                        <a href="events.html" class="block text-white text-xl font-medium hover:text-orange-300 transition-colors">Events</a>
                        <a href="resources.html" class="block text-white text-xl font-medium hover:text-orange-300 transition-colors">Resources</a>
                        <a href="#contact" class="block text-orange-300 text-xl font-medium">Contact Us</a>
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

// Contact form validation and submission
const contactForm = document.getElementById('contactForm');
const responseModal = document.getElementById('responseModal');
const modalIcon = document.getElementById('modalIcon');
const modalTitle = document.getElementById('modalTitle');
const modalMessage = document.getElementById('modalMessage');
const modalClose = document.getElementById('modalClose');

// Email validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Show modal
function showModal(type, title, message) {
    if (type === 'success') {
        modalIcon.className = 'w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center bg-green-100';
        modalIcon.innerHTML = '<i class="fas fa-check text-2xl text-green-600"></i>';
    } else {
        modalIcon.className = 'w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center bg-red-100';
        modalIcon.innerHTML = '<i class="fas fa-times text-2xl text-red-600"></i>';
    }
    
    modalTitle.textContent = title;
    modalMessage.textContent = message;
    responseModal.classList.remove('hidden');
    responseModal.classList.add('flex');
    
    // Add smooth entrance animation
    setTimeout(() => {
        responseModal.querySelector('div').style.transform = 'scale(1)';
        responseModal.querySelector('div').style.opacity = '1';
    }, 10);
}

// Close modal
modalClose.addEventListener('click', () => {
    responseModal.classList.add('hidden');
    responseModal.classList.remove('flex');
});

// Close modal on backdrop click
responseModal.addEventListener('click', (e) => {
    if (e.target === responseModal) {
        responseModal.classList.add('hidden');
        responseModal.classList.remove('flex');
    }
});

// Contact form submission
contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(this);
    const data = {
        fullName: formData.get('fullName'),
        email: formData.get('email'),
        requestType: formData.get('requestType'),
        message: formData.get('message'),
        terms: formData.get('terms')
    };
    
    // Validation
    if (!data.fullName.trim()) {
        showModal('error', 'Validation Error', 'Please enter your full name.');
        return;
    }
    
    if (!validateEmail(data.email)) {
        showModal('error', 'Validation Error', 'Please enter a valid email address.');
        return;
    }
    
    if (!data.requestType) {
        showModal('error', 'Validation Error', 'Please select a type of request.');
        return;
    }
    
    if (!data.message.trim()) {
        showModal('error', 'Validation Error', 'Please enter your message.');
        return;
    }
    
    if (!data.terms) {
        showModal('error', 'Validation Error', 'Please agree to the terms of service.');
        return;
    }
    
    // Show loading state
    const submitButton = this.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Sending...';
    submitButton.disabled = true;
    submitButton.classList.add('opacity-75');
    
    // Submit to backend API
    fetch('/api/contact', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: data.fullName,
            email: data.email,
            subject: data.requestType,
            message: data.message,
            phone: '', // Add phone field if needed
            company: '' // Add company field if needed
        })
    })
    .then(response => response.json())
    .then(result => {
        // Reset button
        submitButton.textContent = originalText;
        submitButton.disabled = false;
        submitButton.classList.remove('opacity-75');
        
        if (result.message) {
            // Show success message
            showModal('success', 'Message Sent!', `Thank you ${data.fullName}! We've received your message and will respond within 1-2 working days.`);
            
            // Reset form
            this.reset();
            
            // Reset floating labels
            document.querySelectorAll('.form-input').forEach(input => {
                input.value = '';
            });
        } else {
            throw new Error('Failed to send message');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        
        // Reset button
        submitButton.textContent = originalText;
        submitButton.disabled = false;
        submitButton.classList.remove('opacity-75');
        
        // Show error message
        showModal('error', 'Error', 'Sorry, there was an error sending your message. Please try again later.');
    });
});

// Newsletter form submission
const newsletterForm = document.getElementById('newsletterForm');
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
                    showToast('success', result.message);
                    this.querySelector('input[type="email"]').value = '';
                } else {
                    throw new Error('Failed to subscribe');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('error', 'Sorry, there was an error subscribing. Please try again later.');
            });
        } else {
            showToast('error', 'Please enter a valid email address.');
        }
    });
}

// Toast notification function
function showToast(type, message) {
    const toast = document.createElement('div');
    toast.className = `fixed top-24 right-6 px-6 py-4 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300 ${
        type === 'success' ? 'bg-green-500' : 'bg-red-500'
    } text-white`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Animate out and remove
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (document.body.contains(toast)) {
                document.body.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

// Enhanced form interactions
document.addEventListener('DOMContentLoaded', () => {
    // Add focus effects to form inputs
    const formInputs = document.querySelectorAll('.form-input, input, textarea, select');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.transform = 'scale(1.02)';
            this.style.boxShadow = '0 8px 25px rgba(255, 107, 53, 0.15)';
        });
        
        input.addEventListener('blur', function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '';
        });
    });
    
    // Add hover effects to buttons
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            if (!this.disabled) {
                this.style.transform = 'translateY(-2px)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Character counter for textarea
    const messageTextarea = document.getElementById('message');
    if (messageTextarea) {
        const counterDiv = document.createElement('div');
        counterDiv.className = 'text-sm text-gray-500 mt-1 text-right';
        counterDiv.textContent = '0/500';
        messageTextarea.parentNode.appendChild(counterDiv);
        
        messageTextarea.addEventListener('input', function() {
            const length = this.value.length;
            const maxLength = 500;
            counterDiv.textContent = `${length}/${maxLength}`;
            
            if (length > maxLength) {
                counterDiv.className = 'text-sm text-red-500 mt-1 text-right';
                this.value = this.value.substring(0, maxLength);
            } else if (length > maxLength * 0.9) {
                counterDiv.className = 'text-sm text-orange-500 mt-1 text-right';
            } else {
                counterDiv.className = 'text-sm text-gray-500 mt-1 text-right';
            }
        });
    }
});

// Smooth scroll for any anchor links
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

// Add loading animation
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

// Form field validation in real-time
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('input[required], textarea[required], select[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            // Clear validation styling on input
            this.classList.remove('border-red-500', 'border-green-500');
        });
    });
});

function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    
    if (field.type === 'email') {
        isValid = validateEmail(value);
    } else if (field.hasAttribute('required')) {
        isValid = value !== '';
    }
    
    if (isValid) {
        field.classList.remove('border-red-500');
        field.classList.add('border-green-500');
    } else {
        field.classList.remove('border-green-500');
        field.classList.add('border-red-500');
    }
    
    return isValid;
}

// Keyboard navigation enhancements
document.addEventListener('keydown', (e) => {
    // Escape key closes modal
    if (e.key === 'Escape' && !responseModal.classList.contains('hidden')) {
        responseModal.classList.add('hidden');
        responseModal.classList.remove('flex');
    }
    
    // Enter key on modal close button
    if (e.key === 'Enter' && document.activeElement === modalClose) {
        modalClose.click();
    }
});

// Auto-resize textarea
const textareas = document.querySelectorAll('textarea');
textareas.forEach(textarea => {
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });
});

// Chatbot functionality is now handled by chatbot.js
