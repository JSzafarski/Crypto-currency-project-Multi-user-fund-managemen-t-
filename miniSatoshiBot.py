from time import strftime, localtime
import time
import math
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

raider_cooldown_tracker = {"@Bligga": 0,
                           "@BarberQc": 0,
                           "@Naterulestheworld": 0,
                           "@laaazim": 0,
                           "@KevvnnDR": 0}


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


# special command for detecting raiders
@bot.message_handler(commands=['raid'])
def raid(message):
    reward_amount = 100000000  # 100 m msats
    cooldown = 60 * 15  # 15 minutes
    chat_id = message.chat.id
    user = "@" + message.from_user.username
    if chat_id == -1002130978267:
        if user in raider_cooldown_tracker:
            if user in raider_cooldown_tracker:  # means they have used the bot
                last_time = int(raider_cooldown_tracker[user])
                if time.time() > last_time + cooldown:
                    raider_cooldown_tracker[user] = time.time()
                    tipper = "@CryptoSniper000"
                    if funds_database.check_user_balance(tipper) < reward_amount:
                        return
                    amount_to_tip = reward_amount
                    new_tipper_balance = int(funds_database.check_user_balance(tipper)) - int(amount_to_tip)
                    username_to_tip_balance = int(funds_database.check_user_balance(user))
                    new_username_to_tip_balance = username_to_tip_balance + int(amount_to_tip)
                    funds_database.update_balance(tipper, new_tipper_balance)
                    funds_database.update_balance(user, new_username_to_tip_balance)
                    sats_balance = float(reward_amount)
                    amount_in_dollars = ((float(int(sats_balance)) / float(100000000000)) * get_price())
                    substring = f"{amount_in_dollars:.2f}".replace(".", "\\.")
                    bot.send_message(chat_id,
                                     f"🤖 Raider: {user} , has been tipped *100000000*mSats \\(${substring}\\) for raiding\\!",
                                     parse_mode='MarkdownV2')
                    # chenge new time to this time creadit raider inform them they got credited and the next time
                    # until they get credited if they radi again (they can radie again before creditign time


# shill bot commands in main :

@bot.message_handler(commands=['special_x'])
def rain(message):
    chat_id = message.chat.id
    if chat_id == -1002130978267:
        bot.send_message(chat_id,
                         "*X/Twitter \\- Special Bounties:*\n\nWe have special X bounties dedicated to Michael "
                         "Saylor and DaVinci that pay *5x* 📈 the rate of a regular X bounty\\.\n Simply type 'X\\-"
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
                         "24 hours per user\nYou will receive 💰 500,000,000 mSatoshis on submission of a "
                         "valid screenshot\\!"
                         , parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['follow_x'])
def rain(message):
    chat_id = message.chat.id
    if chat_id == -1002130978267:
        bot.send_message(chat_id, "🟣 *Follow our X:*\nFollow our X with your official account:\n\n[@mbtc\\_sol]("
                                  "https://twitter\\.com/mbtc\\_sol)\n\nEnsure you meet the requirements:\n🟣 Not "
                                  "shadow\\-banned\\. Check here: [\\_Link\\_](https://shadowban\\.yuzurisa\\.com/)\n🟣 "
                                  "Post a valid screenshot, proving you are following us\n🟣 Duplicate screenshots will "
                                  "result in disqualification\nAttach the keyword: *x\\-follow* with your screenshot for "
                                  "submission to be valid\n\n*This bounty can only be completed once per user*\nPays "
                                  "out: *250,000,000 mSats*"
                         , parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['vote_cmc'])
def rain(message):
    chat_id = message.chat.id
    if chat_id == -1002130978267:
        bot.send_message(chat_id,
                         "To celebrate our CMC listing we are introducing 2 bounties\\.\n\n1\\) Post a bullish comment on "
                         "our CMC"
                         "page: https://coinmarketcap\\.com/currencies/mini\\-bitcoin/\\! \n\nEnsure the following with your comments:\n🟣 Not AI\\-generated and generic\n🟣 "
                         "Comes across as"
                         "genuine and not spammy\n\n*This bounty can only be completed once per hour\n\nPays out:\n1,000,000,"
                         "000 mSats\n\n2\\) Click the ⭐️ in the top left corner of our official CMC page to join the Mini Bitcoin "
                         "watchlist\\. Can only be completed once\\. \n\n*This bounty can only be completed once per user\nPays "
                         "out:\n250,000,000 mSats\n\n*Keywords to use with your screenshot:*\nFor watchlist: cmc\\-watchlist\nFor comment: cmc\\-comment",
                         parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['vote_x'])
