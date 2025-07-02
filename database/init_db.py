import bcrypt
from database.db_connection import db

def create_tables():
    """Create database tables"""
    
    # Teachers table
    teachers_table = """
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        full_name VARCHAR(100) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    # Students table
    students_table = """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        subject_name VARCHAR(100) NOT NULL,
        marks INTEGER NOT NULL,
        teacher_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES teachers (id),
        UNIQUE(name, subject_name, teacher_id)
    )
    """
    
    try:
        db.execute_update(teachers_table)
        db.execute_update(students_table)
        print("Tables created successfully!")
        return True
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

def create_sample_data():
    """Create sample teachers and students for testing"""
    
    # Create sample teacher
    password = "teacher123"
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    teacher_query = """
    INSERT OR IGNORE INTO teachers (username, email, password_hash, full_name)
    VALUES (?, ?, ?, ?)
    """
    
    try:
        teacher_id = db.execute_insert(teacher_query, (
            'teacher1',
            'teacher@example.com',
            hashed_password.decode('utf-8'),
            'John Smith'
        ))
        
        if teacher_id:
            # Create sample students
            students_data = [
                ('Alice Johnson', 'Mathematics', 85),
                ('Bob Smith', 'Physics', 78),
                ('Carol Davis', 'Chemistry', 92),
                ('David Wilson', 'Mathematics', 76),
                ('Eve Brown', 'Physics', 88),
                ('Frank Miller', 'Chemistry', 94),
                ('Grace Lee', 'Mathematics', 89),
                ('Henry Garcia', 'Physics', 82)
            ]
            
            student_query = """
            INSERT OR IGNORE INTO students (name, subject_name, marks, teacher_id)
            VALUES (?, ?, ?, ?)
            """
            
            for name, subject, marks in students_data:
                db.execute_insert(student_query, (name, subject, marks, teacher_id))
        
        print("Sample data created successfully!")
        print("Login credentials:")
        print("Username: teacher1")
        print("Password: teacher123")
        return True
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        return False

def initialize_database():
    """Initialize the database with tables and sample data"""
    print("Initializing database...")
    
    if create_tables():
        if create_sample_data():
            print("Database initialization completed successfully!")
        else:
            print("Database tables created, but sample data creation failed.")
    else:
        print("Database initialization failed!")

if __name__ == "__main__":
    initialize_database()