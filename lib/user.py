import re

class User:
    def __init__(self, id, username, email, password, peeps=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.peeps = peeps or []
    
    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.email}, {self.password}, peeps={self.peeps})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def is_valid(self):
        if self.username in [None, ""]:
            return False
        elif self.email in [None, ""]:
            return False
        elif not re.match(
            r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", self.email,
            re.IGNORECASE
        ):
            return False
        elif self.password in [None, ""]:
            return False
        else:
            return True
    
    def generate_errors(self):
        if self.username in [None, ""]:
            return "Username can't be empty."
        elif self.email in [None, ""]:
            return "Email can't be empty."
        elif not re.match(
            r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", self.email,
            re.IGNORECASE
        ):
            return "Email must be valid."
        elif self.password in [None, ""]:
            return "Invalid password."