def rain(message):
    chat_id = message.chat.id
    if chat_id == -1002130978267:
        bot.send_message(chat_id,
                         f"*__X/Twitter__*\nWe've introduced an X bounty that can be claimed once every 5 minutes\\.\n\nSimply type "
                         f"'X' in the rewards channel, and attach the screenshot of the shill post made on X\\.\n\nYou must abide "
                         f"by the following requirements with your X post:\n🟣 You must reply to a crypto influencer with more than "
                         f"*50k followers* on a post *less* than *4hrs old*\n🟣 Use the following hashtags in your reply:\n\\$mBTC "
                         f"_\\#Bitcoin \\#BitcoinOnSolana \\#sol \\#meme \\#utility_\n🟣 X account must not be shadow banned\\. Check here:  "
                         f"[Shadowban](https://shadowban\\.yuzurisa\\.com/)\n🟣 And most importantly, please attach the recently made "
                         f"comparison chart in your shill post\\!\n\nComparison chart download: [Link]("
                         f"https://i\\.ibb\\.co/PtzJw86/Comparison\\.png)\nYou are early download: [Link]("
                         f"https://i\\.ibb\\.co/j3L7N6V/Programmed-to-send-2\\.png)\n\nYou will receive *50000000* mSatoshis on "
                         f"submission of the"
                         f"screenshot\\.",
                         parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['vote_info'])
