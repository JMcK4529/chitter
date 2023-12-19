from lib.peep import Peep

def test_peep_constructs():
    id, content, timestamp, user_id = None, "Content", "2023-12-01 11:11:11", "1"
    peep = Peep(id, content, timestamp, user_id)

    assert peep.id == id
    assert peep.content == content
    assert peep.timestamp == timestamp
    assert peep.user_id == user_id

def test_peep_repr():
    assert "Peep(None, Content, 2023-12-01 11:11:11, 1)" == str(
                    Peep(None, "Content", "2023-12-01 11:11:11", "1"))

def test_peep_eq():
    peep1 = Peep(None, "Content", "2023-12-01 11:11:11", "1")
    peep2 = Peep(None, "Content", "2023-12-01 11:11:11", "1")
    assert peep1 == peep2

def test_invalid_peep_is_valid_returns_false():
    ids = [None, None, None]
    contents = ["Content", "Content", None]
    timestamps = ["2023-12-01 11:11:11", None, "2023-12-01 11:11:11"]
    user_ids = [None, "1", "1"]
    for args in zip(ids, contents, timestamps, user_ids):
        peep = Peep(*args)
        assert peep.is_valid() == False

def test_valid_peep_is_valid_returns_true():
    ids = ["1", "2", "3"]
    contents = ["Content", "More content", "Yet another bit of content"]
    timestamps = ["2023-12-01 11:11:11", "2010-10-31 14:34:52", "2107-02-28 02:01:59"]
    user_ids = ["2", "3", "1"]
    for args in zip(ids, contents, timestamps, user_ids):
        peep = Peep(*args)
        assert peep.is_valid() == True

def test_peep_generate_errors():
    stamp = "2023-12-01 11:11:11"
    ids = [None, None, None, None, None, None, None]
    contents = ["Content", "Content", None, "Content", None, None, None]
    timestamps = [stamp, None, stamp, None, stamp, None, None]
    user_ids = [None, "1", "1", None, None, "1", None]
    args = zip(ids, contents, timestamps, user_ids)
    errors = [
        "User ID can't be empty.",
        "Timestamp must match the format 'YYYY-MM-DD hh:mm:ss'.",
        "Content can't be empty.",
        "Timestamp must match the format 'YYYY-MM-DD hh:mm:ss'. User ID can't be empty.",
        "Content can't be empty. User ID can't be empty.",
        "Content can't be empty. Timestamp must match the format 'YYYY-MM-DD hh:mm:ss'.",
        "Content can't be empty. Timestamp must match the format 'YYYY-MM-DD hh:mm:ss'. User ID can't be empty."
    ]
    for args, errors in zip(args, errors):
        peep = Peep(*args)
        assert peep.is_valid() == False
        assert peep.generate_errors() == errors