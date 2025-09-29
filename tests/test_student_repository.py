from control.student_repository import StudentRepository

def test_create_student_table(setup_test_db, test_db):
    """Test Create table Student"""
    repo = StudentRepository(test_db)
    repo.create_table()
    cursor = test_db.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='student'
    """)
    assert cursor.fetchone() is not None


def test_insert_student(setup_test_db, test_db):
    """Test for insert student"""
    repo = StudentRepository(test_db)
    repo.create_table()
    student_data = {
        'name': 'John',
        'lastname': 'Doe',
        'phone': '987654321',
        'date_baptism': '2020-05-01',
        'date_of_birth': '2000-01-01',
        'id_team': 1
    }
    
    repo.insert_row(student_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT * FROM student WHERE name = ?', ('John',))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == 'John'
    assert result[2] == 'Doe'
    assert result[3] == '987654321'
    assert result[4] == '2020-05-01'
    assert result[5] == '2000-01-01'
    assert result[6] == 1


def test_get_student(setup_test_db, test_db):
    """Test for get student"""
    repo = StudentRepository(test_db)
    repo.create_table()
    student_data = {
        'name': 'John',
        'lastname': 'Doe',
        'phone': '987654321',
        'date_baptism': '2020-05-01',
        'date_of_birth': '2000-01-01',
        'id_team': 1
    }
    repo.insert_row(student_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM student WHERE name = ?', ('John',))
    student_id = cursor.fetchone()[0]
    result = repo.get_row(student_id)
    
    assert result is not None
    assert result[1] == 'John'
    assert result[2] == 'Doe'
    assert result[3] == '987654321'
    assert result[4] == '2020-05-01'
    assert result[5] == '2000-01-01'
    assert result[6] == 1


def test_update_student(setup_test_db, test_db):
    """Test for update student"""
    repo = StudentRepository(test_db)
    repo.create_table()
    student_data = {
        'name': 'John',
        'lastname': 'Doe',
        'phone': '987654321',
        'date_baptism': '2020-05-01',
        'date_of_birth': '2000-01-01',
        'id_team': 1
    }
    repo.insert_row(student_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM student WHERE name = ?', ('John',))
    student_id = cursor.fetchone()[0]
    
    update_data = {
        'phone': '999888777'
    }
    repo.update_row(student_id, update_data)
    
    result = repo.get_row(student_id)
    assert result is not None
    assert result[3] == '999888777'  # phone actualizado


def test_delete_student(setup_test_db, test_db):
    """Test for delete student"""
    repo = StudentRepository(test_db)
    repo.create_table()
    student_data = {
        'name': 'John',
        'lastname': 'Doe',
        'phone': '987654321',
        'date_baptism': '2020-05-01',
        'date_of_birth': '2000-01-01',
        'id_team': 1
    }
    repo.insert_row(student_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM student WHERE name = ?', ('John',))
    student_id = cursor.fetchone()[0]
    
    repo.delete_row(student_id)
    
    result = repo.get_row(student_id)
    assert result is None
