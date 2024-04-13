import psycopg2, re, os
from configparser import ConfigParser
from getpass import getpass

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

def clear_console():
    """
    Clear the console.
    """
    os.system('clear') if os.name == 'posix' else os.system('cls')

tables_deployment = (
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
    print("Trying to connect to the database...")
    while True:
        try:
            with psycopg2.connect(**config) as conn:
                print(f"Connected as {config['user']} to {config['database']} database\nWaiting for commands...")
                command = input("\n>>>")
                if command == "help" or command == "h":
                    clear_console()
                    print("Commands:\ndeploy\nadd user\nshow users\nshow admins\nexit\n")
                elif command == "drop":
                    clear_console()
                    db_call("DROP TABLE users, admins")
                    print("Tables dropped.")
                elif command == "add administr4t0r":
                    clear_console()
                    print("Add a new admin(ONLY FOR TESTING)")
                    admin_name = input("Enter admin name: ").strip()
                    admin_password = input("Enter admin password: ").strip()
                    if not re.fullmatch(r"^[a-zA-Z0-9\-_!^&*]+$", admin_password): 
                        print("Password must contain only letters, numbers, and symbols: -_!^&*")
                        continue
                    clear_console()
                    db_call("INSERT INTO admins (admin_name, admin_password) VALUES (%s, %s)", (admin_name, admin_password))
                elif command == "deploy":
                    clear_console()
                    for table in tables_deployment:
                        db_call(table)
                elif command == "add user":
                    clear_console()
                    print("Add a new user")
                    user_name = input("Enter user name: ").strip()
                    if db_call(f"SELECT user_name FROM users WHERE user_name = \'{user_name}\'", fetch=True): 
                        print("User already exists.")
                        continue
                    user_password = getpass("Enter user password: ")
                    if not re.fullmatch(r"^[a-zA-Z0-9\-_!^&*]+$", user_password): 
                        print("Password must contain only letters, numbers, and symbols: -_!^&*")
                        continue
                    clear_console()
                    db_call("INSERT INTO users (user_name, user_password) VALUES (%s, %s)", (user_name, user_password))
                elif command == "show users":
                    clear_console()
                    print("Users:")
                    list_of_users = db_call("SELECT user_id, user_name FROM users", fetch=True)
                    print(*list_of_users, sep='\n') if list_of_users else print("No users found.")
                elif command == "show admins":
                    clear_console()
                    print("Login as an admin to show admin list:")
                    admin_name = input("Enter admin name: ").strip()
                    if db_call(f"SELECT admin_name FROM admins WHERE admin_name = \'{admin_name}\'", fetch=True):
                        admin_password = getpass("Enter admin password: ")
                        if db_call(f"SELECT * FROM admins WHERE admin_name = \'{admin_name}\' AND admin_password = \'{admin_password}\'", fetch=True):
                            clear_console()
                            print("Login successful.")
                            print(*db_call("SELECT * FROM admins", fetch=True), sep='\n')
                elif command == "exit":
                    break
                else:
                    clear_console()
                    print("unknown command")
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)