import telebot
import userfunds
from requests import request
import getlppoolinfo
import get_trending_coins
import usertasksdb
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import raidleaderboard
import hashlib
import image_verification

paused_users = []  # user to keep specific memebers paused.

leaderboard = raidleaderboard.ShillStats()
my_token = '6896610984:AAHOE6ft3wbyXMuAC1FBssFJ4RA5FEWMC-w'
bot = telebot.TeleBot(my_token)
user_funds = userfunds.FundsDatabase()
user_tasks = usertasksdb.UserRewardDb()
allowable_submissions = {
    "dextools": 100000000,
    "dexscreener": 20000000,
    "birdeye": 50000000,
    "gemsradar": 100000000,
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
    "x": 25000000,
    "cmc-comment": 20000000000,
    "cmc-watchlist": 250000000,
    "x-follow": 125000000,
    "x-saylor": 250000000,
    "x-davinci": 250000000,
    "medium": 2000000000
}
""""reddit-upvote": 25000000,
    "reddit-commnet": 25000000,
    "reddit-post": 100000000"""

infinity = 999999999999999999999999
twenty_four_hours = 60 * 60 * 24
six_hours = 60 * 60 * 6
one_hour = 60 * 60
thirty_minutes = 60 * 30
twenty_minutes = 20 * 60
five_minutes = 5 * 60
ten_minutes = 10 * 60
fiveteen_minutes = 15 * 60
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
    "x": five_minutes,
    "cmc-comment": six_hours,
    "cmc-watchlist": infinity,
    "x-follow": infinity,
    "x-saylor": twenty_four_hours,
    "x-davinci": twenty_four_hours,
    "medium": infinity
}
choices = ['dextools', 'dexscreener', 'birdeye', 'gemsradar', 'coinalpha', 'coincatapult', 'coinmoonhunt',
           'coindiscovery',
           'coinbazooka', 'coinscope', 'ntm.ai', 'top100token', 'rugfreecoins', 'coinboom', 'coinmooner', 'coinhunt',
           "CNToken.io", "Coinvote", "x", "cmc-comment", "cmc-watchlist", "x-follow", "x-saylor", "x-davinci","medium"]


@bot.message_handler(commands=['expense'])
def expense_check():
    user_count = 118
    four_days = 60 * 60 * 24 * 4
    top_submission = 0
    top_using_task = ""
    for key in allowable_submissions:  # also need to account for time
        if int(allowable_submissions[key]) / int(time_outs[key]) > top_submission:
            top_using_task = key
            top_submission = int(allowable_submissions[key]) / int(time_outs[key])  # msats per second
    print(f"Current expense: " + str(
        (user_count * four_days * top_submission) / 100000000000) + f" By task {top_using_task} as a upperbound")


@bot.message_handler(commands=[
    'disqualify'])  # set to 0 and set the tokens earned back to me and also set their other database balance to zero
def rain(message):
    user_name = "@" + message.from_user.username
    chat_id = message.chat.id
    if user_name == "@MINI_BTC_CHAD" or user_name == "@LongIt345" or user_name == "@CryptoSniper000":
        arguments = message.text.split()
        user_to_remove = arguments[1]
        if leaderboard.check_user_exist(user_to_remove):
            current_balance = leaderboard.fetch_total_earned(user_to_remove)
            if int(current_balance) > 0:
                leaderboard.add_to_total_earnings(user_to_remove, -current_balance)
                user_funds.update_balance(user_to_remove, 0)
                dev_balance = int(user_funds.check_user_balance("@CryptoSniper000"))
                reimbursed_balance = dev_balance + current_balance
                user_funds.update_balance("@CryptoSniper000", reimbursed_balance)  # add back the balance to the dev
                bot.send_message(chat_id, f"{user_to_remove} has been disqualified!")


