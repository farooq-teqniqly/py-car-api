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
