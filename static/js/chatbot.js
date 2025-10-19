// ===========================================
// Enhanced Chatbot Widget for MAHE Innovation Centre
// ===========================================

(function initChatbot() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupChatbot);
    } else {
        setupChatbot();
    }

    function setupChatbot() {
        // Create floating chat button
        const chatBtn = document.createElement('button');
        chatBtn.id = 'chatbot-toggle';
        chatBtn.className = 'fixed z-[60] bottom-6 right-6 w-16 h-16 rounded-full shadow-2xl flex items-center justify-center bg-gradient-to-br from-orange-primary to-orange-secondary text-white hover:scale-110 transition-all duration-300 hover:shadow-orange-500/50';
        chatBtn.setAttribute('aria-label', 'Open chat assistant');
        chatBtn.innerHTML = `
            <i class="fa-solid fa-comments text-2xl"></i>
            <span id="chat-notification" class="hidden absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full text-xs flex items-center justify-center font-bold animate-pulse">1</span>
        `;
        document.body.appendChild(chatBtn);

        // Create chat window
        const chatWindow = document.createElement('div');
        chatWindow.id = 'chatbot-window';
        chatWindow.className = 'fixed z-[60] bottom-24 right-6 w-[360px] md:w-[420px] h-[580px] rounded-2xl overflow-hidden shadow-[0_25px_80px_rgba(0,0,0,0.4)] transform translate-y-8 scale-95 opacity-0 pointer-events-none transition-all duration-300 ease-out';
        
        chatWindow.innerHTML = `
            <div class="h-full flex flex-col bg-white">
                <!-- Header -->
                <div class="bg-gradient-to-r from-orange-primary to-orange-secondary text-white px-5 py-4 flex items-center justify-between shadow-lg">
                    <div class="flex items-center gap-3">
                        <div class="relative">
                            <div class="w-10 h-10 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center border-2 border-white/40">
                                <i class="fa-solid fa-robot text-white text-lg"></i>
                            </div>
                            <div class="absolute bottom-0 right-0 w-3 h-3 bg-green-400 rounded-full border-2 border-white"></div>
                        </div>
                        <div>
                            <h3 class="font-bold text-base">MiC Assistant</h3>
                            <p class="text-xs text-white/80">Online • Typically replies instantly</p>
                        </div>
                    </div>
                    <button id="chatbot-close" class="text-white/80 hover:text-white hover:bg-white/20 rounded-lg p-2 transition-colors" aria-label="Close chat">
                        <i class="fa-solid fa-xmark text-xl"></i>
                    </button>
                </div>

                <!-- Chat Messages Area -->
                <div class="flex-1 overflow-y-auto bg-gradient-to-br from-gray-50 to-gray-100 p-4" id="chatbot-messages-container">
                    <!-- Welcome Message -->
                    <div class="flex gap-3 mb-4 animate-fade-in">
                        <div class="w-8 h-8 rounded-full bg-gradient-to-br from-orange-primary to-orange-secondary flex items-center justify-center flex-shrink-0">
                            <i class="fa-solid fa-robot text-white text-sm"></i>
                        </div>
                        <div class="flex-1">
                            <div class="bg-white rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm border border-gray-200">
                                <p class="text-sm text-gray-800 leading-relaxed">
                                    Hi! 👋 I'm the MiC Assistant. I can help you with:
                                </p>
                                <ul class="mt-2 space-y-1 text-xs text-gray-600">
                                    <li>• Event information</li>
                                    <li>• Resources and programs</li>
                                    <li>• General inquiries</li>
                                </ul>
                            </div>
                            <p class="text-xs text-gray-400 mt-1 ml-1">Just now</p>
                        </div>
                    </div>

                    <!-- Quick Actions -->
                    <div class="mb-4">
                        <p class="text-xs text-gray-500 font-medium mb-2 ml-1">Quick actions:</p>
                        <div class="grid grid-cols-2 gap-2" id="quick-actions">
                            <button class="quick-action-btn bg-white border border-gray-200 rounded-xl px-3 py-2 text-xs font-medium text-gray-700 hover:border-orange-primary hover:bg-orange-50 hover:text-orange-primary transition-all duration-200 text-left">
                                📅 Upcoming Events
                            </button>
                            <button class="quick-action-btn bg-white border border-gray-200 rounded-xl px-3 py-2 text-xs font-medium text-gray-700 hover:border-orange-primary hover:bg-orange-50 hover:text-orange-primary transition-all duration-200 text-left">
                                📚 Browse Resources
                            </button>
                            <button class="quick-action-btn bg-white border border-gray-200 rounded-xl px-3 py-2 text-xs font-medium text-gray-700 hover:border-orange-primary hover:bg-orange-50 hover:text-orange-primary transition-all duration-200 text-left">
                                💡 Innovation Programs
                            </button>
                            <button class="quick-action-btn bg-white border border-gray-200 rounded-xl px-3 py-2 text-xs font-medium text-gray-700 hover:border-orange-primary hover:bg-orange-50 hover:text-orange-primary transition-all duration-200 text-left">
                                📞 Contact Us
                            </button>
                        </div>
                    </div>

                    <!-- Messages will be appended here -->
                    <div id="chatbot-messages"></div>
                </div>

                <!-- Typing Indicator (hidden by default) -->
                <div id="typing-indicator" class="hidden px-4 py-2 bg-gradient-to-br from-gray-50 to-gray-100">
                    <div class="flex gap-3">
                        <div class="w-8 h-8 rounded-full bg-gradient-to-br from-orange-primary to-orange-secondary flex items-center justify-center flex-shrink-0">
                            <i class="fa-solid fa-robot text-white text-sm"></i>
                        </div>
                        <div class="bg-white rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm border border-gray-200 flex gap-1">
                            <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
                            <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
                            <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
                        </div>
                    </div>
                </div>

                <!-- Input Area -->
                <div class="bg-white border-t border-gray-200 p-4">
                    <form id="chatbot-form" class="flex gap-2">
                        <div class="flex-1 relative">
                            <input 
                                id="chatbot-input" 
                                type="text" 
                                placeholder="Type your message..." 
                                class="w-full px-4 py-3 pr-10 bg-gray-100 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-primary focus:border-transparent text-sm placeholder-gray-400 transition-all"
                                autocomplete="off"
                            />
                            <button type="button" id="emoji-btn" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors">
                                <i class="fa-regular fa-face-smile text-lg"></i>
                            </button>
                        </div>
                        <button 
                            type="submit" 
                            id="send-btn"
                            class="w-12 h-12 bg-gradient-to-br from-orange-primary to-orange-secondary text-white rounded-xl flex items-center justify-center hover:shadow-lg hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                            aria-label="Send message"
                        >
                            <i class="fa-solid fa-paper-plane text-lg"></i>
                        </button>
                    </form>
                    <p class="text-xs text-gray-400 text-center mt-2">Powered by MAHE Innovation Centre</p>
                </div>
            </div>
        `;
        
        document.body.appendChild(chatWindow);

        // Get elements
        const messagesContainer = chatWindow.querySelector('#chatbot-messages-container');
        const messagesDiv = chatWindow.querySelector('#chatbot-messages');
        const form = chatWindow.querySelector('#chatbot-form');
        const input = chatWindow.querySelector('#chatbot-input');
        const typingIndicator = chatWindow.querySelector('#typing-indicator');
        const closeBtn = chatWindow.querySelector('#chatbot-close');
        const quickActionBtns = chatWindow.querySelectorAll('.quick-action-btn');

        let isOpen = false;
        let sessionId = null;

        // Initialize session ID
        function initializeSession() {
            sessionId = localStorage.getItem('chatbot_session_id');
            if (!sessionId) {
                sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
                localStorage.setItem('chatbot_session_id', sessionId);
            }
        }

        // Initialize session when chatbot loads
        initializeSession();

        // Open/Close functions
        function openChat() {
            chatWindow.classList.remove('pointer-events-none', 'opacity-0', 'scale-95', 'translate-y-8');
            chatWindow.classList.add('opacity-100', 'scale-100', 'translate-y-0');
            isOpen = true;
            input.focus();
            // Hide notification badge
            document.getElementById('chat-notification')?.classList.add('hidden');
        }

        function closeChat() {
            chatWindow.classList.add('pointer-events-none', 'opacity-0', 'scale-95', 'translate-y-8');
            chatWindow.classList.remove('opacity-100', 'scale-100', 'translate-y-0');
            isOpen = false;
        }

        // Toggle chat
        chatBtn.addEventListener('click', () => {
            isOpen ? closeChat() : openChat();
        });

        closeBtn.addEventListener('click', closeChat);

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && isOpen) {
                closeChat();
            }
        });

        // Add user message
        function addUserMessage(text) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'flex justify-end gap-3 mb-4 animate-slide-in-right';
            messageDiv.innerHTML = `
                <div class="flex-1 flex justify-end">
                    <div class="bg-gradient-to-br from-orange-primary to-orange-secondary text-white rounded-2xl rounded-tr-sm px-4 py-3 shadow-md max-w-[85%]">
                        <p class="text-sm leading-relaxed">${escapeHtml(text)}</p>
                    </div>
                </div>
            `;
            messagesDiv.appendChild(messageDiv);
            scrollToBottom();
        }

        // Add bot message
        function addBotMessage(text, delay = 800) {
            showTypingIndicator();
            
            setTimeout(() => {
                hideTypingIndicator();
                
                const messageDiv = document.createElement('div');
                messageDiv.className = 'flex gap-3 mb-4 animate-fade-in';
                
                // Process text for buttons
                const processedContent = processMessageForButtons(text);
                
                messageDiv.innerHTML = `
                    <div class="w-8 h-8 rounded-full bg-gradient-to-br from-orange-primary to-orange-secondary flex items-center justify-center flex-shrink-0">
                        <i class="fa-solid fa-robot text-white text-sm"></i>
                    </div>
                    <div class="flex-1">
                        <div class="bg-white rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm border border-gray-200 max-w-[85%]">
                            ${processedContent}
                        </div>
                        <p class="text-xs text-gray-400 mt-1 ml-1">Just now</p>
                    </div>
                `;
                messagesDiv.appendChild(messageDiv);
                scrollToBottom();
            }, delay);
        }

        // Process message text to convert button markers to actual buttons
        function processMessageForButtons(text) {
            // Check if text contains button markers
            const buttonRegex = /\[BUTTON:([^|]+)\|([^\]]+)\]/g;
            const hasButtons = buttonRegex.test(text);
            
            let processedText;
            if (hasButtons) {
                // Don't escape HTML if we have buttons - we want to render them
                processedText = text;
            } else {
                // Escape HTML for regular text
                processedText = escapeHtml(text);
            }
            
            // Convert button markers to actual buttons
            processedText = processedText.replace(buttonRegex, (match, buttonText, url) => {
                return `<button style="display: inline-block; margin-top: 8px; padding: 8px 12px; background: linear-gradient(135deg, #ff6b35, #ff8c42); color: white; font-size: 12px; font-weight: 500; border-radius: 8px; border: none; cursor: pointer; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)'" onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)'" onclick="navigateToPage('${url}')">${buttonText}</button>`;
            });
            
            return processedText;
        }

        // Navigate to page function (make it globally accessible)
        window.navigateToPage = function(url) {
            // Close chat window
            closeChat();
            
            // Navigate to the page
            window.location.href = url;
        };

        // Show/Hide typing indicator
        function showTypingIndicator() {
            typingIndicator.classList.remove('hidden');
            scrollToBottom();
        }

        function hideTypingIndicator() {
            typingIndicator.classList.add('hidden');
        }

        // Scroll to bottom
        function scrollToBottom() {
            setTimeout(() => {
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }, 100);
        }

        // Escape HTML to prevent XSS
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Handle form submission
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const message = input.value.trim();
            
            if (!message) return;

            addUserMessage(message);
            input.value = '';

            // Generate bot response
            generateBotResponse(message);
        });

        // Quick action buttons
        quickActionBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const action = btn.textContent.trim();
                addUserMessage(action);
                
                // Generate appropriate response with button links
                if (action.includes('Events')) {
                    addBotMessage("Great! We have several exciting events coming up. Check our Events page at /events for upcoming events. Would you like me to show you specific event categories?", 600);
                } else if (action.includes('Resources')) {
                    addBotMessage("We offer a wide range of resources including innovation tools, incubation programs, and mentorship opportunities. Visit our Resources page at /resources for detailed information!", 600);
                } else if (action.includes('Innovation')) {
                    addBotMessage("Our Innovation Programs include MAHE SID, incubation support, and the SCHAP e-Cell mentorship program. We provide financial aid and guidance to aspiring entrepreneurs. Visit our Resources page at /resources for details. What would you like to know more about?", 700);
                } else if (action.includes('Contact')) {
                    addBotMessage("You can reach us through our Contact page where you can fill out a form, or email us directly. Get in touch via our Contact page at /contact. We typically respond within 1-2 business days. How can we help you today?", 600);
                }
            });
        });

        // Enhanced bot response logic with API integration
        async function generateBotResponse(userMessage) {
            try {
                const response = await fetch('/api/chatbot', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: userMessage,
                        session_id: sessionId
                    })
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                
                if (data.error) {
                    addBotMessage(data.error, 800);
                } else {
                    addBotMessage(data.response, 800);
                    // Store session ID for future requests
                    if (data.session_id) {
                        sessionId = data.session_id;
                        localStorage.setItem('chatbot_session_id', sessionId);
                    }
                }
            } catch (error) {
                console.error('Chatbot API error:', error);
                // Fallback response
                addBotMessage("I'm having trouble connecting right now. Please try again in a moment or visit our Contact page for immediate assistance.", 800);
            }
        }

        // Add custom styles for animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fade-in {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            @keyframes slide-in-right {
                from { opacity: 0; transform: translateX(20px); }
                to { opacity: 1; transform: translateX(0); }
            }
            .animate-fade-in {
                animation: fade-in 0.3s ease-out;
            }
            .animate-slide-in-right {
                animation: slide-in-right 0.3s ease-out;
            }
            #chatbot-messages-container {
                scrollbar-width: thin;
                scrollbar-color: #ff6b35 #f3f4f6;
            }
            #chatbot-messages-container::-webkit-scrollbar {
                width: 6px;
            }
            #chatbot-messages-container::-webkit-scrollbar-track {
                background: #f3f4f6;
            }
            #chatbot-messages-container::-webkit-scrollbar-thumb {
                background: #ff6b35;
                border-radius: 3px;
            }
            #chatbot-messages-container::-webkit-scrollbar-thumb:hover {
                background: #ff8c42;
            }
        `;
        document.head.appendChild(style);

        // Show notification after 5 seconds if chat is closed
        setTimeout(() => {
            if (!isOpen) {
                document.getElementById('chat-notification')?.classList.remove('hidden');
            }
        }, 5000);
    }
})();
