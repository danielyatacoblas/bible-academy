from control.classroom_repository import ClassroomRepository

def test_create_classroom_table(setup_test_db, test_db):
    """Test Create table Classroom"""
    repo = ClassroomRepository(test_db)
    repo.create_table()
    cursor = test_db.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='classroom'
    """)
    assert cursor.fetchone() is not None

def test_insert_classroom(setup_test_db, test_db):
    """Test for insert to classroom"""
    repo = ClassroomRepository(test_db)
    repo.create_table()
    classroom_data = {
        'name': 'A1',
        'start_date': '2024-01-01',
        'end_date': '2024-06-30',
        'id_teacher': 1,
        'id_course': 1,
        'id_cicle': 1
    }
    
    repo.insert_row(classroom_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT * FROM classroom WHERE name = ?', ('A1',))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == 'A1'  
    assert result[2] == '2024-01-01' 
    assert result[3] == '2024-06-30'  
def test_get_classroom(setup_test_db, test_db):
    """Test for get classroom"""
    repo = ClassroomRepository(test_db)
    repo.create_table()
    classroom_data = {
        'name': 'A1',
        'start_date': '2024-01-01',
        'end_date': '2024-06-30',
        'id_teacher': 1,
        'id_course': 1,
        'id_cicle': 1
    }
    repo.insert_row(classroom_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM classroom WHERE name = ?', ('A1',))
    classroom_id = cursor.fetchone()[0]
    result = repo.get_row(classroom_id)
    
    assert result is not None
    assert result[1] == 'A1'  
    assert result[2] == '2024-01-01'  
    assert result[3] == '2024-06-30' 

def test_update_classroom(setup_test_db, test_db):
    """Test for update classroom"""
    repo = ClassroomRepository(test_db)
    repo.create_table()
    classroom_data = {
        'name': 'A1',
        'start_date': '2024-01-01',
        'end_date': '2024-06-30',
        'id_teacher': 1,
        'id_course': 1,
        'id_cicle': 1
    }
    repo.insert_row(classroom_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM classroom WHERE name = ?', ('A1',))
    classroom_id = cursor.fetchone()[0]
    
    update_data = {
        'name': 'A02'
    }
    repo.update_row(classroom_id, update_data)
    
    result = repo.get_row(classroom_id)
    assert result is not None
    assert result[1] == 'A02'

def test_delete_classroom(setup_test_db, test_db):
    """Test for delete classroom"""
    repo = ClassroomRepository(test_db)
    repo.create_table()
    classroom_data = {
        'name': 'A1',
        'start_date': '2024-01-01',
        'end_date': '2024-06-30',
        'id_teacher': 1,
        'id_course': 1,
        'id_cicle': 1
    }
    repo.insert_row(classroom_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM classroom WHERE name = ?', ('A1',))
    classroom_id = cursor.fetchone()[0]
    
    repo.delete_row(classroom_id)
    
    result = repo.get_row(classroom_id)
    assert result is None