@bot.message_handler(commands=['special_x'])
def rain(message):
    expense_check()
    chat_id = message.chat.id
    if chat_id != -1002066433992:  # not allow as make it only work for that group only
        bot.send_message(chat_id,
                         f"This bot only works in : https://t\\.me/\\+OGXZpC7yGXQ2MDZk \\!",
                         parse_mode='MarkdownV2')
        return
    bot.send_message(chat_id, "*X/Twitter \\- Special Bounties:*\n\nWe have special X bounties dedicated to Michael "
                              "Saylor and DaVinci that pay at a higher the rate of a regular X bounty\\.\n Simply type 'X\\-"
                              "Saylor' or 'X\\-Davinci' in the rewards channel, and attach the relevant "
                              "screenshot\\.\nYou must abide by the following requirements with your X post:\n🟣 Use "
                              "the following hashtags in your reply:\n\\$mBTC \\#Bitcoin \\#BitcoinOnSolana \\#sol "
                              "\\#meme \\#utility\n🟣 Tag our official Twitter \\- @mbtc\\_sol\n🟣 X "
                              "account must not be shadow banned\\.\nCheck here: Shadowban \\("
                              "https://shadowban\\.yuzurisa\\.com/\\)\n🟣 Ensure your reply is posted on a ["
                              "@Davincij15 Profile](https://twitter\\.com/Davincij15) or [@saylor Profile]("
                              "https://twitter\\.com/saylor) post less than 6 hours old\n🟣 And most importantly, "
                              "please attach the Saylor GIF for your Saylor reply or Davinci GIF for your Davinci "
                              "reply\\. Download links below\\!\n\nDaVinci GIF: [Link]("
                              "https://imgur\\.com/IlkOdMI)\nSaylor GIF: [Link]("
                              "https://imgur\\.com/a/PglCK7N)\n\nThis bounty can only be claimed once every "
                              "24 hours per user\nYou will receive 💰 25,000,000 mSatoshis on submission of a "
                              "valid screenshot\\!"
                     , parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['raid_shitcoins'])
def rain(message):
    chat_id = message.chat.id
    if chat_id != -1002066433992:  # not allow as make it only work for that group only
        bot.send_message(chat_id,
                         f"This bot only works in : https://t\\.me/\\+OGXZpC7yGXQ2MDZk \\!",
                         parse_mode='MarkdownV2')
        return
    bot.send_message(chat_id, "🟣 *X/Twitter \\- raid $HULVIN and \\#HULVIN posts\\!*\n\nHULVIN is a "
                              "halving\\-meta token on"
                              "SOL sitting at $20m market cap\\. People are falsely claiming that it was the first token to the halving "
                              "meta\\.\n\nReply to any $HULVIN posts, and shill $mBTC on them\\. These can include the official ["
                              "HULVIN X account](https://twitter\\.com/hulvinsol) and any $HULVIN relevant posts\\.\n\n*Consider "
                              "the following pointers and anything else you can come up with:*\n\n🟣 We were first\\. $mBTC was "
                              "launched on 3rd April, whereas $HULVIN was made a week later\n\n🟣 We have actual utilities, $HULVIN does "
                              "not\n\n🟣 $mBTC is a much lower market cap, therefore a bargain in comparison and much more scope for "
                              "growth\n\n*You must abide by the following requirements with your X post:*\n\n🟣 Tag "
                              "@mbtc\\_sol\n\n🟣 Do not reply to a post more than 12 hours old\n\n🟣 Each reply should be "
                              "unique and thoughtful\\. Don't come across as spammy/AI generated\\.\n\n🟣 Use the following hashtags "
                              "in your reply:\n\n\\_$mBTC \\#halving \\#Bitcoin \\#BitcoinOnSolana \\#sol \\#meme "
                              "\\#utility\\_\n\n🟣 X account must not be shadow banned\\. Check here: Shadowban \\("
                              "https://shadowban\\.yuzurisa\\.com/\\)\n\n*Simply type \'X\\-Meta\' in the rewards "
                              "channel, and attach the screenshot of the shill post made\\. Any irrelevant posts that do not meet the "
                              "requirements can result in disqualification\\.\n\nThe cooldown period for this bounty is *15 minutes "
                              "hours*\n\n*You will receive *50,000,000* mSatoshis on submission of the "
                              "screenshot\\!"
                     , parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['follow_x'])
