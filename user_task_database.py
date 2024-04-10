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
    "birdeye": 50000000,
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
    "coinvote": 30000,
    "x": 100000000
}

infinity = 999999999999999999999999
twenty_four_hours = 60 * 60 * 24
six_hours = 60 * 60 * 6
one_hour = 60 * 60
thirty_minutes = 60 * 30
twenty_minutes = 20 * 60
time_outs = {  # ( in epoch time)
    "dextools": infinity,
    "dexscreener": one_hour,
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
    "coinvote": twenty_four_hours,
    "x": twenty_minutes
}
choices = ['dextools', 'dexscreener', 'birdeye', 'gemsradar', 'coinalpha', 'coincatapult', 'coinmoonhunt',
           'coindiscovery',
           'coinbazooka', 'coinscope', 'ntm.ai', 'top100token', 'rugfreecoins', 'coinboom', 'coinmooner', 'coinhunt',
           "CNToken.io", "Coinvote", "x"]


@bot.message_handler(commands=['vote_x'])
def rain(message):
    chat_id = message.chat.id
    if chat_id != -4174401511:  # not allow as make it only work for that group only
        bot.send_message(chat_id,
                         f"This bot only works in : https://t\\.me/\\+OGXZpC7yGXQ2MDZk \\!",
                         parse_mode='MarkdownV2')
        return
    bot.send_message(chat_id,
                     f"__X/Twitter__\n*We've introduced an X bounty that can be claimed once every 20 minutes\\.\n\n*Simply type "
                     f"'X' in the rewards channel, and attach the screenshot of the shill post made on X\\.\n\n*You must abide "
                     f"by the following requirements with your X post:\n🟣 You must reply to a crypto influencer with more than "
                     f"*50k followers* on a post *less* than *4hrs old*\n🟣 Use the following hashtags in your reply:\n\\$mBTC "
                     f"_\\#Bitcoin \\#BitcoinOnSolana \\#sol \\#meme \\#utility_\n🟣 X account must not be shadow banned\\. Check here:  "
                     f"[Shadowban](https://shadowban\\.yuzurisa\\.com/)\n🟣 And most importantly, please attach the recently made "
                     f"comparison chart in your shill post\\!\n\nComparison chart download link: \n[Link]("
                     f"https://i\\.ibb\\.co/PtzJw86/Comparison\\.png)\n\n*You will receive 100000000 mSatoshis on submission of the "
                     f"screenshot\\.",
                     parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['vote_info'])
def rain(message):
    chat_id = message.chat.id
    if chat_id != -4174401511:  # not allow as make it only work for that group only
        bot.send_message(chat_id,
                         f"This bot only works in : https://t\\.me/\\+OGXZpC7yGXQ2MDZk \\!",
                         parse_mode='MarkdownV2')
        return
    bot.send_message(chat_id,
                     f"🟣 __Vote Bounty Info:__\n\nVote on the trackers below, and attach a screenshot with the name of the "
                     f"tracker to instantly receive your reward\\.\n\n💸💸 Click any of the links below to get started\\! 💸💸\n\n["
                     f"DexTools](https://www\\.dextools\\.io/app/en/solana/pair-explorer"
                     f"/DDnvC5rvvZeJLuNKBF6xsdqHA6GPKbLxYq8z1bzaotUC?t=1712460479955) hit the 👍🏻 \\(100,000,000 mSatoshis\\) "
                     f"\\(Vote one time\\)\n\n[Birdeye](https://birdeye\\.so/token/mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ"
                     f"?chain=solana) hit the 👍🏻 \\(50,000,000 mSatoshis\\) \\(Once every 24hours\\)\n\n[DexScreener]("
                     f"https://dexscreener\\.com/solana/ddnvc5rvvzejlunkbf6xsdqha6gpkblxyq8z1bzaotuc)  hit the 🚀 \\(25,000,"
                     f"000 mSatoshis\\) \\(Vote every hour\\)\n\nReach X votes and get "
                     f"listed:\n\n[GemsRadar](https://gemsradar\\.com/coins/mini-bitcoin) login and vote 🗳 🔥 \\(500,"
                     f"000,000 mSatoshis\\) 🔥\n\n[CoinAlpha]("
                     f"https://coinalpha\\.app/token/mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ)  login and vote 🗳 \\(5,000,"
                     f"000 mSatoshis\\) \\(Available every 24hrs\\)\n\n[CoinCatapult]("
                     f"https://coincatapult\\.com/coin/mini-bitcoin-mbtc) vote 🗳 \\(5,000,000 mSatoshis\\) \\(Available every "
                     f"6hrs\\)\n\n[CoinDiscovery](https://coindiscovery\\.app/coin/mini-bitcoin#description) vote 🗳 \\(5,000,"
                     f"000 mSatoshis\\) \\(Available every hour\\)\n\n*Other Trackers:*\n[NTM\\.ai]("
                     f"https://ntm\\.ai/token/mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ?graph"
                     f"=DDnvC5rvvZeJLuNKBF6xsdqHA6GPKbLxYq8z1bzaotUC) vote 'Bullish' or 'Safu' \\(500,000 mSatoshis\\) \\("
                     f"Available"
                     f"every hour\\)\n[CoinBazooka](https://coinbazooka\\.com/coin/mini-bitcoin) vote 🗳 \\(250000 mSatoshis\\) \\("
                     f"Available every 24hrs\\)\n[CoinScope](https://www\\.coinscope\\.co/coin/1-mbtc) login and vote 🗳 \\(250000 "
                     f"mSatoshis\\) \\(Available every 24hrs\\)\n[CoinSniper](https://coinsniper\\.net/coin/63289) login and vote "
                     f"🗳 \\(250000 mSatoshis\\) \\(Available every 24hrs\\)\n[top100token]("
                     f"https://top100token\\.com/address/mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ) vote 🚀 \\(250000 "
                     f"mSatoshis\\) \\("
                     f"Available every 24hrs\\)\n[Rugfreecoins](https://www\\.rugfreecoins\\.com/coin-details/24899) vote 🔥 \\("
                     f"150000 mSatoshis\\) \\(Available every 24hrs\\)\n[CNToken\\.io](https://cncrypto\\.io/coin/mini-bitcoin) vote "
                     f"🗳 \\(150000 mSatoshis\\) \\(Available every 24hrs\\)\n[CoinMoonHunt](https://coinmoonhunt\\.com/coin/Mini "
                     f"Bitcoin)  vote 🗳 \\(150000 mSatoshis\\) \\(Available every hour\\)\n[CoinBoom]("
                     f"https://coinboom\\.net/coin/mini-bitcoin-2) vote 🚀\\(30000 mSatoshis\\) \\(Available every 24hrs\\)\n["
                     f"CoinMooner](https://coinmooner.com/coin/mini-bitcoin-mbtc)  vote 🚀\\(30000 mSatoshis\\) \\(Available every "
                     f"24hrs\\)\n[CoinVote](https://coinvote\\.cc/en/coin/Mini-Bitcoin)  login and hit the 👍🏻 \\(30000 "
                     f"mSatoshis\\) \\(Available every 24hrs\\)",
                     parse_mode='MarkdownV2', disable_web_page_preview=True)


