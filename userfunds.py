# database to manage user tips in a safe simple manner
import random
import sqlite3

admins = ["@MINI_BTC_CHAD", "@LongIt345", "@CryptoSniper000"]


class FundsDatabase:
    def __init__(self):
        self.connection = sqlite3.connect("user_funds.db",
                                          check_same_thread=False)  # check what the check next thread means
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("""CREATE TABLE userfunds(
                username INTEGER,
                balance INTEGER,
                wallet TEXT
                )""")
            self.connection.commit()
        except sqlite3.Error:
            print("user_funds database is Already created")

    def check_user_exist(self, telegram_username):
        sql = "SELECT * FROM userfunds WHERE username =?"
        self.cursor.execute(sql, [telegram_username])
        user = self.cursor.fetchone()  # should be only one ofc
        if user is None:
            return False
        else:
            return True

    def add_user(self, telegram_username, wallet):  # INITIALISE NEW USER
        sql = "INSERT INTO userfunds VALUES (?,?,?)"
        self.cursor.execute(sql, (telegram_username, 0, wallet))
        self.connection.commit()

    def check_user_balance(self, telegram_username):
        sql = "SELECT * FROM userfunds WHERE username =?"
        self.cursor.execute(sql, [telegram_username])
        user_settings = self.cursor.fetchone()
        return user_settings[1]

    def get_user_wallet(self, telegram_username):
        sql = "SELECT * FROM userfunds WHERE username =?"
        self.cursor.execute(sql, [telegram_username])
        user_settings = self.cursor.fetchone()
        return user_settings[2]

    def update_balance(self, telegram_username, new_balance):
        sql = "UPDATE userfunds SET balance =? WHERE username=?"
        self.cursor.execute(sql, [new_balance, telegram_username])
        self.connection.commit()

    def update_wallet(self, telegram_username, new_wallet):
        sql = "UPDATE userfunds SET wallet =? WHERE username=?"
        self.cursor.execute(sql, [new_wallet, telegram_username])
        self.connection.commit()

    def fetch_random_users(self, tipper):
        self.cursor.execute("SELECT * FROM userfunds")
        rows = self.cursor.fetchall()
        range_of_users = len(rows)
        amount_of_members = random.randint(1, range_of_users)
        temp_user_list = []
        for x in range(1, amount_of_members + 1):
            while True:
                selected_user = rows[random.randint(0, range_of_users - 1)][0]
                if str(selected_user) == tipper and len(temp_user_list) == range_of_users - 1:
                    break
                if selected_user not in temp_user_list and selected_user not in admins:
                    temp_user_list.append(selected_user)
                    break
        return temp_user_list
