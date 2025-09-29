from control.course_repository import CourseRepository

def test_create_course_table(setup_test_db, test_db):
    """Test Create table Course"""
    repo = CourseRepository(test_db)
    repo.create_table()
    cursor = test_db.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='course'
    """)
    assert cursor.fetchone() is not None

def test_insert_course(setup_test_db, test_db):
    """Test for insert to course"""
    repo = CourseRepository(test_db)
    repo.create_table()
    course_data = {
        'name': 'Python 101',
        'level': 'V',
    }
    
    repo.insert_row(course_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT * FROM course WHERE name = ?', ('Python 101',))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == 'Python 101'  
    assert result[2] == 'V' 

def test_get_course(setup_test_db, test_db):
    """Test for get course"""
    repo = CourseRepository(test_db)
    repo.create_table()
    course_data = {
        'name': 'Python 101',
        'level': 'V',
    }
    repo.insert_row(course_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM course WHERE name = ?', ('Python 101',))
    course_id = cursor.fetchone()[0]
    result = repo.get_row(course_id)
    
    assert result is not None
    assert result[1] == 'Python 101'  
    assert result[2] == 'V' 

def test_update_course(setup_test_db, test_db):
    """Test for update course"""
    repo = CourseRepository(test_db)
    repo.create_table()
    course_data = {
        'name': 'Python 101',
        'level': 'V'
    }
    repo.insert_row(course_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM course WHERE name = ?', ('Python 101',))
    course_id = cursor.fetchone()[0]
    
    update_data = {
        'name': 'Python 102'
    }
    repo.update_row(course_id, update_data)
    
    result = repo.get_row(course_id)
    assert result is not None
    assert result[1] == 'Python 102'

def test_delete_course(setup_test_db, test_db):
    """Test for delete course"""
    repo = CourseRepository(test_db)
    repo.create_table()
    course_data = {
        'name': 'Python 101',
        'level': 'V'
    }
    repo.insert_row(course_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM course WHERE name = ?', ('Python 101',))
    course_id = cursor.fetchone()[0]
    
    repo.delete_row(course_id)
    
    result = repo.get_row(course_id)
    assert result is None