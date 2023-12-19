from lib.peep import Peep

class PeepRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute(
            """
            SELECT * FROM peeps;
            """
        )
        peeps = []
        for row in rows:
            peeps.append(
                Peep(
                    row['id'], row['content'], 
                    row['timestamp'], row['user_id']
                )
            )
        return peeps

    def find(self, id):
        try:
            row = self._connection.execute(
                """
                SELECT * FROM peeps WHERE id=%s;
                """, [id]
            )[0]
            return Peep(row['id'], row['content'], 
                        row['timestamp'], row['user_id'])
        except:
            raise ValueError(f"Peep with ID {id} does not exist")

    def create(self, peep):
        self._connection.execute(
            """
            INSERT INTO peeps (content, timestamp, user_id)
            VALUES (%s, %s, %s);
            """, [peep.content, peep.timestamp, peep.user_id]
        )
        row = self._connection.execute(
            """
            SELECT * FROM peeps WHERE id=(SELECT MAX(id) FROM peeps);
            """
        )[0]
        return Peep(row['id'], row['content'], 
                    row['timestamp'], row['user_id'])

    def delete(self, id):
        self._connection.execute(
            """
            DELETE FROM peeps WHERE id=%s;
            """, [id]
        )