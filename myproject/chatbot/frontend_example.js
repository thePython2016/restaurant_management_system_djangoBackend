// Frontend Example: How to implement blinking chatbot notification
// This shows how your React/frontend app can use the new API endpoints

// 1. Fetch notification data for the user tab
async function getChatbotNotification() {
    try {
        const response = await fetch('/api/chatbot/notification/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`, // JWT token
                'Content-Type': 'application/json',
            },
        });
        
        if (response.ok) {
            const data = await response.json();
            return data;
        }
    } catch (error) {
        console.error('Error fetching notification:', error);
    }
    return null;
}

// 2. Fetch chatbot page data when user clicks notification
async function getChatbotPageData() {
    try {
        const response = await fetch('/api/chatbot/page/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                'Content-Type': 'application/json',
            },
        });
        
        if (response.ok) {
            const data = await response.json();
            return data;
        }
    } catch (error) {
        console.error('Error fetching chatbot page:', error);
    }
    return null;
}

// 3. React Component Example
/*
import React, { useState, useEffect } from 'react';

function UserTab() {
    const [notification, setNotification] = useState(null);
    const [showChatbot, setShowChatbot] = useState(false);
    const [chatbotData, setChatbotData] = useState(null);

    useEffect(() => {
        // Load notification when component mounts
        loadNotification();
    }, []);

    const loadNotification = async () => {
        const notificationData = await getChatbotNotification();
        if (notificationData && notificationData.show_notification) {
            setNotification(notificationData);
        }
    };

    const handleNotificationClick = async () => {
        const pageData = await getChatbotPageData();
        setChatbotData(pageData);
        setShowChatbot(true);
    };

    return (
        <div className="user-tab">
            {/* User tab content */}
            
            {/* Blinking Notification */}
            {notification && (
                <div 
                    className={`notification ${notification.blink ? 'blink' : ''}`}
                    onClick={handleNotificationClick}
                    style={{ 
                        backgroundColor: notification.color,
                        cursor: 'pointer',
                        padding: '10px',
                        borderRadius: '5px',
                        margin: '10px 0'
                    }}
                >
                    <span style={{ marginRight: '8px' }}>{notification.icon}</span>
                    {notification.message}
                </div>
            )}

            {/* Chatbot Modal/Page */}
            {showChatbot && chatbotData && (
                <div className="chatbot-modal">
                    <h2>{chatbotData.welcome_message}</h2>
                    <p>{chatbotData.subtitle}</p>
                    
                    <div className="features">
                        {chatbotData.features.map((feature, index) => (
                            <div key={index} className="feature-item">
                                • {feature}
                            </div>
                        ))}
                    </div>
                    
                    <div className="chat-input">
                        <input 
                            type="text" 
                            placeholder={chatbotData.placeholder}
                            // Add your chat functionality here
                        />
                    </div>
                </div>
            )}
        </div>
    );
}

// CSS for blinking animation
const styles = `
.notification.blink {
    animation: blink 1.5s infinite;
}

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0.3; }
}

.notification:hover {
    transform: scale(1.05);
    transition: transform 0.2s;
}
`;
*/

// 4. Usage in your existing frontend:
/*
// In your user dashboard/tab component:
// 1. Call getChatbotNotification() when the user tab loads
// 2. Show a blinking notification if show_notification is true
// 3. When user clicks notification, call getChatbotPageData()
// 4. Redirect to chatbot page or show chatbot modal
// 5. Use the existing /api/chatbot/chat/ endpoint for actual chat functionality
*/












