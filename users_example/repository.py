from psycopg2.extras import DictCursor
import psycopg2

class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM users")
            return [dict(row) for row in cur]

    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_by_term(self, search_term=""):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                """
                    SELECT * FROM users
                    WHERE email ILIKE %s OR name ILIKE %s
                """,
                (f"%{search_term}%", f"%{search_term}%"),
            )
            return [dict(row) for row in cur]

    def _update(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET email = %s WHERE id = %s",
                (user["email"], user["id"]),
            )
        self.conn.commit()

    def _create(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (email, name) VALUES (%s, %s) RETURNING id",
                (user["email"], user["name"]),
            )
            id = cur.fetchone()[0]
            user["id"] = id
        self.conn.commit()

    def _delete(self, id):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM users WHERE id = %s",
                (id,)
            )
        self.conn.commit()