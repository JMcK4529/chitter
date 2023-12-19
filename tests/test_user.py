from lib.user import User
from unittest.mock import Mock

def test_user_constructs():
    id, username = None, "JMcK4529"
    peep_mock = Mock()
    user = User(id, username, peeps=[peep_mock])
    assert user.id == id
    assert user.username == username
    assert user.peeps == [peep_mock]

def test_user_repr():
    assert "User(1, JMcK4529, peeps=[])" == str(
        User(1, "JMcK4529", peeps=[])
    )
    
def test_user_eq():
    id, username = None, "JMcK4529"
    peep_mock = Mock()
    user1 = User(id, username, peeps=[peep_mock])
    user2 = User(id, username, peeps=[peep_mock])
    assert user1 == user2
    
def test_invalid_user_is_valid_returns_false():
    ids = [None, None]
    usernames = [None, ""]
    peep_mocks = [[Mock()], None]
    for args in zip(ids, usernames, peep_mocks):
        user = User(*args)
        assert user.is_valid() == False
    
def test_valid_user_is_valid_returns_true():
    ids = ["1", "2", "3"]
    usernames = ["astropig", "sillyname", "anuva1"]
    peep_mocks = [[Mock(), Mock()], [Mock()], None]
    for args in zip(ids, usernames, peep_mocks):
        user = User(*args)
        assert user.is_valid()
    
def test_user_generate_errors():
    ids = [None, None]
    usernames = [None, ""]
    peep_mocks = [[Mock()], None]
    args = zip(ids, usernames, peep_mocks)
    errors = ["Username can't be empty.",
              "Username can't be empty."]
    for args, errors in zip(args, errors):
        assert User(*args).generate_errors() == errors