def rain(message):
    chat_id = message.chat.id
    if chat_id != -1002066433992:  # not allow as make it only work for that group only
        bot.send_message(chat_id,
                         f"This bot only works in : https://t\\.me/\\+OGXZpC7yGXQ2MDZk \\!",
                         parse_mode='MarkdownV2')
        return
    bot.send_message(chat_id, "🟣 *Follow our X:*\nFollow our X with your official account:\n\n[@mbtc\\_sol]("
                              "https://twitter\\.com/mbtc\\_sol)\n\nEnsure you meet the requirements:\n🟣 Not "
                              "shadow\\-banned\\. Check here: [\\_Link\\_](https://shadowban\\.yuzurisa\\.com/)\n🟣 "
                              "Post a valid screenshot, proving you are following us\n🟣 Duplicate screenshots will "
                              "result in disqualification\nAttach the keyword: *x\\-follow* with your screenshot for "
                              "submission to be valid\n\n*This bounty can only be completed once per user*\nPays "
                              "out: *125,000,000 mSats*"
                     , parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['vote_cmc'])
def rain(message):
    chat_id = message.chat.id
    if chat_id != -1002066433992:  # not allow as make it only work for that group only
        bot.send_message(chat_id,
                         f"This bot only works in : https://t\\.me/\\+OGXZpC7yGXQ2MDZk \\!",
                         parse_mode='MarkdownV2')
        return
    bot.send_message(chat_id,
                     "To celebrate our CMC listing we are introducing 2 bounties\\.\n\n1\\) Post a bullish comment on "
                     "our CMC"
                     "page: https://coinmarketcap\\.com/currencies/mini\\-bitcoin/\\! \n\nEnsure the following with your comments:\n🟣 Not AI\\-generated and generic\n🟣 "
                     "Comes across as"
                     "genuine and not spammy\n\n*This bounty can only be completed once per hour\n\nPays out:\n1,500,000,"
                     "000 mSats\n\n2\\) Click the ⭐️ in the top left corner of our official CMC page to join the Mini Bitcoin "
                     "watchlist\\. Can only be completed once\\. \n\n*This bounty can only be completed once per user\nPays "
                     "out:\n250,000,000 mSats\n\n*Keywords to use with your screenshot:*\nFor watchlist: cmc\\-watchlist\nFor comment: cmc\\-comment",
                     parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['vote_x'])
def rain(message):
    chat_id = message.chat.id
    if chat_id != -1002066433992:  # not allow as make it only work for that group only
        bot.send_message(chat_id,
                         f"This bot only works in : https://t\\.me/\\+OGXZpC7yGXQ2MDZk \\!",
                         parse_mode='MarkdownV2')
        return
    bot.send_message(chat_id,
                     f"*__X/Twitter__*\nWe've introduced an X bounty that can be claimed once every 5 minutes\\.\n\nSimply type "
                     f"'X' in the rewards channel, and attach the screenshot of the shill post made on X\\.\n\nYou must abide "
                     f"by the following requirements with your X post:\n🟣 You must reply to a crypto influencer with more than "
                     f"*50k followers* on a post *less* than *4hrs old*\n🟣 Use the following hashtags in your reply:\n\\$mBTC "
                     f"_\\#Bitcoin \\#BitcoinOnSolana \\#sol \\#meme \\#utility_\n🟣 X account must not be shadow banned\\. Check here:  "
                     f"[Shadowban](https://shadowban\\.yuzurisa\\.com/)\n🟣 And most importantly, please attach the recently made "
                     f"comparison chart in your shill post\\!\n\nComparison chart download: [Link]("
                     f"https://i\\.ibb\\.co/PtzJw86/Comparison\\.png)\nYou are early download: [Link]("
                     f"https://i\\.ibb\\.co/j3L7N6V/Programmed-to-send-2\\.png)\n\nYou will receive *30000000* mSatoshis on "
                     f"submission of the"
                     f"screenshot\\.",
                     parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['vote_info'])
