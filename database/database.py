from typing import Optional


class Database:
    def __init__(self, connection: Optional[str] = None) -> None:
        """Create a connection to a database."""
        self.connected: bool = True
        pass


db: Optional[Database] = None


def initialize_database(connection: Optional[str] = None) -> Database:
    print('Initializing database...')
    global db
    db = Database(connection)
    return db


def get_database() -> Database:
    global db
    if db is None:
        db = initialize_database()
    return db
