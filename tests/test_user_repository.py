from lib.user import User
from lib.peep import Peep
from lib.user_repository import UserRepository
from unittest.mock import Mock
import pytest, os, hashlib
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(override=True)

hash_pass = hashlib.sha256(os.getenv('CREATOR_PASS').encode('utf-8')).hexdigest()
hash_pass_test = hashlib.sha256("TESTPASSWORD".encode('utf-8')).hexdigest()
email = os.getenv('CREATOR_EMAIL')

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
    print(os.environ)
    repo = UserRepository(db_connection)
    assert repo.all() == [
        User(1, 'JMcK4529', email, hash_pass, peeps=[])
    ]

def test_user_repo_find(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = UserRepository(db_connection)
    assert repo.find(1) == User(1, 'JMcK4529', email, hash_pass, peeps=[])
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
            1, 'JMcK4529', email, hash_pass,
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
    assert repo.create(User(None, 'User2', "test2@mail.com", hash_pass_test, peeps=None)) == \
                                        User(2, 'User2', "test2@mail.com", hash_pass_test, peeps=[])

def test_user_repo_delete(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = UserRepository(db_connection)
    assert repo.create(User(None, 'User2', "test2@mail.com", hash_pass_test, peeps=None)) == \
                                        User(2, 'User2', "test2@mail.com", hash_pass_test, peeps=[])
    assert repo.delete(2) == None
    assert repo.all() == [
        User(1, 'JMcK4529', email, hash_pass, peeps=[])
    ]

def test_user_repo_find_by_email(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = UserRepository(db_connection)
    assert repo.find_by_email(email) == \
        User(1, 'JMcK4529', email, hash_pass, peeps=[])
    
def test_user_repo_find_by_username(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = UserRepository(db_connection)
    assert repo.find_by_username('JMcK4529') == \
        User(1, 'JMcK4529', email, hash_pass, peeps=[])
    
def test_user_repo_check_password(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = UserRepository(db_connection)
    assert repo.check_password(email, os.getenv('CREATOR_PASS'))
    assert repo.check_password('JMcK4529', os.getenv('CREATOR_PASS'))
    assert repo.check_password(email, 'failure') == False
    with pytest.raises(ValueError) as err:
        repo.check_password('NonUser', 'fakepassword')
    assert str(err.value) == "NonUser does not exist"