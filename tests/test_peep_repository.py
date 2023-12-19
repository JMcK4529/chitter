from lib.peep import Peep
from lib.peep_repository import PeepRepository
from lib.user import User
from unittest.mock import Mock
import pytest
from datetime import datetime

def test_peep_repo_constructs():
    try:
        connection = Mock()
        repo = PeepRepository(connection)
    except:
        raise AssertionError(
            "PeepRepository class does not construct properly"
            )
    
def test_peep_repo_all(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = PeepRepository(db_connection)
    assert repo.all() == [
        Peep(1, 'Welcome to Chitter!', 
             datetime.fromisoformat('2023-12-07 11:13:15'), 1)
    ]

def test_peep_repo_find(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = PeepRepository(db_connection)
    assert repo.find(1) == Peep(1, 'Welcome to Chitter!', 
                            datetime.fromisoformat('2023-12-07 11:13:15'), 1)
    with pytest.raises(Exception) as err:
        repo.find(2)
    assert str(err.value) == "Peep with ID 2 does not exist"

def test_peep_repo_create(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = PeepRepository(db_connection)
    assert repo.create(Peep(None, 'Peep2', '2024-01-01 12:00:00', 1)) == \
            Peep(2, 'Peep2', datetime.fromisoformat('2024-01-01 12:00:00'), 1)

def test_peep_repo_delete(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repo = PeepRepository(db_connection)
    assert repo.create(Peep(None, 'Peep2', '2024-01-01 12:00:00', 1)) == \
            Peep(2, 'Peep2', datetime.fromisoformat('2024-01-01 12:00:00'), 1)
    assert repo.delete(2) == None
    assert repo.all() == [
        Peep(1, 'Welcome to Chitter!', 
             datetime.fromisoformat('2023-12-07 11:13:15'), 1)
    ]