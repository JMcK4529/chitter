from lib.user import User
from lib.peep import Peep
from lib.user_repository import UserRepository
from unittest.mock import Mock
import pytest
from datetime import datetime

def test_user_repo_constructs():
    try:
        connection = Mock()
        repo = UserRepository(connection)
    except:
        raise AssertionError(
            "UserRepository class does not construct properly"
            )
    
def test_user_repo_all(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = UserRepository(db_connection)
    assert repo.all() == [
        User(1, 'JMcK4529', peeps=[])
    ]

def test_user_repo_find(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = UserRepository(db_connection)
    assert repo.find(1) == User(1, 'JMcK4529', peeps=[])
    with pytest.raises(Exception) as err:
        repo.find(2)
    assert str(err.value) == "User with ID 2 does not exist"

def test_user_repo_find_with_peeps(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = UserRepository(db_connection)
    fwp = repo.find_with_peeps(1)
    print(type(fwp.peeps[0].timestamp))
    assert repo.find_with_peeps(1) == \
        User(
            1, 'JMcK4529', 
            peeps=[
                Peep(
                    1, 
                    'Welcome to Chitter!', 
                    datetime.fromisoformat('2023-12-07 11:13:15'),
                    1
                    )
                ]
            )
    with pytest.raises(Exception) as err:
        repo.find_with_peeps(2)
    assert str(err.value) == "User with ID 2 does not exist"

def test_user_repo_create(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = UserRepository(db_connection)
    assert repo.create(User(None, 'User2', peeps=None)) == \
                                        User(2, 'User2', peeps=[])

def test_user_repo_delete(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = UserRepository(db_connection)
    assert repo.create(User(None, 'User2', peeps=None)) == \
                                        User(2, 'User2', peeps=[])
    assert repo.delete(2) == None
    assert repo.all() == [
        User(1, 'JMcK4529', peeps=[])
    ]