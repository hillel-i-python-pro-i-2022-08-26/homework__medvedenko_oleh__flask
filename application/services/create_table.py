from application.services.db_connection import DBConnection


def create_table():
    with DBConnection() as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS phones(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                contact_name VARCHAR NOT NULL,
                phone_value VARCHAR NOT NULL
                )
                """
            )
