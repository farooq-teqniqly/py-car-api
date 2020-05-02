from typing import Tuple, Generator

import pyodbc


def connect(server: str, db: str, user: str, password: str):
    if not server or not db or not user or not password:
        raise ValueError("Provide the SQL Server name, database, user, and password.")

    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + server
        + ";DATABASE="
        + db
        + ";UID="
        + user
        + ";PWD="
        + password
    )

    return connection


def get_entities(connection, entity: str) -> Generator[Tuple, None, None]:
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM [dbo].[{entity}]")
    return cursor
