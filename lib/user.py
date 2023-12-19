import re

class User:
    def __init__(self, id, username, peeps=None):
        self.id = id
        self.username = username
        self.peeps = peeps or []
    
    def __repr__(self):
        return f"User({self.id}, {self.username}, peeps={self.peeps})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def is_valid(self):
        if self.username in [None, ""]:
            return False
        else:
            return True
    
    def generate_errors(self):
        if self.username in [None, ""]:
            return "Username can't be empty."