def rain(message):
    chat_id = message.chat.id
    if chat_id != -1002066433992:  # not allow as make it only work for that group only
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
                     f"?chain=solana) hit the 👍🏻 \\(20,000,000 mSatoshis\\) \\(One Time\\)\n\n[DexScreener]("
                     f"https://dexscreener\\.com/solana/ddnvc5rvvzejlunkbf6xsdqha6gpkblxyq8z1bzaotuc)  hit the 🚀 \\(25,000,"
                     f"000 mSatoshis\\) \\(Vote every hour\\)\n\nReach X votes and get "
                     f"listed:\n\n[GemsRadar](https://gemsradar\\.com/coins/mini-bitcoin) login and vote 🗳 🔥 \\(100,"
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
    chat_id = message.chat.id
    if message.from_user.username is None:
        bot.send_message(chat_id,
                         f"User has no username , Please create a username in your Telegram settings\\!",
                         parse_mode='MarkdownV2')
        return
    user_name = "@" + message.from_user.username
    if user_name == "@MINI_BTC_CHAD" or user_name == "@LongIt345" or user_name == "@CryptoSniper000":  # ignore admin
        return
    if chat_id != -1002066433992:  # not allow as make it only work for that group only
        bot.send_message(chat_id,
                         f"This bot only works in : https://t\\.me/\\+OGXZpC7yGXQ2MDZk \\!",
                         parse_mode='MarkdownV2')
        return
    if message.photo is None:
        bot.send_message(chat_id,
                         f"*🟣 Please provide a screenshot with a correct keyword\\!*\nFor example, if you are "
                         f"providing"
                         f"proof you have upvoted on Dexscreener, please type 'Dexscreener' with the attached "
                         f"screenshot\\.\n\nFor more"
                         f"information, consult the pinned message\\.\\.\\.\n\nOtherwise type: /vote\\_info or /vote\\_cmc or /vote\\_x to get more "
                         f"information\\.",
                         parse_mode='MarkdownV2')
        return
    if message.caption is None:
        bot.send_message(chat_id,
                         f"*🟣 Please provide a keyword of the submission type\\!*\nFor example, if you are providing "
                         f"proof you have upvoted on Dexscreener, please type 'Dexscreener' with the attached "
                         f"screenshot\\.\n\nFor more"
                         f"information, consult the pinned message\\.\\.\\.\n\nOtherwise type: /vote\\_info or /vote\\_cmc or /vote\\_x to get more "
                         f"information\\.",
                         parse_mode='MarkdownV2')
        return
    user_submission_type = message.caption
    if len(message.caption.split()) > 1:
        bot.send_message(chat_id,
                         f"*🟣 Please provide a keyword of the submission type\\!*\nFor example, if you are providing "
                         f"proof you have upvoted on Dexscreener, please type 'Dexscreener' with the attached "
                         f"screenshot\\.\n\nFor more"
                         f"information, consult the pinned message\\.\\.\\.\n\nOtherwise type: /vote\\_info or /vote\\_cmc or /vote\\_x to get more "
                         f"information\\.",
                         parse_mode='MarkdownV2')
        return
    # perform a security check on the image
    standard_form = convert_to_standard(user_submission_type)
    if standard_form in allowable_submissions:  # this means user has submitted a potentially allowable submission
        if user_funds.check_user_exist(user_name):  # if user is registered
            if user_tasks.check_user_exist(user_name):
                # fetch the existing tasks
                temp = user_tasks.get_user_tesks(user_name).split()  # split into list
                if standard_form not in temp:
                    raw = message.photo[0].file_id
                    file_info = bot.get_file(raw)
                    downloaded_file = bot.download_file(file_info.file_path)
                    readable_hash = hashlib.sha256(downloaded_file).hexdigest()
                    if not image_verification.verify_image(
                            str(readable_hash)):  # if it failed (then give the user a warning!)
                        user_name = user_name.replace("_", "\\_")
                        bot.send_message(chat_id,
                                         f"⚠️ Our Systems have detected signs of cheating ⚠️\n\n❌ User : {user_name} may be disqualified "
                                         f"if this presists\\!\n\n @CryptoSniper000 please review this incident",
                                         parse_mode='MarkdownV2')
                        return
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
                                # check if the image is sound
                                raw = message.photo[0].file_id
                                file_info = bot.get_file(raw)
                                downloaded_file = bot.download_file(file_info.file_path)
                                readable_hash = hashlib.sha256(downloaded_file).hexdigest()
                                if not image_verification.verify_image(
                                        str(readable_hash)):  # if it failed (then give the user a warning!)
                                    user_name = user_name.replace("_", "\\_")
                                    bot.send_message(chat_id,
                                                     f"⚠️ Our Systems have detected signs of cheating ⚠️\n\n❌ User : {user_name} may be disqualified "
                                                     f"if this presists\\!\n\n @CryptoSniper000 please review this incident",
                                                     parse_mode='MarkdownV2')
                                    return
                                temp[index + 1] = str(time.time())  # change it to current time
                                completed_tasks = " ".join(temp)
                                user_tasks.update_completed_tasks(user_name, completed_tasks)
                                print(f"{user_name}  completed {standard_form}")
                                fund_user(user_name, standard_form, chat_id)
                                updated = True
                                break  # changed this
                    if not updated:
                        time_left = int(float(time_outs[standard_form]) / float(60 * 60) - float(
                            (time.time() - last_epoch) / float(60 * 60)))
                        if time_left > 10000:
                            bot.send_message(chat_id,
                                             f"*Task Already competed\\!*\nThis task has already been completed and "
                                             f"cannot be completed again\\!",
                                             parse_mode='MarkdownV2')
                            return
                        hour_string = "hours"
                        if time_left == 1:
                            hour_string = "one hour"
                        elif time_left == 0:
                            time_left = int(float(time_outs[standard_form]) / float(60) - float(
                                (time.time() - last_epoch) / float(60)))
                            if time_left == 0:
                                time_left = int(float(time_outs[standard_form]) - float(
                                    (time.time() - last_epoch)))
                                hour_string = "Seconds"
                            else:
                                if time_left == 1:
                                    hour_string = "minute"
                                else:
                                    hour_string = "minutes"
                        bot.send_message(chat_id,
                                         f"*Task Already competed\\!*\nThis task has already been completed\\.Please "
                                         f"Try again in {time_left} {hour_string}\\!",
                                         parse_mode='MarkdownV2')
                        return
            else:
                user_tasks.add_user(user_name)
                user_tasks.update_completed_tasks(user_name, standard_form + " " + str(time.time()))
                print(f"{user_name}  completed {standard_form}")
                fund_user(user_name, standard_form, chat_id)
                return
        else:
            bot.send_message(chat_id,
                             f"*User not registered*\nPlease register an account using : https://t\\.me/mBTCTipbot\\.",
                             parse_mode='MarkdownV2')
            return
    else:
        best_choice = process.extractOne(standard_form, choices)[0].replace(".", "\\.")
        best_choice = best_choice.replace("-", "\\-")
        bot.send_message(chat_id,
                         f"🟣 *Invalid submission*\nDid you mean: *{best_choice}*?\n\nFor example, if you are providing "
                         f"proof you have upvoted on Dexscreener, please type 'Dexscreener' with the attached "
                         f"screenshot\\.\n\nOtherwise type: /vote\\_info or /vote\\_cmc or /vote\\_x to get more "
                         f"information\\.",
                         parse_mode='MarkdownV2')
        return


