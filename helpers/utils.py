import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if not password:
        return False
    
    # Minimum 6 characters
    return len(password) >= 6

def validate_student_data(name, subject_name, marks):
    """Validate student data"""
    errors = []
    
    # Validate name
    if not name or not name.strip():
        errors.append("Student name is required")
    elif len(name.strip()) < 2:
        errors.append("Student name must be at least 2 characters long")
    elif len(name.strip()) > 100:
        errors.append("Student name must be less than 100 characters")
    
    # Validate subject name
    if not subject_name or not subject_name.strip():
        errors.append("Subject name is required")
    elif len(subject_name.strip()) < 2:
        errors.append("Subject name must be at least 2 characters long")
    elif len(subject_name.strip()) > 100:
        errors.append("Subject name must be less than 100 characters")
    
    # Validate marks
    try:
        marks_int = int(marks)
        if marks_int < 0:
            errors.append("Marks cannot be negative")
        elif marks_int > 1000:
            errors.append("Marks cannot exceed 1000")
    except (ValueError, TypeError):
        errors.append("Marks must be a valid number")
    
    if errors:
        return {
            'valid': False,
            'message': '; '.join(errors)
        }
    
    return {
        'valid': True,
        'message': 'Valid data'
    }

def sanitize_string(text):
    """Sanitize string input"""
    if not text:
        return ""
    
    # Remove extra whitespace and strip
    return ' '.join(text.strip().split())

def format_datetime(dt_string):
    """Format datetime string for display"""
    try:
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return dt_string

def generate_success_response(message, data=None):
    """Generate standardized success response"""
    response = {
        'success': True,
        'message': message
    }
    
    if data:
        response.update(data)
    
    return response

def generate_error_response(message, error_code=None):
    """Generate standardized error response"""
    response = {
        'success': False,
        'message': message
    }
    
    if error_code:
        response['error_code'] = error_code
    
    return response

def calculate_grade(marks):
    """Calculate letter grade based on marks"""
    if marks >= 90:
        return 'A+'
    elif marks >= 80:
        return 'A'
    elif marks >= 70:
        return 'B+'
    elif marks >= 60:
        return 'B'
    elif marks >= 50:
        return 'C'
    elif marks >= 40:
        return 'D'
    else:
        return 'F'

def get_grade_color(marks):
    """Get color code for grade display"""
    if marks >= 80:
        return '#28a745'  # Green
    elif marks >= 60:
        return '#ffc107'  # Yellow
    elif marks >= 40:
        return '#fd7e14'  # Orange
    else:
        return '#dc3545'  # Red