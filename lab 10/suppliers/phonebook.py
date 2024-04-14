import psycopg2, re, os
from configparser import ConfigParser

def load_config(filename='test.ini', section='postgresql'):
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


def phone_correctiring(phone:str):
    """
    Check the phone number for correctness.

    Args:
        phone (str): phone number.

    Returns:
        str: phone number in correct form.
    """
    # 8 707 123 45 67
    # 87071234567
    # +7  707  123  45  67
    # +77071234567
    # 77071234567
    #! -87071234567
    #! #87071234567
    if phone.startswith('+7'):
        phone = "+7" + re.sub(r'\D', '', phone[2:]) # change any non int to nothing exept + symbol
    elif phone.startswith('8'):
        phone = "+7" + re.sub(r'\D', '', phone)[1:]
    else:
        print("Phone number must start with +7 or 8")
        return None
    return phone[:12]

def db_call_add_user():
    print("Add a new user")
    user_name = input("Enter user name: ").strip()
    if db_call(f"SELECT user_name FROM main WHERE user_name = \'{user_name}\'", fetch=True): 
        print("User already exists.")
        return
    user_phone = phone_correctiring(input("Enter user phone:").strip())
    if user_phone: db_call("INSERT INTO main (user_name, user_phone) VALUES (%s, %s)", (user_name, user_phone))
    else: return

def db_call_show_users():
    call = db_call("SELECT * FROM main ORDER BY user_id ASC", fetch=True)
    if call:
        print("Users list: \n")
        print(*call, sep='\n')
    else: 
        print("Users list is empty")

def db_call_change_user():
    print("Whrite user name to change")
    change_param = input("Enter user name: ").strip()
    call = db_call(f"SELECT user_name, user_phone FROM main WHERE user_name = \'{change_param}\'", fetch=True)
    if call:
        print("Found these users:")
        print(*call, sep='\n')
        user_id = int(input("\nChoose user to change: \n"))
        changing_param = input("What you want to change? name or phone: \n")
        if changing_param == "name":
            new_name = input("Enter new name: ")
            db_call(f"UPDATE main SET user_name = \'{new_name}\' WHERE user_name = \'{call[user_id-1][1]}\'")
        elif changing_param == "phone":
            new_phone = phone_correctiring(input("Enter new phone: "))
            if new_phone: db_call(f"UPDATE main SET user_phone = \'{new_phone}\' WHERE user_phone = \'{call[user_id-1][2]}\'")
        else:
            print("Unknown command")
    else:
        print("No users found.")
        return

if __name__ == "__main__":
    config = load_config(filename="phonebook.ini", section="postgresql")
    print("Connecting to the PostgreSQL database...")
    while True: # main loop
        try:
            with psycopg2.connect(**config) as conn:
                print(f"Connected as {config['user']} to {config['database']} database\nWaiting for commands...")
                command = input("\n>>>")
                if command == "help" or command == "-h":
                    clear_console()
                    print("CMD phonebook by mihailaexx\n\nCommands:\nadd user\nshow users\nexit\n")
                elif command == "add user":
                    clear_console()
                    db_call_add_user()
                elif command == "show users":
                    clear_console()
                    db_call_show_users()
                elif command == "edit user":
                    clear_console()
                    db_call_change_user()
                elif command == "exit":
                    break
                else:
                    clear_console()
                    print("unknown command")
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)