import telebot
import userfunds
from requests import request

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
    token_address = "mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ"  # change to mini btc later
    token_result = request('GET',
                           f"https://api.dexscreener.com/latest/dex/pairs/solana/{token_address}",
                           headers=header)
    return float(token_result.json()["pairs"][0]["priceUsd"])


@bot.message_handler(commands=['convert'])
def convert_to_usd(message):
    chat_id = message.chat.id
    price_per_mbtc = get_price()  # need to fetch this
    arguments = message.text.split()
    if len(arguments) > 2:
        bot.send_message(chat_id, f"*Requires an Integer Input*\nPlease Provide a whole number in mSatoshis\\.",
                         parse_mode='MarkdownV2')
        return
    msatoshi_amount = arguments[1]
    if not msatoshi_amount.isnumeric():
        bot.send_message(chat_id, f"*Requires an Integer Input*\nPlease Provide a whole number in mSatoshis\\.",
                         parse_mode='MarkdownV2')
        return
    amount_in_dollars = str(round((float(int(msatoshi_amount)) / float(100000000000)) * price_per_mbtc, 2))
    bot.send_message(chat_id, f"The converted amount is equal to {amount_in_dollars} dollars")


# every admin will hev equal deduction of balance in order to preserve solvency

@bot.message_handler(commands=['checkbalance'])
def check_balance(message):
    chat_id = message.chat.id
    tipper = "@" + message.from_user.username
    if tipper == "@MINI_BTC_CHAD" or "@LongIt345" or "@CryptoSniper000":  # enforce same admin controls across multiple
        tipper = "@CryptoSniper000"
    if funds_database.check_user_exist(tipper):
        funds = funds_database.check_user_balance(tipper)
        mbtc_balance = float(funds) / float(100000000000)
        bot.send_message(chat_id, f"{tipper} ,💰 Your balance is : {mbtc_balance:.11f} mBTC ({funds} mSatoshis)")
        return
    else:
        bot.send_message(chat_id, f"{tipper} ,⚠️ You haven't setup a wallet yet.\nPlease use our simple setup bot "
                                  f"'https://t.me/mBTCTipbot' and follow instructions"
                                  "to begin")
        return


@bot.message_handler(commands=['tip'])
def tipping(message):
    chat_id = message.chat.id
    tipper = "@" + message.from_user.username
    if tipper == "@MINI_BTC_CHAD" or "@LongIt345" or "@CryptoSniper000":  # enforce same admin controls across multiple
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
        if username_to_tip in admins:
            bot.send_message(chat_id, f"*Admins cannot tip themselves*\\.",
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
            bot.send_message(chat_id, "User has not setup their tipping wallet.")
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
    if tipper == "@MINI_BTC_CHAD" or "@LongIt345" or "@CryptoSniper000":  # enforce same admin controls across multiple
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
                        bot.send_message(chat_id, f"{tipper} cannot tip themselves!")
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


@bot.message_handler(commands=['rain'])
def rain(message):
    chat_id = message.chat.id
    tipper = "@" + message.from_user.username
    if tipper == "@MINI_BTC_CHAD" or "@LongIt345" or "@CryptoSniper000":  # enforce same admin controls across multiple
        tipper = "@CryptoSniper000" #sets to master
    arguments = message.text.split()
    random_list_of_users = funds_database.fetch_random_users(tipper)
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
    string_builder = f"{tipper} has mass tipped :"
    for user in random_list_of_users:
        if budget - modulo >= 0:
            username_to_tip_balance = int(funds_database.check_user_balance(user))
            new_username_to_tip_balance = username_to_tip_balance + modulo
            funds_database.update_balance(user, new_username_to_tip_balance)
        else:
            username_to_tip_balance = int(funds_database.check_user_balance(user))
            new_username_to_tip_balance = username_to_tip_balance + remainder
            funds_database.update_balance(user, new_username_to_tip_balance)
        string_builder += f" {user} ,"
    bot.send_message(chat_id, string_builder)


if __name__ == "__main__":
    bot.infinity_polling(timeout=None)
