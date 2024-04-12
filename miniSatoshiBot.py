import telebot
import userfunds
from requests import request
import getlppoolinfo
import get_trending_coins
import raidleaderboard

leaderboard = raidleaderboard.ShillStats()
my_token = '7179501342:AAGFiuXaX_ainsSXJN8VfTKfgz36PyObdwA'
bot = telebot.TeleBot(my_token)
funds_database = userfunds.FundsDatabase()

header = {
    "User-Agent": " ".join(
        [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/113.0.0.0 Safari/537.36",
        ]
    )
}
admins = ["@MINI_BTC_CHAD", "@LongIt345", "@CryptoSniper000"]


def get_price():
    token_address = "ddnvc5rvvzejlunkbf6xsdqha6gpkblxyq8z1bzaotuc"  # change to mini btc later
    token_result = request('GET',
                           f"https://api.dexscreener.com/latest/dex/pairs/solana/{token_address}",
                           headers=header)
    return float(token_result.json()["pairs"][0]["priceUsd"])


def get_marketcap():
    token_address = "ddnvc5rvvzejlunkbf6xsdqha6gpkblxyq8z1bzaotuc"  # change to mini btc later
    token_result = request('GET',
                           f"https://api.dexscreener.com/latest/dex/pairs/solana/{token_address}",
                           headers=header)
    return float(token_result.json()["pairs"][0]["fdv"])


def get_trending_tokens():
    token_address = "ddnvc5rvvzejlunkbf6xsdqha6gpkblxyq8z1bzaotuc"  # change to mini btc later
    token_result = request('GET',
                           f"https://api.dexscreener.com/latest/dex/pairs/solana/{token_address}",
                           headers=header)


@bot.message_handler(commands=['leaderboard'])
def leader_board(message):
    chat_id = message.chat.id
    total_earned = leaderboard.get_total_awards()
    task_count = leaderboard.get_total_tasks()
    top_users = leaderboard.get_top_five()
    bot.send_message(chat_id,
                     f"🟣 *__Shill to earn Leaderboard__*\n\n{top_users}\n💰 Total earned: *{total_earned}* mSats\n📚 Total "
                     f"tasks completed: *{task_count}*\n\n👯 [Join rewards group]("
                     f"https://t\\.me/\\+OGXZpC7yGXQ2MDZk)",
                     parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['supplyleft'])
def supplyleft(message):
    chat_id = message.chat.id
    supply = getlppoolinfo.get_lp_info()
    bot.send_message(chat_id, f"Supply left in the Liquidity pool : *{supply}*",
                     parse_mode='MarkdownV2')


@bot.message_handler(commands=['getprice'])
def rain(message):
    chat_id = message.chat.id
    price = str(get_price()).replace(".", ",")
    bot.send_message(chat_id, f"Mini Bitcoin price : *{price}$*",
                     parse_mode='MarkdownV2')


@bot.message_handler(commands=['compare'])  # compare it to trending coins on sol
def rain(message):
    chat_id = message.chat.id
    arguments = message.text.split()
    if len(arguments) < 2:
        bot.send_message(chat_id, f"Please Provide the token you wish to compare",
                         parse_mode='MarkdownV2')
        return
    result = get_trending_coins.compare(arguments[1])
    if result is not False:
        bot.send_message(chat_id, result,
                         parse_mode='MarkdownV2')


@bot.message_handler(commands=['convert'])
def convert_to_usd(message):
    chat_id = message.chat.id
    price_per_mbtc = get_price()  # need to fetch this
    arguments = message.text.split()
    if message.from_user.username is None:  # no username
        if len(arguments) < 2:
            bot.send_message(chat_id, f"*Requires an Integer Input*\nDo: /convert \\<amount in m Satoshis\\>\\.",
                             parse_mode='MarkdownV2')
            return
    else:  # check if they are registered:
        user = "@" + message.from_user.username
        if user == "@MINI_BTC_CHAD" or user == "@LongIt345" or user == "@CryptoSniper000":  # enforce same admin controls across multiple
            user = "@CryptoSniper000"
        if funds_database.check_user_exist(user):
            if len(arguments) < 2:  # clearly they want to check for themselves
                funds = funds_database.check_user_balance(user)
                sats_balance = float(funds)
                amount_in_dollars = ((float(int(sats_balance)) / float(100000000000)) * price_per_mbtc)
                substring = f"{amount_in_dollars:.5f}".replace(".", "\\.")
                user = user.replace("_", "\\_")
                bot.send_message(chat_id, f"Dear {user}, your converted balance is equal to *${substring}*",
                                 parse_mode='MarkdownV2')
                return
    if len(arguments) > 2 or len(arguments) < 2:
        bot.send_message(chat_id, f"*Requires an Integer Input*\nPlease Provide a whole number in mSatoshis\\.",
                         parse_mode='MarkdownV2')
        return
    msatoshi_amount = arguments[1]
    if not msatoshi_amount.isnumeric():
        bot.send_message(chat_id, f"*Requires an Integer Input*\nPlease Provide a whole number in mSatoshis\\.",
                         parse_mode='MarkdownV2')
        return
    amount_in_dollars = ((float(int(msatoshi_amount)) / float(100000000000)) * price_per_mbtc)
    substring = f"{amount_in_dollars:.5f}".replace(".", "\\.")
    bot.send_message(chat_id, f"The converted amount is equal to *${substring}*", parse_mode='MarkdownV2')


