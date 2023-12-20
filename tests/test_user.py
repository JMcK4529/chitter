from lib.user import User
from unittest.mock import Mock
import hashlib, os
from dotenv import load_dotenv
load_dotenv()

def test_user_constructs():
    id, username, email = None, "JMcK4529", os.getenv('CREATOR_EMAIL')
    binary_pass = os.getenv('CREATOR_PASS').encode('utf-8')
    hash_pass = hashlib.sha256(binary_pass).hexdigest()
    peep_mock = Mock()
    user = User(id, username, email, hash_pass, peeps=[peep_mock])
    assert user.id == id
    assert user.username == username
    assert user.email == email
    assert user.password == hash_pass
    assert user.peeps == [peep_mock]

def test_user_repr():
    binary_pass = os.getenv('CREATOR_PASS').encode('utf-8')
    hash_pass = hashlib.sha256(binary_pass).hexdigest()
    assert f"User(1, JMcK4529, {os.getenv('CREATOR_EMAIL')}, {hash_pass}, peeps=[])" == str(
        User(1, "JMcK4529", os.getenv('CREATOR_EMAIL'), hash_pass, peeps=[])
    )
    
def test_user_eq():
    id, username = None, "JMcK4529"
    peep_mock = Mock()
    binary_pass = os.getenv('CREATOR_PASS').encode('utf-8')
    hash_pass = hashlib.sha256(binary_pass).hexdigest()
    email = os.getenv('CREATOR_EMAIL')
    user1 = User(id, username, email, hash_pass, peeps=[peep_mock])
    user2 = User(id, username, email, hash_pass, peeps=[peep_mock])
    assert user1 == user2
    
def test_invalid_user_is_valid_returns_false():
    ids = [None, None, None]
    usernames = [None, "", "Test"]
    email = os.getenv('CREATOR_EMAIL')
    emails = [email, email, email]
    binary_pass = os.getenv('CREATOR_PASS').encode('utf-8')
    hash_pass = hashlib.sha256(binary_pass).hexdigest()
    hash_passes = [hash_pass, hash_pass, ""]
    peep_mocks = [[Mock()], None, None]
    for args in zip(ids, usernames, emails, hash_passes, peep_mocks):
        user = User(*args)
        assert user.is_valid() == False
    
def test_valid_user_is_valid_returns_true():
    ids = ["1", "2", "3"]
    usernames = ["astropig", "sillyname", "anuva1"]
    email = os.getenv('CREATOR_EMAIL')
    emails = [email, email, email]
    binary_pass = os.getenv('CREATOR_PASS').encode('utf-8')
    hash_pass = hashlib.sha256(binary_pass).hexdigest()
    hash_passes = [hash_pass, hash_pass, hash_pass]
    peep_mocks = [[Mock(), Mock()], [Mock()], None]
    for args in zip(ids, usernames, emails, hash_passes, peep_mocks):
        user = User(*args)
        assert user.is_valid()
    
def test_user_generate_errors():
    ids = [None, None, None, None, None]
    usernames = [None, "", "Test", "Test", "Test"]
    email = os.getenv('CREATOR_EMAIL')
    emails = [email, email, email, "", "test(at)example.com"]
    peep_mocks = [[Mock()], None, None, None, None]
    binary_pass = os.getenv('CREATOR_PASS').encode('utf-8')
    hash_pass = hashlib.sha256(binary_pass).hexdigest()
    hash_passes = [hash_pass, hash_pass, "", hash_pass, hash_pass]
    args = zip(ids, usernames, emails, hash_passes, peep_mocks)
    errors = ["Username can't be empty.",
              "Username can't be empty.", 
              "Invalid password.",
              "Email can't be empty.",
              "Email must be valid."]
    for args, errors in zip(args, errors):
        assert User(*args).generate_errors() == errors
