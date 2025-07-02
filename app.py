from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from config import Config, DevelopmentConfig, ProductionConfig
from controllers.auth_controller import AuthController
from controllers.student_controller import StudentController
from database.init_db import initialize_database

# Create Flask application
app = Flask(__name__)

# Load configuration
if os.environ.get('FLASK_ENV') == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Initialize database on first run
@app.before_request
def ensure_tables_exist():
    if not hasattr(app, 'db_initialized'):
        initialize_database()
        app.db_initialized = True

# Routes
@app.route('/')
def index():
    """Redirect to login if not authenticated, otherwise to dashboard"""
    if 'teacher_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    """Display login page"""
    if 'teacher_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Display teacher dashboard"""
    if 'teacher_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', teacher=session.get('teacher'))

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

# API Routes
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """Handle login authentication"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        # Authenticate user
        auth_result = AuthController.authenticate_teacher(username, password)
        
        if auth_result['success']:
            # Store user session
            teacher = auth_result['teacher']
            session['teacher_id'] = teacher['id']
            session['teacher'] = teacher
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'redirect_url': url_for('dashboard')
            })
        else:
            return jsonify(auth_result), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login error: {str(e)}'
        }), 500

@app.route('/api/students', methods=['GET'])
def api_get_students():
    """Get all students for logged-in teacher"""
    if 'teacher_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Not authenticated'
        }), 401
    
    try:
        teacher_id = session['teacher_id']
        result = StudentController.get_all_students(teacher_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching students: {str(e)}'
        }), 500

@app.route('/api/students', methods=['POST'])
def api_add_student():
    """Add new student or update existing student"""
    if 'teacher_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Not authenticated'
        }), 401
    
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        subject_name = data.get('subject_name', '').strip()
        marks = data.get('marks', '')
        
        if not name or not subject_name or not marks:
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400
        
        teacher_id = session['teacher_id']
        result = StudentController.add_or_update_student(name, subject_name, marks, teacher_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error adding student: {str(e)}'
        }), 500

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def api_update_student(student_id):
    """Update existing student"""
    if 'teacher_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Not authenticated'
        }), 401
    
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        subject_name = data.get('subject_name', '').strip()
        marks = data.get('marks', '')
        
        if not name or not subject_name or not marks:
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400
        
        teacher_id = session['teacher_id']
        result = StudentController.update_student(student_id, name, subject_name, marks, teacher_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating student: {str(e)}'
        }), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    """Delete student"""
    if 'teacher_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Not authenticated'
        }), 401
    
    try:
        teacher_id = session['teacher_id']
        result = StudentController.delete_student(student_id, teacher_id)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error deleting student: {str(e)}'
        }), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    """Get specific student by ID"""
    if 'teacher_id' not in session:
        return jsonify({
            'success': False,
            'message': 'Not authenticated'
        }), 401
    
    try:
        teacher_id = session['teacher_id']
        result = StudentController.get_student_by_id(student_id, teacher_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching student: {str(e)}'
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)