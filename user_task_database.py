import telebot
import userfunds
from requests import request
import getlppoolinfo
import get_trending_coins
import usertasksdb
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

my_token = '6896610984:AAHOE6ft3wbyXMuAC1FBssFJ4RA5FEWMC-w'
bot = telebot.TeleBot(my_token)
user_funds = userfunds.FundsDatabase()
user_tasks = usertasksdb.UserRewardDb()
allowable_submissions = {
    "dextools": 100000000,
    "dexscreener": 50000000,
    "birdeye": 25000000,
    "gemsradar": 500000000,
    "coinalpha": 5000000,
    "coincatapult": 5000000,
    "coinmoonhunt": 5000000,
    "coindiscovery": 5000000,
    "coinbazooka": 500000,
    "coinscope": 250000,
    "coinsniper": 250000,
    "ntm.ai": 500000,
    "top100token": 250000,
    "rugfreecoins": 150000,
    "coinboom": 30000,
    "coinmooner": 30000,
    "coinhunt": 200000,
    "cntoken.io": 150000,
    "coinvote": 30000
}

infinity = 999999999999999999999999
twenty_four_hours = 60 * 60 * 24
six_hours = 60 * 60 * 6
one_hour = 60 * 60
thirty_minutes = 60 * 30
time_outs = {  # ( in epoch time)
    "dextools": infinity,
    "dexscreener": infinity,
    "birdeye": infinity,
    "gemsradar": twenty_four_hours,
    "coinalpha": twenty_four_hours,
    "coincatapult": six_hours,
    "coinmoonhunt": one_hour,
    "coindiscovery": one_hour,
    "coinbazooka": twenty_four_hours,
    "coinscope": twenty_four_hours,
    "coinsniper": twenty_four_hours,
    "ntm.ai": one_hour,
    "top100token": twenty_four_hours,
    "rugfreecoins": twenty_four_hours,
    "coinboom": twenty_four_hours,
    "coinmooner": twenty_four_hours,
    "coinhunt": twenty_four_hours,
    "cntoken.io": thirty_minutes,
    "coinvote": twenty_four_hours
}
choices = ['dextools', 'dexscreener', 'birdeye', 'gemsradar', 'coinalpha', 'coincatapult', 'coinmoonhunt',
           'coindiscovery',
           'coinbazooka', 'coinscope', 'ntm.ai', 'top100token', 'rugfreecoins', 'coinboom', 'coinmooner', 'coinhunt',
           "CNToken.io", "Coinvote"]


@bot.message_handler(commands=['info'])
def rain(message):
    chat_id = message.chat.id
    if chat_id != -4174401511:  # not allow as make it only work for that group only
        bot.send_message(chat_id,
                         f"This bot only works in : https://t\\.me/\\+OGXZpC7yGXQ2MDZk \\!",
                         parse_mode='MarkdownV2')
        return
    bot.send_message(chat_id,
                     f"\n\n[DexTools]("
                     f"https://www.dextools.io/app/en/solana/pair-explorer"
                     f"/DDnvC5rvvZeJLuNKBF6xsdqHA6GPKbLxYq8z1bzaotUC?t=1712460479955) hit the 👍🏻"
                     f"*\\(5000000 mSatoshis\\)\n\n*[DexScreener]("
                     f"https://dexscreener.com/solana/ddnvc5rvvzejlunkbf6xsdqha6gpkblxyq8z1bzaotuc) hit the 🚀 "
                     f"*\\(2500000 mSatoshis\\)*\n\n[Birdeye]("
                     f"https://birdeye.so/token/mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ?chain=solana) hit"
                     f" the 👍🏻 *\\(1000000 mSatoshis\\)*\n\n*Reach X "
                     f"votes and get listed:*\n\n[GemsRadar](https://gemsradar.com/coins/mini-bitcoin) login and "
                     f"vote 🗳 *\\(10000000 mSatoshis\\)*\n\n[CoinAlpha]("
                     f"https://coinalpha.app/token/mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ) login and vote 🗳 "
                     f"*\\(1000000 mSatoshis\\)*\n\n[CoinCatapult](https://coincatapult.com/coin/mini-bitcoin-mbtc) "
                     f"vote 🗳 *\\(1000000 mSatoshis\\)*\n\n[CoinMoonHunt]("
                     f"https://coinmoonhunt.com/coin/Mini%20Bitcoin) vote 🗳 *\\(1000000 mSatoshis\\)*\n\n["
                     f"CNToken\\.io](https://cncrypto.io/coin/mini-bitcoin)vote 🗳 *\\(150000 mSatoshis\\)*",
                     parse_mode='MarkdownV2', disable_web_page_preview=True)


def convert_to_standard(input_string):
    lower_case_string = input_string.lower()
    lower_case_string = lower_case_string.strip()  # remove any spaces
    return lower_case_string


# each entry will be (keyword epoch keyword epoch ....so forth

@bot.message_handler(func=lambda message: True,
                     content_types=['photo', 'text'])  # any message ( needs to check if user attaches a picture too)
