import psycopg2
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    """
    Load configuration from file.

    Args:
        filename (str, optional): file path. Defaults to 'database.ini'.
        section (str, optional): name of section. Defaults to 'postgresql'.

    Returns:
        dict: host: str, database: str, user: str, password: str
    """
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return config

def db_call(query, data=None, fetch=False):
    """
    Make a call to the database.

    Args:
    query (str): SQL query.
    data (tuple, optional): Data for the query, by default None.
    fetch (bool, optional): Return the result of the query, by default False.

    Returns:
    list | None: Result/None(fetch=False).
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, data)
            if fetch:
                return cur.fetchall()
            conn.commit()
            print("Query executed successfully.")
    except Exception as error:
        print(f"Error: {error}")
        return None

create_comands = (
    """
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        user_name VARCHAR(50) UNIQUE NOT NULL,
        user_password VARCHAR(50) NOT NULL
    )
    """,
    """
    CREATE TABLE admins (
        admin_id SERIAL PRIMARY KEY,
        admin_name VARCHAR(50) UNIQUE NOT NULL,
        admin_password VARCHAR(50) NOT NULL
    )
    """
)

if __name__ == "__main__":
    config = load_config()
    print(f"Connected as {config['user']} to {config['database']} database")
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            # with conn.cursor() as cur:
            #     for command in create_comands:
            #         cur.execute(command)
            #         print("table added")
            #! db_call(command for command in create_comands)
            # with conn.cursor() as cur:
            #     user_name = input("Enter user name: ")
            #     user_password = input("Enter password: ")
            #     cur.execute("INSERT INTO users (user_name, user_pasword) VALUES (%s, %s)",
            #         (user_name, user_password))
            #     conn.commit()
            #     print("User added successfully.")
            db_call("INSERT INTO users (user_name, user_password) VALUES (%s, %s)", ("test_user_n", "123456"))
            # with conn.cursor() as cur:
            #     cur.execute("SELECT * FROM users")
            #     records = cur.fetchall()
            #     for record in records:
            #         print(record)
            print(*db_call("SELECT * FROM users", fetch=True), sep='\n')
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)