import sqlite3


#for storing hashes in the database so we know the next game hash as well as the previous game hashes
#needs a class data strucutre to store the hash

class GameHashDb:
    def __init__(self):
        self.connection = sqlite3.connect("gamehash.db",
                                          check_same_thread=False)  # check what the check next thread means
        self.cursor9 = self.connection.cursor()
        try:
            self.cursor9.execute("""CREATE TABLE gamehashtable(
                hashdigest TEXT
                )""")
            self.connection.commit()
        except sqlite3.Error:
            print("gamehash database is Already created")

    def get_latest_hash(self):
        sql = "SELECT * FROM gamehashtable"
        self.cursor9.execute(sql)
        hashes = self.cursor9.fetchall()  # should be only one ofc
        if len(hashes) == 0:
            return ""
        else:
            last_index = len(hashes) - 1
            return hashes[last_index][0]

    def add_hash(self, game_hash):  # INITIALISE NEW USER
        sql = "INSERT INTO gamehashtable VALUES (?)"
        self.cursor9.execute(sql, (game_hash,))
        self.connection.commit()