def rain(message):
    chat_id = message.chat.id
    if chat_id == -1002130978267:
        bot.send_message(chat_id,
                         f"🟣 __Vote Bounty Info:__\n\nVote on the trackers below, and attach a screenshot with the name of the "
                         f"tracker to instantly receive your reward\\.\n\n💸💸 Click any of the links below to get started\\! 💸💸\n\n["
                         f"DexTools](https://www\\.dextools\\.io/app/en/solana/pair-explorer"
                         f"/DDnvC5rvvZeJLuNKBF6xsdqHA6GPKbLxYq8z1bzaotUC?t=1712460479955) hit the 👍🏻 \\(100,000,000 mSatoshis\\) "
                         f"\\(Vote one time\\)\n\n[Birdeye](https://birdeye\\.so/token/mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ"
                         f"?chain=solana) hit the 👍🏻 \\(50,000,000 mSatoshis\\) \\(One Time\\)\n\n[DexScreener]("
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


####################################

def determine_time_left_till_reset():
    reference_reset_leaderboard_time = 1713092400  # seed
    interval = 60 * 60 * 24 * 4  # 4 days
    current_time = time.time()
    absoloute_difference = abs(reference_reset_leaderboard_time - current_time)  # time since seed
    epoch_val = int((interval - (absoloute_difference % interval)) // 3600)
    if epoch_val // 24 > 0:
        if int(epoch_val / 24) == 1:
            return str(int(epoch_val / 24)) + " day"
        return str(int(epoch_val / 24)) + " days"
    else:
        return str(epoch_val) + " hours"


@bot.message_handler(commands=['position'])
def position_users(message):
    chat_id = message.chat.id
    user = "@" + message.from_user.username
    if chat_id == -1002130978267:
        if leaderboard.check_user_exist:
            position = leaderboard.get_position(user)
            user = user.replace("_", "\\_")
            bot.send_message(chat_id,
                             f"Dear, {user} you are position *{position}* on this week's shill\\-to\\-earn leaderboard",
                             parse_mode='MarkdownV2', disable_web_page_preview=True)
        else:
            bot.send_message(chat_id, "User has not yet used shill to earn!",
                             parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['leaderboard'])
def leader_board(message):
    chat_id = message.chat.id
    if chat_id == -1002130978267:
        total_earned = leaderboard.get_total_awards()
        task_count = leaderboard.get_total_tasks()
        top_users = leaderboard.get_top_five()
        number_shillers = leaderboard.get_total_users()
        time_left = determine_time_left_till_reset()
        # convert total earned to dollars too
        sats_balance = float(total_earned)
        amount_in_dollars = ((float(int(sats_balance)) / float(100000000000)) * get_price())
        total_earned_dollars = f"{amount_in_dollars:.2f}".replace(".", "\\.")
        bot.send_message(chat_id,
                         f"🟣 *__Shill to earn Leaderboard__*\n\n{top_users}\n💰 Total earned: *{total_earned}*mSats \\(${total_earned_dollars}\\)\n📚 Total "
                         f"tasks completed: *{task_count}*\n👯 Number of shillers: *{number_shillers}*\n🕐 Time left: *{time_left}*\n\n👯 [Join rewards"
                         f" group]("
                         f"https://t\\.me/\\+OGXZpC7yGXQ2MDZk)",
                         parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['supplyleft'])
def supplyleft(message):
    chat_id = message.chat.id
    if chat_id == -1002130978267:
        supply = getlppoolinfo.get_lp_info()
        bot.send_message(chat_id, f"Supply left in the Liquidity pool : *{supply}*",
                         parse_mode='MarkdownV2')


@bot.message_handler(commands=['getprice'])
def rain(message):
    chat_id = message.chat.id
    if chat_id == -1002130978267:
        price = str(get_price()).replace(".", ",")
        bot.send_message(chat_id, f"Mini Bitcoin price : *{price}$*",
                         parse_mode='MarkdownV2')


@bot.message_handler(commands=['compare'])  # compare it to trending coins on sol
def rain(message):
    chat_id = message.chat.id
    if chat_id == -1002130978267:
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
    if chat_id == -1002130978267:
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
    if chat_id == -1002130978267:
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
    if chat_id == -1002130978267:
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
    if chat_id == -1002130978267:
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
                    bot.send_message(chat_id,
                                     f"*Requires an Integer Input*\nPlease Provide a whole number in mSatoshis\\.",
                                     parse_mode='MarkdownV2')
                    return
                else:
                    if int(funds_database.check_user_balance(tipper)) >= int(amount_to_tip):
                        new_tipper_balance = int(funds_database.check_user_balance(tipper)) - int(amount_to_tip)
                        username_to_tip_balance = int(funds_database.check_user_balance(username_to_tip))
                        new_username_to_tip_balance = username_to_tip_balance + int(amount_to_tip)
                        funds_database.update_balance(tipper, new_tipper_balance)
                        funds_database.update_balance(username_to_tip, new_username_to_tip_balance)
                        tipper = tipper.replace("_", "\\_")
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
            bot.send_message(chat_id,
                             "Please first Dm the : 'https://t.me/mBTCTipbot' bot to setup a wallet.\nYou will "
                             "need to be tipped by a team member before you can send mBTC to other users in the "
                             "group")
            return


@bot.message_handler(commands=['tip'])
def tipping(message):
    chat_id = message.chat.id
    if chat_id == -1002130978267:
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
                    bot.send_message(chat_id,
                                     f"*Requires an Integer Input*\nPlease Provide a whole number in mSatoshis\\.",
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
            bot.send_message(chat_id,
                             "Please first Dm the : 'https://t.me/mBTCTipbot' bot to setup a wallet.\nYou will "
                             "need to be tipped by a team member before you can send mBTC to other users in the "
                             "group")
            return


@bot.message_handler(commands=['tipmany'])
def rain(message):
    chat_id = message.chat.id
    if chat_id == -1002130978267:
        tipper = "@" + message.from_user.username
        if tipper == "@MINI_BTC_CHAD" or tipper == "@LongIt345" or tipper == "@CryptoSniper000":  # enforce same admin controls across multiple
            tipper = "@CryptoSniper000"
        if funds_database.check_user_exist(tipper):
            arguments = message.text.split()
            argument_length = len(arguments)
            if argument_length < 3:
                bot.send_message(chat_id,
                                 f"*Invalid Input*\nPlease us the following syntax:\n/tip \\<@\\username1\\>\\ "
                                 f"\\<@\\username2\\> \\.\\.\\. \\<@\\username\\>\\"
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
                    bot.send_message(chat_id,
                                     f"*Requires an Integer Input*\nPlease Provide a whole number in mSatoshis\\.",
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
                    bot.send_message(chat_id,
                                     f"{tipper} has tipped {amount_to_tip} mSatoshis each to each selected user.")
                else:  # not enough funds
                    bot.send_message(chat_id,
                                     f"*Insufficient funds*\nThe cumulative amount tipped is greater than your balance\\.",
                                     parse_mode='MarkdownV2')
                    return
        else:
            bot.send_message(chat_id,
                             "Please first Dm the : 'https://t.me/mBTCTipbot' bot to setup a wallet.\nYou will "
                             "need to be tipped by a team member before you can send mBTC to other users in the "
                             "group")
            return


@bot.message_handler(commands=['rain'])  # check why it leaves a comma at the end
def rain(message):
    chat_id = message.chat.id
    if chat_id == -1002130978267:
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