def convert_to_standard(input_string):
    lower_case_string = input_string.lower()
    lower_case_string = lower_case_string.strip()  # remove any spaces
    return lower_case_string


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
                         f"*🟣 Please provide a keyword of the submission type\\!*\nFor example, if you are providing "
                         f"proof you have upvoted on Dexscreener, please type 'Dexscreener' with the attached "
                         f"screenshot\\.\n\nFor more"
                         f"information, consult the pinned message\\.\\.\\.\n\nOtherwise type: /vote_info to get more "
                         f"information\\.",
                         parse_mode='MarkdownV2')
        return
    '''else:  # here check if its only one photo as we want one submission at once
        for index, photo in enumerate(message.photo):
            print(photo.file_id)
            if index > 0:
                bot.send_message(chat_id,
                                 f"*🟣 Please provide only one image per submission\\!*\n\n\nFor more"
                                 f"information, consult the pinned message\\.\\.\\.\n\nOtherwise type: /vote_info to get "
                                 f"more"
                                 f"information\\.",
                                 parse_mode='MarkdownV2')
                return'''
    if message.caption is None:
        bot.send_message(chat_id,
                         f"*🟣 Please provide a keyword of the submission type\\!*\nFor example, if you are providing "
                         f"proof you have upvoted on Dexscreener, please type 'Dexscreener' with the attached "
                         f"screenshot\\.\n\nFor more"
                         f"information, consult the pinned message\\.\\.\\.\n\nOtherwise type: /vote_info to get more "
                         f"information\\.",
                         parse_mode='MarkdownV2')
        return
    user_submission_type = message.caption
    if len(message.caption.split()) > 1:
        bot.send_message(chat_id,
                         f"*🟣 Please provide a keyword of the submission type\\!*\nFor example, if you are providing "
                         f"proof you have upvoted on Dexscreener, please type 'Dexscreener' with the attached "
                         f"screenshot\\.\n\nFor more"
                         f"information, consult the pinned message\\.\\.\\.\n\nOtherwise type: /vote_info to get more "
                         f"information\\.",
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
                            inject_dex_correction = False
                            if time_left > 100000 and standard_form == "dexscreener":
                                inject_dex_correction = True
                            if time.time() - last_epoch >= int(time_outs[standard_form]) or inject_dex_correction:
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
                        elif time_left == 0:
                            time_left = int(float(time_outs[standard_form]) / float(60) - float(
                                (time.time() - last_epoch) / float(60)))
                            hour_string = "Minutes"
                        bot.send_message(chat_id,
                                         f"*Task Already competed\\!*\nThis task has already been completed\\.Please "
                                         f"Try again in {time_left} {hour_string}\\!",
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
                         f"🟣 *Invalid submission*\nDid you mean: *{best_choice}*?\n\nFor example, if you are providing "
                         f"proof you have upvoted on Dexscreener, please type 'Dexscreener' with the attached "
                         f"screenshot\\.\n\nOtherwise type: /info to get more "
                         f"information\\.",
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
    bot.send_message(chat_id, f"{username} has been tipped *{amount_to_tip}* mSatoshis for completing a task\\!",
                     parse_mode='MarkdownV2')


if __name__ == "__main__":
    bot.infinity_polling(timeout=None)
