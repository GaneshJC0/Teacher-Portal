import bcrypt
from database.db_connection import db
from helpers.utils import validate_email, validate_password

class AuthController:
    @staticmethod
    def authenticate_teacher(username, password):
        """Authenticate teacher login credentials"""
        try:
            # Query to find teacher by username or email
            query = """
            SELECT id, username, email, password_hash, full_name 
            FROM teachers 
            WHERE username = ? OR email = ?
            """
            
            results = db.execute_query(query, (username, username))
            
            if not results:
                return {
                    'success': False,
                    'message': 'Invalid username or email'
                }
            
            teacher = dict(results[0])
            
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), teacher['password_hash'].encode('utf-8')):
                # Remove password hash from returned data
                del teacher['password_hash']
                return {
                    'success': True,
                    'message': 'Login successful',
                    'teacher': teacher
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid password'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Authentication error: {str(e)}'
            }
    
    @staticmethod
    def register_teacher(username, email, password, full_name):
        """Register a new teacher (for future use)"""
        try:
            # Validate input
            if not validate_email(email):
                return {
                    'success': False,
                    'message': 'Invalid email format'
                }
            
            if not validate_password(password):
                return {
                    'success': False,
                    'message': 'Password must be at least 6 characters long'
                }
            
            # Check if username or email already exists
            check_query = """
            SELECT id FROM teachers 
            WHERE username = ? OR email = ?
            """
            
            existing = db.execute_query(check_query, (username, email))
            
            if existing:
                return {
                    'success': False,
                    'message': 'Username or email already exists'
                }
            
            # Hash password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Insert new teacher
            insert_query = """
            INSERT INTO teachers (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
            """
            
            teacher_id = db.execute_insert(insert_query, (
                username, email, hashed_password.decode('utf-8'), full_name
            ))
            
            if teacher_id:
                return {
                    'success': True,
                    'message': 'Teacher registered successfully',
                    'teacher_id': teacher_id
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to register teacher'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Registration error: {str(e)}'
            }
    
    @staticmethod
    def get_teacher_by_id(teacher_id):
        """Get teacher information by ID"""
        try:
            query = """
            SELECT id, username, email, full_name, created_at
            FROM teachers 
            WHERE id = ?
            """
            
            results = db.execute_query(query, (teacher_id,))
            
            if results:
                return {
                    'success': True,
                    'teacher': dict(results[0])
                }
            else:
                return {
                    'success': False,
                    'message': 'Teacher not found'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error fetching teacher: {str(e)}'
            }