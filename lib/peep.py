import re

class Peep:
    def __init__(self, id, content, timestamp, user_id):
        self.id = id
        self.content = content
        self.timestamp = timestamp
        self.user_id = user_id

    def __repr__(self):
        return f"Peep({self.id}, {self.content}, {self.timestamp}, {self.user_id})"
    
    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def is_valid(self):
        if self.content in [None, ""]:
            return False
        if self.timestamp in [None, ""]:
            return False
        elif not re.fullmatch(
            r"^[12][0-9]{3}\-[01][0-9]\-[0-3][0-9]\s[0-2][0-9]\:[0-5][0-9]\:[0-5][0-9]$", 
                        self.timestamp):
            return False
        if self.user_id in [None, ""]:
            return False
        else:
            return True
        
    def generate_errors(self):
        errors = []
        if self.content in [None, ""]:
            errors.append("Content can't be empty.")
        if self.timestamp in [None, ""]:
            errors.append("Timestamp must match the format 'YYYY-MM-DD hh:mm:ss'.")
        elif not re.fullmatch(
            r"^[12][0-9]{3}\-[01][0-9]\-[0-3][0-9]\s[0-2][0-9]\:[0-5][0-9]\:[0-5][0-9]$", 
                        self.timestamp):
            errors.append("Timestamp must match the format 'YYYY-MM-DD hh:mm:ss'.")
        if self.user_id in [None, ""]:
            errors.append("User ID can't be empty.")
        return " ".join(errors)