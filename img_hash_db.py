import sqlite3


class ImgDb:
    def __init__(self):
        self.connection = sqlite3.connect("imghash.db",
                                          check_same_thread=False)  # check what the check next thread means
        self.cursor9 = self.connection.cursor()
        try:
            self.cursor9.execute("""CREATE TABLE imghashtable(
                imghashdigest TEXT
                )""")
            self.connection.commit()
        except sqlite3.Error:
            print("imghash database is Already created")

    def check_hash_exist(self, img_hash):
        sql = "SELECT * FROM imghashtable WHERE imghashdigest =?"
        self.cursor9.execute(sql, [img_hash])
        user = self.cursor9.fetchone()  # should be only one ofc
        if user is None:
            return False
        else:
            return True

    def add_hash(self, img_hash):  # INITIALISE NEW USER
        sql = "INSERT INTO imghashtable VALUES (?)"
        self.cursor9.execute(sql, (img_hash,))
        self.connection.commit()
