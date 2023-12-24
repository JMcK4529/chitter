from lib.user import User
from lib.peep import Peep
import hashlib

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        """Returns all users without associated peeps."""
        users = []
        rows = self._connection.execute(
            """SELECT * FROM users;"""
            )
        for row in rows:
            users.append(
                User(row['id'], 
                     row['username'], 
                     row['email'], 
                     row['password'])
            )
        return users
    
    def find(self, id):
        """Returns the user with id=id."""
        try:
            row = self._connection.execute(
                """
                SELECT * FROM users WHERE id=%s;
                """, [id]
            )[0]
            return User(row['id'], 
                        row['username'], 
                        row['email'], 
                        row['password'])
        except:
            raise ValueError(f"User with ID {id} does not exist")
    
    def find_with_peeps(self, id):
        """Returns the user with id=id, including its peeps."""
        try:
            user_row = self._connection.execute(
                """
                SELECT * FROM users WHERE id=%s;
                """, [id]
            )[0]
            peeps = []
            peep_rows = self._connection.execute(
                """
                SELECT * FROM peeps WHERE user_id=%s;
                """, [id]
            )
            for row in peep_rows:
                peeps.append(
                    Peep(row['id'], row['content'],
                        row['timestamp'], row['user_id'])
                )
            return User(user_row['id'], 
                        user_row['username'], 
                        user_row['email'], 
                        user_row['password'], 
                        peeps=peeps)
        except:
            raise ValueError(f"User with ID {id} does not exist")
        
    def find_by_email(self, email):
        """Returns the user with email=email."""
        try:
            row = self._connection.execute(
                """
                SELECT * FROM users WHERE email=%s;
                """, [email]
            )[0]
            return User(row['id'], 
                        row['username'], 
                        row['email'], 
                        row['password'])
        except:
            raise ValueError(f"User with email {email} does not exist")
        
    def find_by_username(self, username):
        """Returns the user with username=username."""
        try:
            row = self._connection.execute(
                """
                SELECT * FROM users WHERE username=%s;
                """, [username]
            )[0]
            return User(row['id'], 
                        row['username'], 
                        row['email'], 
                        row['password'])
        except:
            raise ValueError(f"User with username {username} does not exist")
    
    def create(self, user):
        """Inserts a new user into the users table."""
        self._connection.execute(
            """
            INSERT INTO users (username, email, password) VALUES (%s, %s, %s)
            """, [user.username, user.email, user.password]
        )
        row = self._connection.execute(
            """
            SELECT * FROM users WHERE id=(SELECT MAX(id) FROM users);
            """
        )[0]
        return User(row['id'], 
                    row['username'], 
                    row['email'], 
                    row['password'])

    def delete(self, id):
        """Deletes a user from the users table."""
        self._connection.execute(
            """
            DELETE FROM users WHERE id=%s;
            """, [id]
        )
        return None
    
    def check_password(self, username_or_email, password):
        """Checks whether the given password is a match for
        the user specified by username or email."""
        if '@' in username_or_email:
            try:
                user = self.find_by_email(username_or_email)
                if user.password == \
                    hashlib.sha256(
                        password.encode('utf-8')
                        ).hexdigest():
                    return True
                else:
                    return False
            except:
                pass
        try:
            user = self.find_by_username(username_or_email)
            if user.password == \
                hashlib.sha256(
                    password.encode('utf-8')
                    ).hexdigest():
                return True
            else:
                return False
        except:
            raise ValueError(f"{username_or_email} does not exist")