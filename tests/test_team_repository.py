from control.team_repository import TeamRepository

def test_create_team_table(setup_test_db, test_db):
    """Test Create table Team"""
    repo = TeamRepository(test_db)
    repo.create_table()
    cursor = test_db.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='team'
    """)
    assert cursor.fetchone() is not None


def test_insert_team(setup_test_db, test_db):
    """Test for insert to team"""
    repo = TeamRepository(test_db)
    repo.create_table()
    team_data = {
        'name': 'Team Alpha',
        'age_start': 10,
        'age_end': 15,
        'gender': 'Male'
    }
    
    repo.insert_row(team_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT * FROM team WHERE name = ?', ('Team Alpha',))
    result = cursor.fetchone()
    assert result is not None
    assert result[1] == 'Team Alpha'   # name
    assert result[2] == 10             # age_start
    assert result[3] == 15             # age_end
    assert result[4] == 'Male'         # gender


def test_get_team(setup_test_db, test_db):
    """Test for get team"""
    repo = TeamRepository(test_db)
    repo.create_table()
    team_data = {
        'name': 'Team Alpha',
        'age_start': 10,
        'age_end': 15,
        'gender': 'Male'
    }
    repo.insert_row(team_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM team WHERE name = ?', ('Team Alpha',))
    team_id = cursor.fetchone()[0]
    result = repo.get_row(team_id)
    
    assert result is not None
    assert result[1] == 'Team Alpha'
    assert result[2] == 10
    assert result[3] == 15
    assert result[4] == 'Male'


def test_update_team(setup_test_db, test_db):
    """Test for update team"""
    repo = TeamRepository(test_db)
    repo.create_table()
    team_data = {
        'name': 'Team Alpha',
        'age_start': 10,
        'age_end': 15,
        'gender': 'Male'
    }
    repo.insert_row(team_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM team WHERE name = ?', ('Team Alpha',))
    team_id = cursor.fetchone()[0]
    
    update_data = {
        'age_end': 18,
        'gender': 'Female'
    }
    repo.update_row(team_id, update_data)
    
    result = repo.get_row(team_id)
    assert result is not None
    assert result[3] == 18       # age_end actualizado
    assert result[4] == 'Female' # gender actualizado


def test_delete_team(setup_test_db, test_db):
    """Test for delete team"""
    repo = TeamRepository(test_db)
    repo.create_table()
    team_data = {
        'name': 'Team Alpha',
        'age_start': 10,
        'age_end': 15,
        'gender': 'Male'
    }
    repo.insert_row(team_data)
    
    cursor = test_db.cursor()
    cursor.execute('SELECT id FROM team WHERE name = ?', ('Team Alpha',))
    team_id = cursor.fetchone()[0]
    
    repo.delete_row(team_id)
    
    result = repo.get_row(team_id)
    assert result is None
