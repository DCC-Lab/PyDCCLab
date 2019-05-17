class User:
    def __init__(self, id, username, password, type, time):
        self.id = id
        self.username = username
        self.password = password
        self.type = type
        self.time = time

    def GetUsername(self):
        return self.username


    def GetType(self):
        return self.type


def ConnectToDatabase(path, username, password):
    if ConnectUser(username, password):
        try:
            return sqlite3.connect(path)
        except (ZeroDivisionError, ValueError):
            return
    else:
        return 0


def ConnectUser(username, password):
    con = sqlite3.connect("credentials.db")
    userData = GetUserData(con, username, password)

    if verifications == 'User found!':
        con.close()
        return True
    else:
        con.close()
        return False


def GetUserData(connection, username, password):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
    try:
        profil = cursor.fetchall()[0]
        return profil
    except IndexError as error:
        print('User not found in database.')
        print(error)
    finally:
        print('User found in database.')


def CreateUserInstance(userEntry):
    userEntry = str(userEntry).lstrip('(')
    userEntry = userEntry.rstrip(')')
    userEntry = userEntry.replace('\'', '')
    userEntry = userEntry.replace(' ', '')
    userEntry = userEntry.split(',')
    userProfil = user.User(userEntry[0], userEntry[1], userEntry[2], userEntry[3], userEntry[4])
    return userProfil