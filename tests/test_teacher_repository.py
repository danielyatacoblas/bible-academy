from control.teacher_repository import TeacherRepository

def test_create_teacher_table(setup_test_db, test_db):
    """Test Create table Teacher"""
    repo = TeacherRepository(test_db)
    repo.create_table()
    cursor = test_db.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='teacher'
    """)
    assert cursor.fetchone() is not None


def test_insert_teacher(setup_test_db, test_db):
    """Test for insert teacher"""
    repo = TeacherRepository(test_db)
    repo.create_table()
    teacher_data = {
        'name': 'Jane',
        'lastname': 'Smith',
        'phone': '987654321',
        'date_baptism': '2015-03-10',
        'date_of_birth': '1980-07-15',
        'id_team': 2
    }
    
    repo.insert_row(teacher_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT * FROM teacher WHERE name = ?', ('Jane',))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == 'Jane'
    assert result[2] == 'Smith'
    assert result[3] == '987654321'
    assert result[4] == '2015-03-10'
    assert result[5] == '1980-07-15'
    assert result[6] == 2


def test_get_teacher(setup_test_db, test_db):
    """Test for get teacher"""
    repo = TeacherRepository(test_db)
    repo.create_table()
    teacher_data = {
        'name': 'Jane',
        'lastname': 'Smith',
        'phone': '987654321',
        'date_baptism': '2015-03-10',
        'date_of_birth': '1980-07-15',
        'id_team': 2
    }
    repo.insert_row(teacher_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM teacher WHERE name = ?', ('Jane',))
    teacher_id = cursor.fetchone()[0]
    result = repo.get_row(teacher_id)
    
    assert result is not None
    assert result[1] == 'Jane'
    assert result[2] == 'Smith'
    assert result[3] == '987654321'
    assert result[4] == '2015-03-10'
    assert result[5] == '1980-07-15'
    assert result[6] == 2


def test_update_teacher(setup_test_db, test_db):
    """Test for update teacher"""
    repo = TeacherRepository(test_db)
    repo.create_table()
    teacher_data = {
        'name': 'Jane',
        'lastname': 'Smith',
        'phone': '987654321',
        'date_baptism': '2015-03-10',
        'date_of_birth': '1980-07-15',
        'id_team': 2
    }
    repo.insert_row(teacher_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM teacher WHERE name = ?', ('Jane',))
    teacher_id = cursor.fetchone()[0]
    
    update_data = {
        'phone': '999888777'
    }
    repo.update_row(teacher_id, update_data)
    
    result = repo.get_row(teacher_id)
    assert result is not None
    assert result[3] == '999888777'  # phone actualizado


def test_delete_teacher(setup_test_db, test_db):
    """Test for delete teacher"""
    repo = TeacherRepository(test_db)
    repo.create_table()
    teacher_data = {
        'name': 'Jane',
        'lastname': 'Smith',
        'phone': '987654321',
        'date_baptism': '2015-03-10',
        'date_of_birth': '1980-07-15',
        'id_team': 2
    }
    repo.insert_row(teacher_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM teacher WHERE name = ?', ('Jane',))
    teacher_id = cursor.fetchone()[0]
    
    repo.delete_row(teacher_id)
    
    result = repo.get_row(teacher_id)
    assert result is None
