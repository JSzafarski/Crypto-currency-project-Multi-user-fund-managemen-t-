import sqlite3


class VirtualBalance:
    def __init__(self):
        self.connection = sqlite3.connect("virtual_balance.db",
                                          check_same_thread=False)  # check what the check next thread means
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("""CREATE TABLE virtualbalancetable(
                username TEXT,
                virbalance TEXT,
                walletaddress TEXT,
                privatekey TEXT,
                betsize TEXT,
                walletbalance TEXT
                )""")
            # virtual balance has to be a reflection of real assets
            self.connection.commit()
        except sqlite3.Error:
            print("virtualbalancetable is Already created")

    def check_user_exist(self, telegram_username):
        sql = "SELECT * FROM virtualbalancetable WHERE username =?"
        self.cursor.execute(sql, [telegram_username])
        user = self.cursor.fetchone()  # should be only one ofc
        if user is None:
            return False
        else:
            return True

    def return_all_users(self): #used for updating the virtual balance
        sql = "SELECT * FROM virtualbalancetable"
        self.cursor.execute(sql)
        users = self.cursor.fetchall()  # should be only one ofc
        return users

    def add_user(self, telegram_username, wallet, private_key):  # INITIALISE NEW USER
        sql = "INSERT INTO virtualbalancetable VALUES (?,?,?,?,?)"
        self.cursor.execute(sql, (telegram_username, 0, wallet, private_key, "0.1"))
        self.connection.commit()

    def check_user_balance(self, telegram_username):
        sql = "SELECT * FROM virtualbalancetable WHERE username =?"
        self.cursor.execute(sql, [telegram_username])
        user_settings = self.cursor.fetchone()
        return user_settings[1]

    def check_user_betsize(self, telegram_username):
        sql = "SELECT * FROM virtualbalancetable WHERE username =?"
        self.cursor.execute(sql, [telegram_username])
        user_settings = self.cursor.fetchone()
        return user_settings[4]

    def get_user_wallet(self, telegram_username):
        sql = "SELECT * FROM virtualbalancetable WHERE username =?"
        self.cursor.execute(sql, [telegram_username])
        user_settings = self.cursor.fetchone()
        return user_settings[2]

    def get_user_keys(self, telegram_username):
        sql = "SELECT * FROM virtualbalancetable WHERE username =?"
        self.cursor.execute(sql, [telegram_username])
        user_settings = self.cursor.fetchone()
        return user_settings[3]

    def update_balance(self, telegram_username, new_virtual_balance):
        sql = "UPDATE virtualbalancetable SET virbalance =? WHERE username=?"
        self.cursor.execute(sql, [new_virtual_balance, telegram_username])
        self.connection.commit()

    def update_bet_size(self, telegram_username, new_bet_size):
        sql = "UPDATE virtualbalancetable SET betsize =? WHERE username=?"
        self.cursor.execute(sql, [new_bet_size, telegram_username])
        self.connection.commit()
