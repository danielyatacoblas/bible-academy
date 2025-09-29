from control.inscription_repository import InscriptionRepository

def test_create_inscription_table(setup_test_db, test_db):
    """Test Create table Inscription"""
    repo = InscriptionRepository(test_db)
    repo.create_table()
    cursor = test_db.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='inscription'
    """)
    assert cursor.fetchone() is not None


def test_insert_inscription(setup_test_db, test_db):
    """Test for insert to inscription"""
    repo = InscriptionRepository(test_db)
    repo.create_table()
    inscription_data = {
        'status': True,
        'date_inscription': '2024-01-01',
        'type_material': 'Libro',
        'status_material': True,
        'id_classroom': 10
    }
    
    repo.insert_row(inscription_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT * FROM inscription WHERE id_classroom = ?', (10,))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == 1           # status → True (SQLite lo guarda como 1)
    assert result[2] == '2024-01-01'
    assert result[3] == 'Libro'
    assert result[4] == 1           # status_material → True (SQLite lo guarda como 1)
    assert result[5] == 10


def test_get_inscription(setup_test_db, test_db):
    """Test for get inscription"""
    repo = InscriptionRepository(test_db)
    repo.create_table()
    inscription_data = {
        'status': False,
        'date_inscription': '2024-02-15',
        'type_material': 'Cuaderno',
        'status_material': True,
        'id_classroom': 20
    }
    repo.insert_row(inscription_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM inscription WHERE id_classroom = ?', (20,))
    inscription_id = cursor.fetchone()[0]
    result = repo.get_row(inscription_id)
    
    assert result is not None
    assert result[1] == 0           # False → 0
    assert result[2] == '2024-02-15'
    assert result[3] == 'Cuaderno'
    assert result[4] == 1
    assert result[5] == 20


def test_update_inscription(setup_test_db, test_db):
    """Test for update inscription"""
    repo = InscriptionRepository(test_db)
    repo.create_table()
    inscription_data = {
        'status': True,
        'date_inscription': '2024-03-10',
        'type_material': 'Manual',
        'status_material': False,
        'id_classroom': 30
    }
    repo.insert_row(inscription_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM inscription WHERE id_classroom = ?', (30,))
    inscription_id = cursor.fetchone()[0]
    
    update_data = {
        'type_material': 'Revista',
        'status_material': True
    }
    repo.update_row(inscription_id, update_data)
    
    result = repo.get_row(inscription_id)
    assert result is not None
    assert result[3] == 'Revista'
    assert result[4] == 1


def test_delete_inscription(setup_test_db, test_db):
    """Test for delete inscription"""
    repo = InscriptionRepository(test_db)
    repo.create_table()
    inscription_data = {
        'status': True,
        'date_inscription': '2024-04-01',
        'type_material': 'Guía',
        'status_material': False,
        'id_classroom': 40
    }
    repo.insert_row(inscription_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM inscription WHERE id_classroom = ?', (40,))
    inscription_id = cursor.fetchone()[0]
    
    repo.delete_row(inscription_id)
    
    result = repo.get_row(inscription_id)
    assert result is None