def check_submission(message):
    user_name = "@" + message.from_user.username
    chat_id = message.chat.id
    if user_name == "@MINI_BTC_CHAD" or user_name == "@LongIt345" or user_name == "@CryptoSniper000":  # ignore admin
        return
    if chat_id != -4174401511:  # not allow as make it only work for that group only
        bot.send_message(chat_id,
                         f"This bot only works in : https://t\\.me/\\+OGXZpC7yGXQ2MDZk \\!",
                         parse_mode='MarkdownV2')
        return
    if message.from_user.username is None:
        bot.send_message(chat_id,
                         f"User has no username , Please create a username in your Telegram settings\\!",
                         parse_mode='MarkdownV2')
        return
    if message.photo is None:
        bot.send_message(chat_id,
                         f"*Please provide a screenshot\\!*\nPlease add a screenshot to prove the task was "
                         f"completed\\.\n\nFor more information, consult the pinned message\\.\\.\\.\nYou can type : "
                         f"/info to get more"
                         f"information\\.\n\nFor more information, consult the pinned message\\.\\.\\.",
                         parse_mode='MarkdownV2')
        return
    if message.caption is None:
        bot.send_message(chat_id,
                         f"*Please provide a keyword of the submission type\\!*\nFor example if you are providing a "
                         f"proof you have upvoted on Dexscreener please type 'dexscreener'\\.\n\nFor more "
                         f"information, consult the pinned message\\.\\.\\.\nYou can type : /info to get more "
                         f"information\\.\n\nFor more information, consult the pinned message\\.\\.\\.",
                         parse_mode='MarkdownV2')
        return
    user_submission_type = message.caption
    if len(message.caption.split()) > 1:
        bot.send_message(chat_id,
                         f"*Please provide a keyword of the submission type\\!*\nFor example if you are providing a "
                         f"proof you have upvoted on Dexscreener please type 'dexscreener'\\.\n\nFor more "
                         f"information, consult the pinned message\\.\\.\\.\nYou can type : /info to get more "
                         f"information\\.\n\nFor more information, consult the pinned message\\.\\.\\.",
                         parse_mode='MarkdownV2')
        return
    standard_form = convert_to_standard(user_submission_type)
    if standard_form in allowable_submissions:  # this means user has submitted a potentially allowable submission
        if user_funds.check_user_exist(user_name):  # if user is registered
            if user_tasks.check_user_exist(user_name):
                # fetch the existing tasks
                temp = user_tasks.get_user_tesks(user_name).split()  # split into list
                if standard_form not in temp:
                    temp.append(standard_form + " " + str(time.time()))
                    completed_tasks = " ".join(temp)
                    user_tasks.update_completed_tasks(user_name, completed_tasks)
                    fund_user(user_name, standard_form, chat_id)
                else:
                    last_epoch = 0
                    updated = False
                    time_left = 0
                    for index, item in enumerate(temp):
                        if item == standard_form:
                            last_epoch = int(float(temp[index + 1]))
                            if time.time() - last_epoch >= int(time_outs[standard_form]):
                                temp[index + 1] = str(time.time())  # change it to current time
                                completed_tasks = " ".join(temp)
                                user_tasks.update_completed_tasks(user_name, completed_tasks)
                                fund_user(user_name, standard_form, chat_id)
                                updated = True
                            break
                    if not updated:
                        time_left = int(float(time_outs[standard_form]) / float(60 * 60) - float(
                            (time.time() - last_epoch) / float(60 * 60)))
                        if time_left > 10000:
                            bot.send_message(chat_id,
                                             f"*Task Already competed\\!*\nThis task has already been completed and "
                                             f"cannot be completed again\\!\\.",
                                             parse_mode='MarkdownV2')
                            return
                        hour_string = "hours"
                        if time_left == 1:
                            hour_string = "one hour"
                        bot.send_message(chat_id,
                                         f"*Task Already competed\\!*\nThis task has already been completed\\.Please "
                                         f"Try again in {time_left} {hour_string}\\!\\.",
                                         parse_mode='MarkdownV2')
                        return
            else:
                user_tasks.add_user(user_name)
                user_tasks.update_completed_tasks(user_name, standard_form + " " + str(time.time()))
                fund_user(user_name, standard_form, chat_id)
        else:
            bot.send_message(chat_id,
                             f"*User not registered*\nPlease register an account using : https://t\\.me/mBTCTipbot\\.",
                             parse_mode='MarkdownV2')
            return
    else:
        best_choice = process.extractOne(standard_form, choices)[0].replace(".", "\\.")
        # here try to give suggestion to what they actually might of meant usign the library fuzzy wuzy
        bot.send_message(chat_id,
                         f"*Invalid submission*\nDid you mean: *{best_choice}*?\n\nPlease provide a valid keyword "
                         f"to match your submission for example"
                         f":'dextools' for a DexTools upvote submission\\.You can type : /info to get more "
                         f"information\\.\n\nFor more information, consult the pinned message\\.\\.\\.",
                         parse_mode='MarkdownV2')
        return


def fund_user(username, task_completed, chat_id):
    tipper = "@CryptoSniper000"
    amount_to_tip = int(allowable_submissions[task_completed])
    new_tipper_balance = int(user_funds.check_user_balance(tipper)) - int(amount_to_tip)
    username_to_tip_balance = int(user_funds.check_user_balance(username))
    new_username_to_tip_balance = username_to_tip_balance + int(amount_to_tip)
    user_funds.update_balance(tipper, new_tipper_balance)
    user_funds.update_balance(username, new_username_to_tip_balance)
    bot.send_message(chat_id, f"{username} has been tipped {amount_to_tip} mSatoshis for completing a task")


if __name__ == "__main__":
    bot.infinity_polling(timeout=None)
