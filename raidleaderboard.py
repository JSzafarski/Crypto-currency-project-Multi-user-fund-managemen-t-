import sqlite3


class ShillStats:
    def __init__(self):
        self.connection = sqlite3.connect("userstats.db",
                                          check_same_thread=False)  # check what the check next thread means
        self.cursor0 = self.connection.cursor()
        try:
            self.cursor0.execute("""CREATE TABLE userstats(
                username INTEGER,
                totalearned INTEGER,
                totalcompleted INTEGER
                )""")
            self.connection.commit()
        except sqlite3.Error:
            print("userstats database is Already created")

    def fetch_total_completed(self, telegram_username):
        sql = "SELECT * FROM userstats WHERE username =?"
        self.cursor0.execute(sql, [telegram_username])
        user_settings = self.cursor0.fetchone()
        return user_settings[2]

    def fetch_total_earned(self, telegram_username):
        sql = "SELECT * FROM userstats WHERE username =?"
        self.cursor0.execute(sql, [telegram_username])
        user_settings = self.cursor0.fetchone()
        return user_settings[1]

    def check_user_exist(self, telegram_username):
        sql = "SELECT * FROM userstats WHERE username =?"
        self.cursor0.execute(sql, [telegram_username])
        user = self.cursor0.fetchone()  # should be only one ofc
        if user is None:
            return False
        else:
            return True

    def add_user(self, telegram_username):  # INITIALISE NEW USER
        sql = "INSERT INTO userstats VALUES (?,?,?)"
        self.cursor0.execute(sql, (telegram_username, 0, 0))  # ie empty string
        self.connection.commit()

    def increment_task_count(self, telegram_username):
        sql = "UPDATE userstats SET totalcompleted =? WHERE username=?"
        current_amount = int(self.fetch_total_completed(telegram_username))
        incremented_amount = current_amount + 1
        self.cursor0.execute(sql, [incremented_amount, telegram_username])
        self.connection.commit()

    def add_to_total_earnings(self, telegram_username, earning_to_add):
        sql = "UPDATE userstats SET totalearned =? WHERE username=?"
        current_amount_earned = int(self.fetch_total_earned(telegram_username))
        incremented_amount_earned = current_amount_earned + earning_to_add
        self.cursor0.execute(sql, [incremented_amount_earned, telegram_username])
        self.connection.commit()

    def get_total_awards(self):
        self.cursor0.execute("SELECT * FROM userstats")
        rows = self.cursor0.fetchall()
        total = 0
        for user in rows:
            total += int(user[1])
        return total

    def get_total_tasks(self):
        self.cursor0.execute("SELECT * FROM userstats")
        rows = self.cursor0.fetchall()
        total = 0
        for user in rows:
            total += int(user[2])
        return total
