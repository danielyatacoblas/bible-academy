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
        'id_student': 1,
        'id_classroom': 10,
        'year': 2024,
        'cycle': 'A1',
        'date_taken': '2024-01-01',
        'type_material': 'Libro',
        'status': True,
        'date_inscription': '2024-01-01',
        'status_material': True
    }

    repo.insert_row(inscription_data)

    cursor = test_db.cursor()
    cursor.execute('SELECT * FROM inscription WHERE id_classroom = ?', (10,))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == 1               # id_student
    assert result[2] == 10              # id_classroom
    assert result[3] == 2024            # year
    assert result[4] == 'A1'            # cycle
    assert result[5] == '2024-01-01'    # date_taken
    assert result[6] == 'Libro'         # type_material
    assert result[7] == 1               # status → True (SQLite lo guarda como 1)
    assert result[8] == '2024-01-01'    # date_inscription
    assert result[9] == 1               # status_material → True (SQLite lo guarda como 1)


def test_get_inscription(setup_test_db, test_db):
    """Test for get inscription"""
    repo = InscriptionRepository(test_db)
    repo.create_table()
    inscription_data = {
        'id_student': 2,
        'id_classroom': 20,
        'year': 2024,
        'cycle': 'B1',
        'date_taken': '2024-02-15',
        'type_material': 'Cuaderno',
        'status': False,
        'date_inscription': '2024-02-15',
        'status_material': True
    }
    repo.insert_row(inscription_data)

    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM inscription WHERE id_classroom = ?', (20,))
    inscription_id = cursor.fetchone()[0]
    result = repo.get_row(inscription_id)

    assert result is not None
    assert result[1] == 2               # id_student
    assert result[2] == 20              # id_classroom
    assert result[6] == 'Cuaderno'      # type_material
    assert result[7] == 0               # status → False → 0
    assert result[8] == '2024-02-15'    # date_inscription
    assert result[9] == 1               # status_material


def test_update_inscription(setup_test_db, test_db):
    """Test for update inscription"""
    repo = InscriptionRepository(test_db)
    repo.create_table()
    inscription_data = {
        'id_student': 3,
        'id_classroom': 30,
        'year': 2024,
        'cycle': 'A2',
        'date_taken': '2024-03-10',
        'type_material': 'Manual',
        'status': True,
        'date_inscription': '2024-03-10',
        'status_material': False
    }
    repo.insert_row(inscription_data)

    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM inscription WHERE id_classroom = ?', (30,))
    inscription_id = cursor.fetchone()[0]

    update_data = {
        'type_material': 'Revista',
        'status_material': True
    }
    repo.update_row(update_data, {'id': inscription_id})

    result = repo.get_row(inscription_id)
    assert result is not None
    assert result[6] == 'Revista'   # type_material actualizado
    assert result[9] == 1           # status_material actualizado


def test_delete_inscription(setup_test_db, test_db):
    """Test for delete inscription"""
    repo = InscriptionRepository(test_db)
    repo.create_table()
    inscription_data = {
        'id_student': 4,
        'id_classroom': 40,
        'year': 2024,
        'cycle': 'B2',
        'date_taken': '2024-04-01',
        'type_material': 'Guía',
        'status': True,
        'date_inscription': '2024-04-01',
        'status_material': False
    }
    repo.insert_row(inscription_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM inscription WHERE id_classroom = ?', (40,))
    inscription_id = cursor.fetchone()[0]
    
    repo.delete_row({'id': inscription_id})
    
    result = repo.get_row(inscription_id)
    assert result is None