# every admin will hev equal deduction of balance in order to preserve solvency

@bot.message_handler(commands=['checkbalance'])
def check_balance(message):
    chat_id = message.chat.id
    if message.from_user.username is None:
        bot.send_message(chat_id,
                         f"User has no username\\!",
                         parse_mode='MarkdownV2')
        return
    tipper = "@" + message.from_user.username
    if tipper == "@MINI_BTC_CHAD" or tipper == "@LongIt345" or tipper == "@CryptoSniper000":  # enforce same admin controls across multiple
        tipper = "@CryptoSniper000"
    if funds_database.check_user_exist(tipper):
        funds = funds_database.check_user_balance(tipper)
        mbtc_balance = float(funds) / float(100000000000)
        bot.send_message(chat_id, f"{tipper} ,💰 Your balance is : {mbtc_balance:.11f} mBTC ({funds} mSatoshis)")
        return
    else:
        bot.send_message(chat_id, f"{tipper} ,⚠️ You haven't setup a wallet yet.\nPlease use our simple setup bot "
                                  f"'https://t.me/mBTCTipbot' and follow instructions "
                                  "to begin")
        return


@bot.message_handler(commands=['totalburn'])
def check_balance(message):
    chat_id = message.chat.id
    burn_wallet = "@MiniBtcBurn"
    funds = funds_database.check_user_balance(burn_wallet)
    mbtc_balance = float(funds) / float(100000000000)
    prestring = f"{mbtc_balance:.11f}".replace(".", "\\.")
    bot.send_message(chat_id, f"Total amount burned by all users: *{prestring}* mBTC \\(*{funds}* mSatoshis\\)",
                     parse_mode='MarkdownV2')
    return


@bot.message_handler(commands=['burnsats'])  # for burning mini satoshis ( sending it to burn account)
def burn(message):
    # only argument is the mount to be burned
    burn_wallet = "@MiniBtcBurn"
    chat_id = message.chat.id
    if message.from_user.username is None:  # no username
        bot.send_message(chat_id, f"*Please Set a username!*.",
                         parse_mode='MarkdownV2')
        return
    tipper = "@" + message.from_user.username
    if tipper == "@MINI_BTC_CHAD" or tipper == "@LongIt345" or tipper == "@CryptoSniper000":  # enforce same admin controls across multiple
        tipper = "@CryptoSniper000"
    if funds_database.check_user_exist(tipper):
        arguments = message.text.split()
        argument_length = len(arguments)
        if argument_length < 2 or argument_length > 2:
            bot.send_message(chat_id, f"*Invalid Input*\nPlease us the following syntax:\n/burnsats "
                                      f"\\<\\amount in"
                                      f" mSatoshis\\>\\ \\.",
                             parse_mode='MarkdownV2')
            return
        username_to_tip = burn_wallet
        if funds_database.check_user_exist(username_to_tip):
            amount_to_tip = arguments[1]
            if not amount_to_tip.isnumeric():
                bot.send_message(chat_id, f"*Requires an Integer Input*\nPlease Provide a whole number in mSatoshis\\.",
                                 parse_mode='MarkdownV2')
                return
            else:
                if int(funds_database.check_user_balance(tipper)) >= int(amount_to_tip):
                    new_tipper_balance = int(funds_database.check_user_balance(tipper)) - int(amount_to_tip)
                    username_to_tip_balance = int(funds_database.check_user_balance(username_to_tip))
                    new_username_to_tip_balance = username_to_tip_balance + int(amount_to_tip)
                    funds_database.update_balance(tipper, new_tipper_balance)
                    funds_database.update_balance(username_to_tip, new_username_to_tip_balance)
                    bot.send_message(chat_id, f"{tipper} has Burned *{amount_to_tip}* mSatoshis",
                                     parse_mode='MarkdownV2')
                else:  # not enough funds
                    bot.send_message(chat_id,
                                     f"*Insufficient funds*\nThe amount burned is greater than your balance\\.",
                                     parse_mode='MarkdownV2')
                    return
        else:
            bot.send_message(chat_id,
                             "User has not setup their tipping wallet.\nUse the bot : https://t.me/mBTCTipbot ")
            return
    else:
        bot.send_message(chat_id, "Please first Dm the : 'https://t.me/mBTCTipbot' bot to setup a wallet.\nYou will "
                                  "need to be tipped by a team member before you can send mBTC to other users in the "
                                  "group")
        return


