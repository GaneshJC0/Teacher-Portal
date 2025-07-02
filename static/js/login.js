// Login page functionality
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const loginBtn = document.getElementById('loginBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const usernameField = document.getElementById('username');
    const passwordField = document.getElementById('password');

    // Clear any existing errors when user starts typing
    usernameField.addEventListener('input', () => {
        Utils.clearError('usernameError');
        Utils.clearError('loginError');
    });

    passwordField.addEventListener('input', () => {
        Utils.clearError('passwordError');
        Utils.clearError('loginError');
    });

    // Handle form submission
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Clear previous errors
        Utils.clearFormErrors('loginForm');
        
        // Get form data
        const username = usernameField.value.trim();
        const password = passwordField.value;
        
        // Validate fields
        let isValid = true;
        
        if (!Utils.validateField('username', 'usernameError', 'required')) {
            isValid = false;
        }
        
        if (!Utils.validateField('password', 'passwordError', 'required')) {
            isValid = false;
        }
        
        if (!isValid) {
            return;
        }
        
        // Show loading state
        Utils.showButtonLoading(loginBtn, loadingSpinner);
        
        try {
            // Make login request
            const response = await API.post('/api/auth/login', {
                username: username,
                password: password
            });
            
            if (response.success) {
                // Show success message
                Toast.success('Login successful! Redirecting...');
                
                // Redirect to dashboard
                setTimeout(() => {
                    window.location.href = response.redirect_url || '/dashboard';
                }, 1000);
            } else {
                // Show error message
                Utils.showError('loginError', response.message || 'Login failed');
            }
        } catch (error) {
            console.error('Login error:', error);
            Utils.showError('loginError', error.message || 'An error occurred during login');
        } finally {
            // Hide loading state
            Utils.hideButtonLoading(loginBtn, loadingSpinner);
        }
    });

    // Handle Enter key press
    document.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && (e.target === usernameField || e.target === passwordField)) {
            loginForm.dispatchEvent(new Event('submit'));
        }
    });

    // Focus on username field when page loads
    usernameField.focus();
    
    // Demo credentials helper (for development)
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        // Add demo credentials info
        const demoInfo = document.createElement('div');
        demoInfo.className = 'demo-info';
        demoInfo.innerHTML = `
            <p><small><strong>Demo Credentials:</strong></small></p>
            <p><small>Username: teacher1 | Password: password123</small></p>
        `;
        demoInfo.style.cssText = `
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.1);
            padding: 10px;
            border-radius: 4px;
            text-align: center;
            color: #666;
        `;
        document.body.appendChild(demoInfo);
    }
});