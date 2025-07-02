// Common utility functions and configurations
const API_BASE_URL = '';

// Utility Functions
const Utils = {
    // Show loading state on button
    showButtonLoading: (button, spinner) => {
        const btnText = button.querySelector('.btn-text');
        const loadingSpinner = button.querySelector('.loading-spinner') || spinner;
        
        if (btnText) btnText.style.display = 'none';
        if (loadingSpinner) {
            loadingSpinner.style.display = 'inline-block';
        }
        button.disabled = true;
    },

    // Hide loading state on button
    hideButtonLoading: (button, spinner) => {
        const btnText = button.querySelector('.btn-text');
        const loadingSpinner = button.querySelector('.loading-spinner') || spinner;
        
        if (btnText) btnText.style.display = 'inline';
        if (loadingSpinner) {
            loadingSpinner.style.display = 'none';
        }
        button.disabled = false;
    },

    // Show error message
    showError: (elementId, message) => {
        const errorElement = document.getElementById(elementId);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
    },

    // Clear error message
    clearError: (elementId) => {
        const errorElement = document.getElementById(elementId);
        if (errorElement) {
            errorElement.textContent = '';
            errorElement.style.display = 'none';
        }
    },

    // Clear all form errors
    clearFormErrors: (formId) => {
        const form = document.getElementById(formId);
        if (form) {
            const errorElements = form.querySelectorAll('.error-message');
            errorElements.forEach(element => {
                element.textContent = '';
                element.style.display = 'none';
            });
        }
    },

    // Validate form fields
    validateField: (fieldId, errorId, validationType = 'required') => {
        const field = document.getElementById(fieldId);
        const value = field.value.trim();
        
        if (validationType === 'required' && !value) {
            Utils.showError(errorId, 'This field is required');
            return false;
        }
        
        if (validationType === 'number' && (isNaN(value) || value < 0)) {
            Utils.showError(errorId, 'Please enter a valid number');
            return false;
        }
        
        if (validationType === 'marks' && (isNaN(value) || value < 0 || value > 100)) {
            Utils.showError(errorId, 'Marks must be between 0 and 100');
            return false;
        }
        
        Utils.clearError(errorId);
        return true;
    },

    // Format date
    formatDate: (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    // Debounce function
    debounce: (func, wait) => {
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
};

// API Helper Functions
const API = {
    // Generic API request function
    request: async (url, options = {}) => {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const config = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(API_BASE_URL + url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    },

    // GET request
    get: (url) => API.request(url),

    // POST request
    post: (url, data) => API.request(url, {
        method: 'POST',
        body: JSON.stringify(data)
    }),

    // PUT request
    put: (url, data) => API.request(url, {
        method: 'PUT',
        body: JSON.stringify(data)
    }),

    // DELETE request
    delete: (url) => API.request(url, {
        method: 'DELETE'
    })
};

// Toast notification system
const Toast = {
    show: (message, type = 'info', duration = 3000) => {
        // Remove existing toast
        const existingToast = document.querySelector('.toast');
        if (existingToast) {
            existingToast.remove();
        }

        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span class="toast-message">${message}</span>
            <button class="toast-close" onclick="this.parentElement.remove()">&times;</button>
        `;

        // Add to body
        document.body.appendChild(toast);

        // Auto remove after duration
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, duration);
    },

    success: (message) => Toast.show(message, 'success'),
    error: (message) => Toast.show(message, 'error'),
    warning: (message) => Toast.show(message, 'warning'),
    info: (message) => Toast.show(message, 'info')
};

// Global error handler
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

// Global unhandled promise rejection handler
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});

// Initialize common functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Add CSS for toast notifications if not already present
    if (!document.querySelector('#toast-styles')) {
        const style = document.createElement('style');
        style.id = 'toast-styles';
        style.textContent = `
            .toast {
                position: fixed;
                top: 20px;
                right: 20px;
                min-width: 300px;
                padding: 12px 16px;
                border-radius: 6px;
                color: white;
                font-weight: 500;
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: space-between;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                animation: slideIn 0.3s ease-out;
            }
            
            .toast-success { background-color: #10b981; }
            .toast-error { background-color: #ef4444; }
            .toast-warning { background-color: #f59e0b; }
            .toast-info { background-color: #3b82f6; }
            
            .toast-close {
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                margin-left: 12px;
                padding: 0;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
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
        `;
        document.head.appendChild(style);
    }
});