@bot.message_handler(commands=['tip'])
def tipping(message):
    chat_id = message.chat.id
    tipper = "@" + message.from_user.username
    if tipper == "@MINI_BTC_CHAD" or tipper == "@LongIt345" or tipper == "@CryptoSniper000":  # enforce same admin controls across multiple
        tipper = "@CryptoSniper000"
    if funds_database.check_user_exist(tipper):
        arguments = message.text.split()
        argument_length = len(arguments)
        if argument_length < 3 or argument_length > 3:
            bot.send_message(chat_id, f"*Invalid Input*\nPlease us the following syntax:\n/tip \\<@\\username\\>\\ "
                                      f"\\<\\amount in"
                                      f" mSatoshis\\>\\ \\.",
                             parse_mode='MarkdownV2')
            return
        username_to_tip = arguments[1]
        if username_to_tip == tipper:
            bot.send_message(chat_id, f"*You cannot tip yourself*\\.",
                             parse_mode='MarkdownV2')
            return
        if username_to_tip in admins:
            bot.send_message(chat_id, f"*Admins cannot be tipped*\\.",
                             parse_mode='MarkdownV2')
            return
        if funds_database.check_user_exist(username_to_tip):
            amount_to_tip = arguments[2]
            if not amount_to_tip.isnumeric():
                bot.send_message(chat_id, f"*Requires an Integer Input*\nPlease Provide a whole number in mSatoshis\\.",
                                 parse_mode='MarkdownV2')
                return
            else:
                if int(funds_database.check_user_balance(tipper)) > int(amount_to_tip):
                    new_tipper_balance = int(funds_database.check_user_balance(tipper)) - int(amount_to_tip)
                    username_to_tip_balance = int(funds_database.check_user_balance(username_to_tip))
                    new_username_to_tip_balance = username_to_tip_balance + int(amount_to_tip)
                    funds_database.update_balance(tipper, new_tipper_balance)
                    funds_database.update_balance(username_to_tip, new_username_to_tip_balance)
                    bot.send_message(chat_id, f"{tipper} has tipped {amount_to_tip} mSatoshis to {username_to_tip}")
                else:  # not enough funds
                    bot.send_message(chat_id,
                                     f"*Insufficient funds*\nThe amount tipped is greater than your balance\\.",
                                     parse_mode='MarkdownV2')
                    return
        else:
            bot.send_message(chat_id,
                             "User has not setup their tipping wallet.\nUse the bot : https://t.me/mBTCTipbot ")
            return
    else:
        bot.send_message(chat_id, "Please first Dm the : 'https://t.me/mBTCTipbot' bot to setup a wallet.\nYou will "
                                  "need to be tipped by a team member before you can send mBTC to other users in the "
                                  "group")
        return