def show_delay(standard_form):
    time_left = int(time_outs[standard_form] / 3600)  # hours
    if time_left > 10000:
        return "Cannot be completed again"
    hour_string = "hours"
    if time_left == 1:
        hour_string = "hour"
    elif time_left == 0:
        time_left = int(float(time_outs[standard_form]) / float(60))  # minutes
        if time_left == 0:
            time_left = int(float(time_outs[standard_form]))  # seconds
            hour_string = "Seconds"
        else:
            if time_left == 1:
                hour_string = "minute"
            else:
                hour_string = "minutes"
    return f"{time_left} {hour_string}"


def fund_user(username, task_completed, chat_id):
    tipper = "@CryptoSniper000"
    amount_to_tip = int(allowable_submissions[task_completed])
    if user_funds.check_user_balance(tipper) < amount_to_tip:
        bot.send_message(chat_id, "error!")
        return
    new_tipper_balance = int(user_funds.check_user_balance(tipper)) - int(amount_to_tip)
    username_to_tip_balance = int(user_funds.check_user_balance(username))
    new_username_to_tip_balance = username_to_tip_balance + int(amount_to_tip)
    user_funds.update_balance(tipper, new_tipper_balance)
    user_funds.update_balance(username, new_username_to_tip_balance)
    # update user stats here #
    if leaderboard.check_user_exist(username):
        leaderboard.increment_task_count(username)
        leaderboard.add_to_total_earnings(username, amount_to_tip)
    else:
        leaderboard.add_user(username)
        leaderboard.increment_task_count(username)
        leaderboard.add_to_total_earnings(username, amount_to_tip)
        # task_completed = task_completed.replace(".", "\\.")
        # task_completed = task_completed.replace("_", "\\_")
    bot.send_message(chat_id,
                     f"{username} has been tipped {amount_to_tip} mSatoshis for completing ({task_completed}) task! "
                     f"The cooldown on this task is: {show_delay(task_completed)}")


if __name__ == "__main__":
    bot.infinity_polling(timeout=None)
