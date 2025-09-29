from control.payment_repository import PaymentRepository

def test_create_payment_table(setup_test_db, test_db):
    """Test Create table Payment"""
    repo = PaymentRepository(test_db)
    repo.create_table()
    cursor = test_db.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='payment'
    """)
    assert cursor.fetchone() is not None


def test_insert_payment(setup_test_db, test_db):
    """Test for insert to payment"""
    repo = PaymentRepository(test_db)
    repo.create_table()
    payment_data = {
        'method_payment': 'Efectivo',
        'amount': 500,
        'created_datetime': '2024-01-01 10:00:00',
        'id_inscription': 1
    }
    
    repo.insert_row(payment_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT * FROM payment WHERE id_inscription = ?', (1,))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == 'Efectivo'
    assert result[2] == 500 
    assert result[3] == '2024-01-01 10:00:00'
    assert result[4] == 1


def test_get_payment(setup_test_db, test_db):
    """Test for get payment"""
    repo = PaymentRepository(test_db)
    repo.create_table()
    payment_data = {
        'method_payment': 'Tarjeta',
        'amount': 800,
        'created_datetime': '2024-02-15 14:30:00',
        'id_inscription': 2
    }
    repo.insert_row(payment_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM payment WHERE id_inscription = ?', (2,))
    payment_id = cursor.fetchone()[0]
    result = repo.get_row(payment_id)
    
    assert result is not None
    assert result[1] == 'Tarjeta'
    assert result[2] == 800  
    assert result[3] == '2024-02-15 14:30:00'
    assert result[4] == 2


def test_update_payment(setup_test_db, test_db):
    """Test for update payment"""
    repo = PaymentRepository(test_db)
    repo.create_table()
    payment_data = {
        'method_payment': 'Yape',
        'amount': 300,
        'created_datetime': '2024-03-01 09:00:00',
        'id_inscription': 3
    }
    repo.insert_row(payment_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM payment WHERE id_inscription = ?', (3,))
    payment_id = cursor.fetchone()[0]
    
    update_data = {
        'amount': 450,
        'method_payment': 'Plin'
    }
    repo.update_row(payment_id, update_data)
    
    result = repo.get_row(payment_id)
    assert result is not None
    assert result[1] == 'Plin'
    assert result[2] == 450


def test_delete_payment(setup_test_db, test_db):
    """Test for delete payment"""
    repo = PaymentRepository(test_db)
    repo.create_table()
    payment_data = {
        'method_payment': 'Transferencia',
        'amount': 1000,
        'created_datetime': '2024-04-10 16:00:00',
        'id_inscription': 4
    }
    repo.insert_row(payment_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM payment WHERE id_inscription = ?', (4,))
    payment_id = cursor.fetchone()[0]
    
    repo.delete_row(payment_id)
    
    result = repo.get_row(payment_id)
    assert result is None
