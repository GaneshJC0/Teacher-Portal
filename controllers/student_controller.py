from database.db_connection import db
from helpers.utils import validate_student_data

class StudentController:
    @staticmethod
    def get_all_students(teacher_id):
        """Get all students for a specific teacher"""
        try:
            query = """
            SELECT id, name, subject_name, marks, created_at, updated_at
            FROM students 
            WHERE teacher_id = ?
            ORDER BY name, subject_name
            """
            
            results = db.execute_query(query, (teacher_id,))
            
            students = [dict(row) for row in results]
            
            return {
                'success': True,
                'students': students
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error fetching students: {str(e)}'
            }
    
    @staticmethod
    def add_or_update_student(name, subject_name, marks, teacher_id):
        """Add new student or update existing student's marks"""
        try:
            # Validate input data
            validation_result = validate_student_data(name, subject_name, marks)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'message': validation_result['message']
                }
            
            # Check if student with same name and subject already exists
            check_query = """
            SELECT id, marks FROM students 
            WHERE name = ? AND subject_name = ? AND teacher_id = ?
            """
            
            existing = db.execute_query(check_query, (name, subject_name, teacher_id))
            
            if existing:
                # Update existing student - add new marks to existing marks
                existing_student = dict(existing[0])
                new_total_marks = existing_student['marks'] + int(marks)
                
                update_query = """
                UPDATE students 
                SET marks = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """
                
                rows_updated = db.execute_update(update_query, (new_total_marks, existing_student['id']))
                
                if rows_updated:
                    return {
                        'success': True,
                        'message': f'Updated {name}\'s marks in {subject_name}. New total: {new_total_marks}',
                        'action': 'updated',
                        'student_id': existing_student['id'],
                        'new_marks': new_total_marks
                    }
                else:
                    return {
                        'success': False,
                        'message': 'Failed to update student marks'
                    }
            else:
                # Create new student record
                insert_query = """
                INSERT INTO students (name, subject_name, marks, teacher_id)
                VALUES (?, ?, ?, ?)
                """
                
                student_id = db.execute_insert(insert_query, (name, subject_name, int(marks), teacher_id))
                
                if student_id:
                    return {
                        'success': True,
                        'message': f'Added new student: {name} in {subject_name}',
                        'action': 'created',
                        'student_id': student_id
                    }
                else:
                    return {
                        'success': False,
                        'message': 'Failed to create new student record'
                    }
                    
        except Exception as e:
            return {
                'success': False,
                'message': f'Error processing student: {str(e)}'
            }
    
    @staticmethod
    def update_student(student_id, name, subject_name, marks, teacher_id):
        """Update an existing student's information"""
        try:
            # Validate input data
            validation_result = validate_student_data(name, subject_name, marks)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'message': validation_result['message']
                }
            
            # Check if student exists and belongs to the teacher
            check_query = """
            SELECT id FROM students 
            WHERE id = ? AND teacher_id = ?
            """
            
            existing = db.execute_query(check_query, (student_id, teacher_id))
            
            if not existing:
                return {
                    'success': False,
                    'message': 'Student not found'
                }
            
            # Check for duplicate name-subject combination (excluding current student)
            duplicate_query = """
            SELECT id FROM students 
            WHERE name = ? AND subject_name = ? AND teacher_id = ? AND id != ?
            """
            
            duplicate = db.execute_query(duplicate_query, (name, subject_name, teacher_id, student_id))
            
            if duplicate:
                return {
                    'success': False,
                    'message': 'A student with this name and subject combination already exists'
                }
            
            # Update student
            update_query = """
            UPDATE students 
            SET name = ?, subject_name = ?, marks = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND teacher_id = ?
            """
            
            rows_updated = db.execute_update(update_query, (name, subject_name, int(marks), student_id, teacher_id))
            
            if rows_updated:
                return {
                    'success': True,
                    'message': 'Student updated successfully'
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to update student'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error updating student: {str(e)}'
            }
    
    @staticmethod
    def delete_student(student_id, teacher_id):
        """Delete a student record"""
        try:
            # Check if student exists and belongs to the teacher
            check_query = """
            SELECT id, name, subject_name FROM students 
            WHERE id = ? AND teacher_id = ?
            """
            
            existing = db.execute_query(check_query, (student_id, teacher_id))
            
            if not existing:
                return {
                    'success': False,
                    'message': 'Student not found'
                }
            
            student_info = dict(existing[0])
            
            # Delete student
            delete_query = """
            DELETE FROM students 
            WHERE id = ? AND teacher_id = ?
            """
            
            rows_deleted = db.execute_update(delete_query, (student_id, teacher_id))
            
            if rows_deleted:
                return {
                    'success': True,
                    'message': f'Deleted {student_info["name"]} from {student_info["subject_name"]}'
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to delete student'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error deleting student: {str(e)}'
            }
    
    @staticmethod
    def get_student_by_id(student_id, teacher_id):
        """Get a specific student by ID"""
        try:
            query = """
            SELECT id, name, subject_name, marks, created_at, updated_at
            FROM students 
            WHERE id = ? AND teacher_id = ?
            """
            
            results = db.execute_query(query, (student_id, teacher_id))
            
            if results:
                return {
                    'success': True,
                    'student': dict(results[0])
                }
            else:
                return {
                    'success': False,
                    'message': 'Student not found'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error fetching student: {str(e)}'
            }