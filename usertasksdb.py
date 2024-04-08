import sqlite3


class UserRewardDb:
    def __init__(self):
        self.connection = sqlite3.connect("user_tasks.db",
                                          check_same_thread=False)  # check what the check next thread means
        self.cursor2 = self.connection.cursor()
        try:
            self.cursor2.execute("""CREATE TABLE usertasks(
                username INTEGER,
                completedtasks TEXT
                )""")
            self.connection.commit()
        except sqlite3.Error:
            print("USERTASKS database is Already created")

    def check_user_exist(self, telegram_username):
        sql = "SELECT * FROM usertasks WHERE username =?"
        self.cursor2.execute(sql, [telegram_username])
        user = self.cursor2.fetchone()  # should be only one ofc
        if user is None:
            return False
        else:
            return True

    def add_user(self, telegram_username):  # INITIALISE NEW USER
        sql = "INSERT INTO usertasks VALUES (?,?)"
        self.cursor2.execute(sql, (telegram_username, ""))  # ie empty string
        self.connection.commit()

    def update_completed_tasks(self, telegram_username, tasks):
        sql = "UPDATE usertasks SET completedtasks =? WHERE username=?"
        self.cursor2.execute(sql, [tasks, telegram_username])
        self.connection.commit()

    def get_user_tesks(self, telegram_username):
        sql = "SELECT * FROM usertasks WHERE username =?"
        self.cursor2.execute(sql, [telegram_username])
        user_settings = self.cursor2.fetchone()
        return user_settings[1]
