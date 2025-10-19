// API Integration for MAHE Innovation Centre
// Handles dynamic content loading and API interactions

class MICAPI {
    constructor() {
        this.baseURL = '/api';
    }

    // Fetch events from API
    async fetchEvents() {
        try {
            const response = await fetch(`${this.baseURL}/events`);
            if (!response.ok) throw new Error('Failed to fetch events');
            return await response.json();
        } catch (error) {
            console.error('Error fetching events:', error);
            return [];
        }
    }

    // Fetch resources from API
    async fetchResources() {
        try {
            const response = await fetch(`${this.baseURL}/resources`);
            if (!response.ok) throw new Error('Failed to fetch resources');
            return await response.json();
        } catch (error) {
            console.error('Error fetching resources:', error);
            return [];
        }
    }

    // Submit contact form
    async submitContact(formData) {
        try {
            const response = await fetch(`${this.baseURL}/contact`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            return await response.json();
        } catch (error) {
            console.error('Error submitting contact form:', error);
            throw error;
        }
    }

    // Subscribe to newsletter
    async subscribeNewsletter(email) {
        try {
            const response = await fetch(`${this.baseURL}/newsletter`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email })
            });
            return await response.json();
        } catch (error) {
            console.error('Error subscribing to newsletter:', error);
            throw error;
        }
    }

    // Download resource and track download
    async downloadResource(resourceId) {
        try {
            const response = await fetch(`${this.baseURL}/resources/${resourceId}/download`, {
                method: 'POST'
            });
            return await response.json();
        } catch (error) {
            console.error('Error downloading resource:', error);
            throw error;
        }
    }
}

// Initialize API instance
const micAPI = new MICAPI();

// Dynamic content loading for homepage
document.addEventListener('DOMContentLoaded', function() {
    // Load recent events for homepage
    loadRecentEvents();
    
    // Load featured resources for homepage
    loadFeaturedResources();
    
    // Initialize event listeners
    initializeEventListeners();
});

// Load recent events for homepage display
async function loadRecentEvents() {
    try {
        const events = await micAPI.fetchEvents();
        const recentEvents = events.slice(0, 3); // Get first 3 events
        
        // Update events section on homepage if it exists
        const eventsSection = document.querySelector('#events .space-y-8');
        if (eventsSection && recentEvents.length > 0) {
            eventsSection.innerHTML = '';
            recentEvents.forEach((event, index) => {
                const eventElement = createEventElement(event, index + 1);
                eventsSection.appendChild(eventElement);
            });
        }
    } catch (error) {
        console.error('Error loading recent events:', error);
    }
}

// Load featured resources for homepage display
async function loadFeaturedResources() {
    try {
        const resources = await micAPI.fetchResources();
        const featuredResources = resources.filter(resource => resource.is_featured).slice(0, 3);
        
        // Update resources section on homepage if it exists
        const resourcesSection = document.querySelector('#resources .grid');
        if (resourcesSection && featuredResources.length > 0) {
            // Update resource cards with dynamic content
            const resourceCards = resourcesSection.querySelectorAll('.bg-white, .bg-gray-900');
            featuredResources.forEach((resource, index) => {
                if (resourceCards[index]) {
                    updateResourceCard(resourceCards[index], resource, index + 1);
                }
            });
        }
    } catch (error) {
        console.error('Error loading featured resources:', error);
    }
}

// Create event element for homepage
function createEventElement(event, number) {
    const eventDiv = document.createElement('div');
    eventDiv.className = 'flex items-start space-x-4';
    eventDiv.innerHTML = `
        <div class="w-10 h-10 bg-white rounded-full flex items-center justify-center flex-shrink-0 text-orange-primary font-bold">${number}</div>
        <p class="text-white/90 leading-relaxed">${event.title}</p>
    `;
    return eventDiv;
}

// Update resource card with dynamic content
function updateResourceCard(card, resource, number) {
    const titleElement = card.querySelector('h3');
    const descriptionElement = card.querySelector('p');
    const linkElement = card.querySelector('a');
    
    if (titleElement) titleElement.textContent = resource.title;
    if (descriptionElement) descriptionElement.textContent = resource.description.substring(0, 100) + '...';
    if (linkElement) {
        linkElement.href = '#';
        linkElement.addEventListener('click', (e) => {
            e.preventDefault();
            handleResourceClick(resource);
        });
    }
}

// Handle resource click/download
async function handleResourceClick(resource) {
    try {
        // Track download
        await micAPI.downloadResource(resource.id);
        
        // Show download success message
        showNotification('success', `Downloading ${resource.title}...`);
        
        // If there's a file URL, trigger download
        if (resource.file_url) {
            const link = document.createElement('a');
            link.href = resource.file_url;
            link.download = resource.title;
            link.click();
        }
    } catch (error) {
        console.error('Error handling resource click:', error);
        showNotification('error', 'Failed to download resource. Please try again.');
    }
}

// Initialize event listeners
function initializeEventListeners() {
    // Newsletter subscription
    const newsletterForms = document.querySelectorAll('#newsletterForm');
    newsletterForms.forEach(form => {
        form.addEventListener('submit', handleNewsletterSubscription);
    });
    
    // Contact form submission
    const contactForms = document.querySelectorAll('#contactForm');
    contactForms.forEach(form => {
        form.addEventListener('submit', handleContactSubmission);
    });
}

// Handle newsletter subscription
async function handleNewsletterSubscription(e) {
    e.preventDefault();
    const form = e.target;
    const email = form.querySelector('input[type="email"]').value;
    
    if (!email) {
        showNotification('error', 'Please enter an email address.');
        return;
    }
    
    try {
        const result = await micAPI.subscribeNewsletter(email);
        showNotification('success', result.message);
        form.reset();
    } catch (error) {
        console.error('Newsletter subscription error:', error);
        showNotification('error', 'Failed to subscribe. Please try again.');
    }
}

// Handle contact form submission
async function handleContactSubmission(e) {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    
    const data = {
        name: formData.get('fullName'),
        email: formData.get('email'),
        subject: formData.get('requestType'),
        message: formData.get('message'),
        phone: formData.get('phone') || '',
        company: formData.get('company') || ''
    };
    
    // Validate required fields
    if (!data.name || !data.email || !data.subject || !data.message) {
        showNotification('error', 'Please fill in all required fields.');
        return;
    }
    
    try {
        const result = await micAPI.submitContact(data);
        showNotification('success', `Thank you ${data.name}! We've received your message and will respond within 1-2 working days.`);
        form.reset();
    } catch (error) {
        console.error('Contact submission error:', error);
        showNotification('error', 'Failed to send message. Please try again.');
    }
}

// Show notification
function showNotification(type, message) {
    const notification = document.createElement('div');
    notification.className = `fixed top-24 right-6 px-6 py-4 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300 ${
        type === 'success' ? 'bg-green-500' : 'bg-red-500'
    } text-white`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Animate out and remove
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Export for use in other scripts
window.MICAPI = micAPI;
window.showNotification = showNotification;
