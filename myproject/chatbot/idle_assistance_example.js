// Frontend Example: Idle Timeout Assistance Notification System
// This shows how to implement idle detection and assistance notifications

class IdleAssistanceManager {
    constructor() {
        this.idleThreshold = 1 * 60 * 1000; // 1 minute in milliseconds
        this.checkInterval = 30 * 1000; // Check every 30 seconds
        this.activityTimeout = null;
        this.checkIntervalId = null;
        this.isIdle = false;
        this.lastActivity = Date.now();
        
        this.init();
    }

    init() {
        // Track user activity on various events
        this.trackActivityEvents();
        
        // Start checking for idle time
        this.startIdleCheck();
        
        // Initial activity tracking
        this.trackActivity();
    }

    trackActivityEvents() {
        const events = [
            'mousedown', 'mousemove', 'keypress', 'scroll', 
            'touchstart', 'click', 'keydown'
        ];

        events.forEach(event => {
            document.addEventListener(event, () => {
                this.trackActivity();
            }, true);
        });
    }

    async trackActivity() {
        try {
            const response = await fetch('/api/chatbot/track-activity/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                this.lastActivity = Date.now();
                this.isIdle = false;
                console.log('Activity tracked successfully');
            }
        } catch (error) {
            console.error('Error tracking activity:', error);
        }
    }

    startIdleCheck() {
        this.checkIntervalId = setInterval(async () => {
            await this.checkIdleStatus();
        }, this.checkInterval);
    }

    async checkIdleStatus() {
        try {
            const response = await fetch('/api/chatbot/idle-assistance/', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                
                if (data.show_assistance && !this.isIdle) {
                    this.isIdle = true;
                    this.showAssistanceNotification(data);
                } else if (!data.show_assistance && this.isIdle) {
                    this.isIdle = false;
                    this.hideAssistanceNotification();
                }
            }
        } catch (error) {
            console.error('Error checking idle status:', error);
        }
    }

    showAssistanceNotification(data) {
        // Remove existing notification if any
        this.hideAssistanceNotification();

        // Create notification element
        const notification = document.createElement('div');
        notification.id = 'idle-assistance-notification';
        notification.className = 'idle-assistance-notification';
        
        notification.innerHTML = `
            <div class="notification-content">
                <div class="notification-header">
                    <span class="notification-icon">${data.icon}</span>
                    <span class="notification-title">Need Help?</span>
                    <button class="dismiss-btn" onclick="idleManager.dismissNotification()">×</button>
                </div>
                <div class="notification-body">
                    <p class="notification-message">${data.message}</p>
                    <p class="notification-subtitle">${data.subtitle}</p>
                    <div class="assistance-options">
                        ${data.assistance_options.map(option => 
                            `<div class="option-item">• ${option}</div>`
                        ).join('')}
                    </div>
                    <button class="get-help-btn" onclick="idleManager.openChatbot()">
                        Get Help Now
                    </button>
                </div>
            </div>
        `;

        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${data.color};
            color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            z-index: 10000;
            max-width: 350px;
            animation: slideIn 0.3s ease-out;
            ${data.blink ? 'animation: blink 2s infinite;' : ''}
        `;

        // Add to page
        document.body.appendChild(notification);

        // Auto-hide after 30 seconds if not interacted with
        setTimeout(() => {
            if (document.getElementById('idle-assistance-notification')) {
                this.hideAssistanceNotification();
            }
        }, 30000);
    }

    hideAssistanceNotification() {
        const notification = document.getElementById('idle-assistance-notification');
        if (notification) {
            notification.remove();
        }
    }

    async dismissNotification() {
        try {
            const response = await fetch('/api/chatbot/dismiss-assistance/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                this.hideAssistanceNotification();
                this.isIdle = false;
                console.log('Assistance notification dismissed');
            }
        } catch (error) {
            console.error('Error dismissing notification:', error);
        }
    }

    openChatbot() {
        // Hide notification
        this.hideAssistanceNotification();
        
        // Open chatbot (implement based on your app structure)
        // This could be a modal, new page, or sidebar
        window.location.href = '/chatbot'; // or trigger chatbot modal
    }

    destroy() {
        if (this.checkIntervalId) {
            clearInterval(this.checkIntervalId);
        }
        this.hideAssistanceNotification();
    }
}

// CSS Styles (add to your main CSS file)
const idleAssistanceStyles = `
@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0.7; }
}

.idle-assistance-notification {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.notification-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.notification-icon {
    font-size: 20px;
    margin-right: 8px;
}

.notification-title {
    font-weight: bold;
    font-size: 16px;
    flex: 1;
}

.dismiss-btn {
    background: none;
    border: none;
    color: white;
    font-size: 20px;
    cursor: pointer;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.dismiss-btn:hover {
    background: rgba(255,255,255,0.2);
    border-radius: 50%;
}

.notification-message {
    margin: 0 0 8px 0;
    font-size: 14px;
    line-height: 1.4;
}

.notification-subtitle {
    margin: 0 0 12px 0;
    font-size: 12px;
    opacity: 0.9;
}

.assistance-options {
    margin: 12px 0;
}

.option-item {
    font-size: 12px;
    margin: 4px 0;
    opacity: 0.9;
}

.get-help-btn {
    background: rgba(255,255,255,0.2);
    border: 1px solid rgba(255,255,255,0.3);
    color: white;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    width: 100%;
    margin-top: 10px;
}

.get-help-btn:hover {
    background: rgba(255,255,255,0.3);
}
`;

// Initialize the idle assistance manager
let idleManager;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Add styles to head
    const styleSheet = document.createElement('style');
    styleSheet.textContent = idleAssistanceStyles;
    document.head.appendChild(styleSheet);
    
    // Initialize idle manager
    idleManager = new IdleAssistanceManager();
});

// React Component Example
/*
import React, { useEffect, useRef } from 'react';

function IdleAssistanceProvider({ children }) {
    const idleManagerRef = useRef(null);

    useEffect(() => {
        // Initialize idle manager
        idleManagerRef.current = new IdleAssistanceManager();
        
        return () => {
            // Cleanup
            if (idleManagerRef.current) {
                idleManagerRef.current.destroy();
            }
        };
    }, []);

    return <>{children}</>;
}

// Usage in your main App component:
function App() {
    return (
        <IdleAssistanceProvider>
            <YourAppContent />
        </IdleAssistanceProvider>
    );
}
*/

// Usage Instructions:
/*
1. Include this script in your main app
2. The manager will automatically:
   - Track user activity (mouse, keyboard, touch, scroll)
   - Check for idle time every 30 seconds
       - Show assistance notification after 1 minute of inactivity
   - Allow user to dismiss or get help

3. Customize the idle threshold by changing idleThreshold in the constructor
4. Customize the check interval by changing checkInterval
5. The notification will auto-hide after 30 seconds if not interacted with

API Endpoints Used:
- POST /api/chatbot/track-activity/ - Track user activity
- GET /api/chatbot/idle-assistance/ - Check if assistance needed
- POST /api/chatbot/dismiss-assistance/ - Dismiss notification
*/
