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

    def get_top_five(self):
        position_dict = {
            1: "🥇",
            2: "🥈",
            3: "🥉",
            4: "4️⃣",
            5: "5️⃣",
            6: "6️⃣",
            7: "7️⃣",
            8: "8️⃣",
            9: "9️⃣",
            10: "🔟",
        }
        self.cursor0.execute("SELECT * FROM userstats")
        rows = self.cursor0.fetchall()
        if len(rows) < 10:
            user_range = len(rows) - 1
        else:
            user_range = 10
        users_in_leaderboard = []
        string_builder = ""
        place = 1
        for x in range(0, user_range):
            current_highest = 0  # the highest score
            current_best_user = ""
            for user in rows:
                score = user[1]
                if score > current_highest and user[0] not in users_in_leaderboard:
                    current_highest = score
                    current_best_user = user[0]
            users_in_leaderboard.append(current_best_user)
            current_best_user = current_best_user.replace("@", "")
            current_best_user = current_best_user.replace("_", "\\_")
            current_best_user = current_best_user.replace(".", "\\.")
            string_builder += f"{position_dict[place]} *{current_best_user}*: _{current_highest}_\n"
            if place == 3:
                string_builder += "\n"
            place += 1
        return string_builder

    def get_position(self, telegram_username):
        self.cursor0.execute("SELECT * FROM userstats")
        rows = self.cursor0.fetchall()
        user_range = len(rows) - 1
        users_in_leaderboard = []
        for x in range(0, user_range):
            current_highest = 0  # the highest score
            current_best_user = ""
            for user in rows:
                score = user[1]
                if score > current_highest and user[0] not in users_in_leaderboard:
                    current_highest = score
                    current_best_user = user[0]
            users_in_leaderboard.append(current_best_user)
        for index, ordered_users in enumerate(users_in_leaderboard):
            if ordered_users == telegram_username:
                return index + 1

    def get_first_place(self):
        self.cursor0.execute("SELECT * FROM userstats")
        rows = self.cursor0.fetchall()
        current_highest = 0
        current_best_user = ""
        for user in rows:
            score = user[1]
            if score > current_highest and user[0]:
                current_highest = score
                current_best_user = user[0]
        return current_best_user

    def get_total_users(self):  # exclude banned users later
        self.cursor0.execute("SELECT * FROM userstats")
        rows = self.cursor0.fetchall()
        return len(rows)

    # managing the reset of shiller stats (reset the number of tasks completed and also the amount earned)
    def reset_users(self):
        self.cursor0.execute("SELECT * FROM userstats")
        rows = self.cursor0.fetchall()
        for user in rows:
            user_name = user[0]
            ##reset score##
            sql = "UPDATE userstats SET totalearned =? WHERE username=?"
            self.cursor0.execute(sql, [0, user_name])
            self.connection.commit()
            ##reset tasks completed##
            sql = "UPDATE userstats SET totalcompleted =? WHERE username=?"
            self.cursor0.execute(sql, [0, user_name])
            self.connection.commit()
