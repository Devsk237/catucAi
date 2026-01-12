// Global variables
let chatHistory = [];

// DOM elements
let questionInput, sendButton, chatMessages, newChatBtn, mobileMenuToggle, sidebar;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded');
    
    // Get DOM elements
    questionInput = document.getElementById('questionInput');
    sendButton = document.getElementById('sendButton');
    chatMessages = document.getElementById('chatMessages');
    newChatBtn = document.getElementById('newChatBtn');
    mobileMenuToggle = document.getElementById('mobileMenuToggle');
    sidebar = document.querySelector('.sidebar');
    
    console.log('Elements found:', {
        questionInput: !!questionInput,
        sendButton: !!sendButton,
        chatMessages: !!chatMessages
    });
    
    if (questionInput && sendButton) {
        setupEventListeners();
        focusInput();
        loadChatHistory();
    } else {
        console.error('Required elements not found');
    }
});

function setupEventListeners() {
    console.log('Setting up event listeners');
    
    // Send button click - use multiple methods for reliability
    sendButton.onclick = function(e) {
        console.log('Send button clicked via onclick');
        e.preventDefault();
        sendMessage();
    };
    
    sendButton.addEventListener('click', function(e) {
        console.log('Send button clicked via addEventListener');
        e.preventDefault();
        sendMessage();
    });
    
    // Enter key to send
    questionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            console.log('Enter key pressed');
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize and update send button state
    questionInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 200) + 'px';
        
        const hasText = this.value.trim().length > 0;
        sendButton.classList.toggle('active', hasText);
        console.log('Input changed, hasText:', hasText);
    });
    
    // Other event listeners
    if (newChatBtn) {
        newChatBtn.addEventListener('click', startNewChat);
    }
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', toggleMobileMenu);
    }
}

function focusInput() {
    questionInput.focus();
    // Start with send button enabled
    sendButton.disabled = false;
    sendButton.classList.remove('active');
    console.log('Send button initialized');
}

function setLoading(isLoading) {
    sendButton.disabled = isLoading;
    questionInput.disabled = isLoading;
    
    const svgIcon = sendButton.querySelector('svg');
    const spinner = sendButton.querySelector('.loading-spinner');
    
    if (isLoading) {
        svgIcon.style.display = 'none';
        spinner.style.display = 'flex';
    } else {
        svgIcon.style.display = 'block';
        spinner.style.display = 'none';
    }
}

function sendMessage() {
    console.log('sendMessage function called');
    
    if (!questionInput || !sendButton) {
        console.error('Elements not available');
        return;
    }
    
    const question = questionInput.value.trim();
    console.log('Question:', question);
    
    if (!question) {
        console.log('No question text');
        return;
    }
    
    // Add user message to chat
    addMessage(question, 'user');
    
    // Clear input and reset
    questionInput.value = '';
    questionInput.style.height = 'auto';
    sendButton.classList.remove('active');
    
    // Set loading state
    setLoading(true);
    
    // Send to backend
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question: question
        })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        console.log('Response received:', data);
        if (data.error) {
            addMessage('Error: ' + data.error, 'bot', true);
        } else {
            addMessage(data.response, 'bot');
            updateChatHistory(question, data.response);
        }
    })
    .catch(function(error) {
        console.error('Error:', error);
        addMessage('Sorry, I encountered an error while processing your request. Please try again.', 'bot', true);
    })
    .finally(function() {
        setLoading(false);
        focusInput();
    });
}

function addMessage(content, sender, isError) {
    var messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + sender + '-message';
    
    // Create avatar
    var avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    
    if (sender === 'bot') {
        avatarDiv.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"></path><path d="M2 17l10 5 10-5"></path><path d="M2 12l10 5 10-5"></path></svg>';
    } else {
        avatarDiv.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>';
    }
    
    // Create message content
    var messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    var processedContent = processMessageContent(content, sender, isError);
    messageContent.innerHTML = processedContent;
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function processMessageContent(content, sender, isError) {
    if (isError) {
        return '<p style="color: #ef4444;">' + content + '</p>';
    }
    
    // Clean up content - remove markdown formatting
    var processedContent = content
        .replace(/\*\*(.*?)\*\*/g, '$1')
        .replace(/\*(.*?)\*/g, '$1')
        .replace(/\[(.*?)\]\(.*?\)/g, '$1')
        .replace(/`([^`]+)`/g, '$1')
        .replace(/```[\s\S]*?```/g, '')
        .replace(/#{1,6}\s/g, '')
        .replace(/\n{3,}/g, '\n\n')
        .trim();
    
    // Convert to paragraphs
    var paragraphs = processedContent.split('\n\n').map(function(p) {
        if (p.trim()) {
            return '<p>' + p.trim().replace(/\n/g, '<br>') + '</p>';
        }
        return '';
    }).filter(function(p) {
        return p !== '';
    });
    
    // Add source indicator
    if (processedContent.includes('(source:')) {
        paragraphs.push('<span class="source-indicator">Information from school database</span>');
    }
    
    return paragraphs.join('');
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function startNewChat() {
    while (chatMessages.children.length > 1) {
        chatMessages.removeChild(chatMessages.lastChild);
    }
    
    updateChatHistoryDisplay([]);
    focusInput();
    
    if (window.innerWidth <= 768) {
        sidebar.classList.remove('open');
    }
}

function updateChatHistory(question, response) {
    chatHistory.unshift({
        question: question.substring(0, 50) + (question.length > 50 ? '...' : ''),
        timestamp: new Date().toISOString()
    });
    
    chatHistory = chatHistory.slice(0, 10);
    
    localStorage.setItem('legendbot-history', JSON.stringify(chatHistory));
    updateChatHistoryDisplay(chatHistory);
}

function loadChatHistory() {
    var saved = localStorage.getItem('legendbot-history');
    if (saved) {
        try {
            chatHistory = JSON.parse(saved);
            updateChatHistoryDisplay(chatHistory);
        } catch (e) {
            console.error('Error loading chat history:', e);
        }
    }
}

function updateChatHistoryDisplay(history) {
    var historyContainer = document.querySelector('.chat-history');
    
    if (history.length === 0) {
        historyContainer.innerHTML = '<h3>Recent chats</h3><div class="history-placeholder">No recent conversations</div>';
    } else {
        historyContainer.innerHTML = '<h3>Recent chats</h3><div class="history-list"></div>';
        
        var historyList = historyContainer.querySelector('.history-list');
        historyList.innerHTML = history.map(function(chat, index) {
            return '<div class="history-item" data-index="' + index + '">' +
                   '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>' +
                   '<span>' + chat.question + '</span>' +
                   '</div>';
        }).join('');
        
        var historyItems = historyList.querySelectorAll('.history-item');
        historyItems.forEach(function(item) {
            item.addEventListener('click', function() {
                var question = this.querySelector('span').textContent;
                questionInput.value = question;
                questionInput.style.height = 'auto';
                questionInput.style.height = questionInput.scrollHeight + 'px';
                sendButton.classList.add('active');
                focusInput();
                
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove('open');
                }
            });
        });
    }
}

function toggleMobileMenu() {
    sidebar.classList.toggle('open');
}

// Check server health
fetch('/health')
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        console.log('Server health:', data);
    })
    .catch(function(error) {
        console.error('Health check failed:', error);
    });
