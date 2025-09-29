import pytest
import sqlite3

@pytest.fixture(scope="function")
def test_db():
    """Database in memory for testing"""
    conn = sqlite3.connect(':memory:')
    yield conn
    conn.close()

@pytest.fixture(scope="function")
def setup_test_db(test_db):
    """Clear database after each test"""
    cursor = test_db.cursor()
    yield cursor
    cursor.execute("DROP TABLE IF EXISTS cicle")
    cursor.execute("DROP TABLE IF EXISTS classroom")
    cursor.execute("DROP TABLE IF EXISTS course")
    cursor.execute("DROP TABLE IF EXISTS inscription")
    cursor.execute("DROP TABLE IF EXISTS payment")
    cursor.execute("DROP TABLE IF EXISTS student")
    cursor.execute("DROP TABLE IF EXISTS teacher")
    cursor.execute("DROP TABLE IF EXISTS team")
    cursor.execute("DROP TABLE IF EXISTS user")
    test_db.commit()
