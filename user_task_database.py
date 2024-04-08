import telebot
import userfunds
from requests import request
import getlppoolinfo
import get_trending_coins
import usertasksdb

my_token = '6896610984:AAHOE6ft3wbyXMuAC1FBssFJ4RA5FEWMC-w'
bot = telebot.TeleBot(my_token)
user_funds = userfunds.FundsDatabase()
user_tasks = usertasksdb.UserRewardDb()
allowable_submissions = {
    "dextools": 5000000,
    "dexscreener": 2500000,
    "birdeye": 1000000,
    "gemsradar": 10000000,
    "coinalpha": 1000000,
    "coincatapult": 1000000,
    "coinmoonhunt": 1000000,
    "coindiscovery": 1000000,
    "coinbazooka": 250000,
    "coinscope": 250000,
    "coinsniper": 250000,
    "ntm.ai": 250000,
    "top100token": 250000,
    "rugfreecoins": 150000,
    "coinboom": 30000,
    "coinmooner": 30000,
    "coinhunt": 200000
}


def convert_to_standard(input_string):
    lower_case_string = input_string.lower()
    lower_case_string = lower_case_string.strip()  # remove any spaces
    return lower_case_string


@bot.message_handler(func=lambda message: True,
                     content_types=['photo', 'text'])  # any message ( needs to check if user attaches a picture too)
def check_submission(message):
    chat_id = message.chat.id
    if message.photo is None:
        bot.send_message(chat_id,
                         f"*Please provide a screenshot\\!*\nPlease add a screenshot to prove the task was completed\\.",
                         parse_mode='MarkdownV2')
        return
    if message.caption is None:
        bot.send_message(chat_id,
                         f"*Please provide a keyword of the submission type\\!*\nFor example if you are providing a "
                         f"proof you have upvoted on Dexscreener please type 'dexscreener'\\.",
                         parse_mode='MarkdownV2')
        return
    user_submission_type = message.caption
    standard_form = convert_to_standard(user_submission_type)
    print(standard_form)
    user_name = "@" + message.from_user.username
    if standard_form in allowable_submissions:  # this means user has submitted a potentially allowable submission
        if user_funds.check_user_exist(user_name):  # if user is registered
            if user_tasks.check_user_exist(user_name):
                # fetch the existing tasks
                temp = user_tasks.get_user_tesks(user_name).split()  # split into list
                if standard_form not in temp:
                    temp.append(standard_form)
                    completed_tasks = " ".join(temp)
                    user_tasks.update_completed_tasks(user_name, completed_tasks)
                    fund_user(user_name, standard_form, chat_id)
                else:
                    bot.send_message(chat_id,
                                     f"*Task Already competed\\!*\nThis task has already been completed\\!\\.",
                                     parse_mode='MarkdownV2')
                    return
            else:
                user_tasks.add_user(user_name)
                user_tasks.update_completed_tasks(user_name, standard_form)
                fund_user(user_name, standard_form, chat_id)
        else:
            bot.send_message(chat_id,
                             f"*User not registered*\nPlease register an account using : https://t.me/mBTCTipbot\\.",
                             parse_mode='MarkdownV2')
            return
    else:
        bot.send_message(chat_id,
                         f"*Invalid submission*\nPlease provide a valid keyword to match your submission for example "
                         f":'dextools' for a DexTools upvote submission\\.",
                         parse_mode='MarkdownV2')
        return
        # error
    # check if the user exists
    # check if they already submitted the task
    # if not then add it to database and credit them
    # else give warnings


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
