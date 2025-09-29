from control.cicle_repository import CicleRepository

def test_create_cicle_table(setup_test_db, test_db):
    """Test Create table Cicle"""
    repo = CicleRepository(test_db)
    repo.create_table()
    cursor = test_db.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='cicle'
    """)
    assert cursor.fetchone() is not None

def test_insert_cicle(setup_test_db, test_db):
    """Test for insert to cicle"""
    repo = CicleRepository(test_db)
    repo.create_table()
    cicle_data = {
        'cicle': 'A1',
        'date_start': '2024-01-01',
        'date_end': '2024-06-30',
        'manager': 'Test Manager'
    }
    
    repo.insert_row(cicle_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT * FROM cicle WHERE cicle = ?', ('A1',))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == 'A1'  
    assert result[2] == '2024-01-01' 
    assert result[3] == '2024-06-30'  
    assert result[4] == 'Test Manager'  

def test_get_cicle(setup_test_db, test_db):
    """Test for get cicle"""
    repo = CicleRepository(test_db)
    repo.create_table()
    cicle_data = {
        'cicle': 'A1',
        'date_start': '2024-01-01',
        'date_end': '2024-06-30',
        'manager': 'Test Manager'
    }
    repo.insert_row(cicle_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM cicle WHERE cicle = ?', ('A1',))
    cicle_id = cursor.fetchone()[0]
    result = repo.get_row(cicle_id)
    
    assert result is not None
    assert result[1] == 'A1'  
    assert result[2] == '2024-01-01'  
    assert result[3] == '2024-06-30' 
    assert result[4] == 'Test Manager' 

def test_update_cicle(setup_test_db, test_db):
    """Test for update cicle"""
    repo = CicleRepository(test_db)
    repo.create_table()
    cicle_data = {
        'cicle': 'A1',
        'date_start': '2024-01-01',
        'date_end': '2024-06-30',
        'manager': 'Test Manager'
    }
    repo.insert_row(cicle_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM cicle WHERE cicle = ?', ('A1',))
    cicle_id = cursor.fetchone()[0]
    
    update_data = {
        'manager': 'New Manager'
    }
    repo.update_row(cicle_id, update_data)
    
    result = repo.get_row(cicle_id)
    assert result is not None
    assert result[4] == 'New Manager'

def test_delete_cicle(setup_test_db, test_db):
    """Test for delete cicle"""
    repo = CicleRepository(test_db)
    repo.create_table()
    cicle_data = {
        'cicle': 'A1',
        'date_start': '2024-01-01',
        'date_end': '2024-06-30',
        'manager': 'Test Manager'
    }
    repo.insert_row(cicle_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM cicle WHERE cicle = ?', ('A1',))
    cicle_id = cursor.fetchone()[0]
    
    repo.delete_row(cicle_id)
    
    result = repo.get_row(cicle_id)
    assert result is None