@bot.message_handler(commands=['tipmany'])
def rain(message):
    chat_id = message.chat.id
    tipper = "@" + message.from_user.username
    if tipper == "@MINI_BTC_CHAD" or tipper == "@LongIt345" or tipper == "@CryptoSniper000":  # enforce same admin controls across multiple
        tipper = "@CryptoSniper000"
    if funds_database.check_user_exist(tipper):
        arguments = message.text.split()
        argument_length = len(arguments)
        if argument_length < 3:
            bot.send_message(chat_id,
                             f"*Invalid Input*\nPlease us the following syntax:\n/tip \\<@\\username1\\>\\ "
                             f"\\<@\\username2\\>\\ ... \\<@\\username\\>\\"
                             f"\\<\\amount in"
                             f" mSatoshis\\>\\ \\.",
                             parse_mode='MarkdownV2')
        else:
            # make an initial pass to check if the syntax is sound
            for index in range(1, len(arguments) - 1):
                if not funds_database.check_user_exist(arguments[index]):
                    bot.send_message(chat_id, f"The Username: {index} is not registered.")
                    return
                else:
                    if arguments[index] == tipper:
                        bot.send_message(chat_id, f"{tipper},You cannot tip yourself!")
                        return
            if not arguments[len(arguments) - 1].isnumeric():
                bot.send_message(chat_id, f"*Requires an Integer Input*\nPlease Provide a whole number in mSatoshis\\.",
                                 parse_mode='MarkdownV2')
                return
            amount_to_tip = int(arguments[len(arguments) - 1])
            if int(funds_database.check_user_balance(tipper)) > int(amount_to_tip) * (len(arguments) - 2):
                for index in range(1, len(arguments) - 1):
                    new_tipper_balance = int(funds_database.check_user_balance(tipper)) - int(amount_to_tip)
                    username_to_tip_balance = int(funds_database.check_user_balance(arguments[index]))
                    new_username_to_tip_balance = username_to_tip_balance + int(amount_to_tip)
                    funds_database.update_balance(tipper, new_tipper_balance)
                    funds_database.update_balance(arguments[index], new_username_to_tip_balance)
                bot.send_message(chat_id, f"{tipper} has tipped {amount_to_tip} mSatoshis each to each selected user.")
            else:  # not enough funds
                bot.send_message(chat_id,
                                 f"*Insufficient funds*\nThe cumulative amount tipped is greater than your balance\\.",
                                 parse_mode='MarkdownV2')
                return
    else:
        bot.send_message(chat_id, "Please first Dm the : 'https://t.me/mBTCTipbot' bot to setup a wallet.\nYou will "
                                  "need to be tipped by a team member before you can send mBTC to other users in the "
                                  "group")
        return


@bot.message_handler(commands=['rain'])  # check why it leaves a comma at the end
def rain(message):
    chat_id = message.chat.id
    if message.from_user.username is None:
        bot.send_message(chat_id,
                         f"User has no username\\!",
                         parse_mode='MarkdownV2')
        return
    tipper = "@" + message.from_user.username
    if tipper == "@MINI_BTC_CHAD" or tipper == "@LongIt345" or tipper == "@CryptoSniper000":  # enforce same admin controls across multiple
        tipper = "@CryptoSniper000"  # sets to master
    arguments = message.text.split()
    random_list_of_users = funds_database.fetch_random_users(tipper)
    if len(arguments) < 2:
        bot.send_message(chat_id, f"*Requires a username and a Integer Input*\nPlease Provide a whole number in "
                                  f"mSatoshis\\.",
                         parse_mode='MarkdownV2')
        return
    if not arguments[1].isnumeric():
        bot.send_message(chat_id, f"*Requires an Integer Input*\nPlease Provide a whole number in mSatoshis\\.",
                         parse_mode='MarkdownV2')
        return
    budget = int(arguments[1])
    if budget > funds_database.check_user_balance(tipper):
        bot.send_message(chat_id,
                         f"*Insufficient funds*\nThe cumulative amount tipped is greater than your balance\\.",
                         parse_mode='MarkdownV2')
        return
    modulo = budget // len(random_list_of_users)
    new_tipper_balance = int(funds_database.check_user_balance(tipper)) - int(budget)  # update tipper balance
    funds_database.update_balance(tipper, new_tipper_balance)
    remainder = budget - modulo * len(random_list_of_users)
    string_builder = f"{tipper} has mass tipped: "
    for user in random_list_of_users:
        if budget - modulo > 0 and modulo != 0:
            username_to_tip_balance = int(funds_database.check_user_balance(user))
            new_username_to_tip_balance = username_to_tip_balance + modulo
            funds_database.update_balance(user, new_username_to_tip_balance)
            budget -= modulo
        else:
            username_to_tip_balance = int(funds_database.check_user_balance(user))
            new_username_to_tip_balance = username_to_tip_balance + remainder
            funds_database.update_balance(user, new_username_to_tip_balance)
            string_builder += f" {user} "
            break
        string_builder += f" {user} ,"
    bot.send_message(chat_id, string_builder)


if __name__ == "__main__":
    bot.infinity_polling(timeout=None)
