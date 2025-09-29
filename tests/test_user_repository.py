from control.session.user_repository import UserRepository
from control.utils.encrypt_password import verify_password

def test_create_user_table(setup_test_db, test_db):
    """Test Create table User"""
    repo = UserRepository(test_db)
    repo.create_table()
    cursor = test_db.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='user'
    """)
    assert cursor.fetchone() is not None


def test_create_user(setup_test_db, test_db):
    """Test for creating a user"""
    repo = UserRepository(test_db)
    repo.create_table()
    username = 'test_user'
    role = 'admin'
    password = 'secure_password'
    
    repo.create_user(username, role, password)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT * FROM user WHERE user = ?', (username,))
    result = cursor.fetchone()
    print(f"RESULLLLLLLL: {result}")
    assert result is not None
    assert result[1] == username          # user
    assert result[2] == role              # role
    assert verify_password(result[3],password)  # password encriptado
    assert result[4] is not None          # created_at debe existir




def test_login_failure(setup_test_db, test_db):
    """Test failed login due to incorrect password"""
    repo = UserRepository(test_db)
    repo.create_table()
    username = 'test_user'
    role = 'admin'
    password = 'secure_password'
    
    repo.create_user(username, role, password)
    
    assert repo.login(username, 'wrong_password') is False


def test_login_nonexistent_user(setup_test_db, test_db):
    """Test failed login due to non-existent user"""
    repo = UserRepository(test_db)
    repo.create_table()
    
    assert repo.login('nonexistent_user', 'password') is False
