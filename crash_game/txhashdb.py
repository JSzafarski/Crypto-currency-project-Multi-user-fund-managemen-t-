#storing all hashes here so we know
import sqlite3


class TxHash:
    def __init__(self):
        self.connection = sqlite3.connect("tx_hash.db",
                                          check_same_thread=False)  # check what the check next thread means
        self.cursor0 = self.connection.cursor()
        try:
            self.cursor0.execute("""CREATE TABLE txhash(
                imghashdigest TEXT
                )""")
            self.connection.commit()
        except sqlite3.Error:
            print("imghash database is Already created")

    def check_hash_exist(self, img_hash):
        sql = "SELECT * FROM txhash WHERE imghashdigest =?"
        self.cursor0.execute(sql, [img_hash])
        user = self.cursor0.fetchone()  # should be only one ofc
        if user is None:
            return False
        else:
            return True

    def add_hash(self, img_hash):  # INITIALISE NEW USER
        sql = "INSERT INTO txhash VALUES (?)"
        self.cursor0.execute(sql, (img_hash,))
        self.connection.commit()
