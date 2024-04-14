import math

from requests import request
from time import strftime, localtime
import telebot
from random import randint
from telebot import types
import requests
import cloudinary
import cloudinary.uploader  # to upload the memes
import os
import threading
import openai
import time
from openai import OpenAI
import re
import filter_response
from requests import request
import getlppoolinfo
import userfunds
import raidleaderboard

funds_database = userfunds.FundsDatabase()

leaderboard = raidleaderboard.ShillStats()
# Enter your Assistant ID here.
ASSISTANT_ID = "asst_OdboRIxKhLQrirwYRHZFhyZd"

# Make sure your API key is set as an environment variable.
client = OpenAI(api_key="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")
halving_epoch = 1713808215 - (60 * 60 * 24 * 3)  # check again if this is accurate
my_token = '6948460970:AAH5pEPFnw13cXlZNPIcva1n9nbPSGdQNoQ'
bot = telebot.TeleBot(my_token)
cloudinary.config(
    cloud_name="dzxvvy103",
    api_key="694682428356438",
    api_secret="JRotWDdIAAGSiUN5Td1_z-4Jbm0"
)

solscan_header = {
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3MDY3NTM5ODAzOTQsImVtYWlsIjoic29sYmFieTMyNUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJpYXQiOjE3MDY3NTM5ODB9.Lp77APFLV-rOnNbDzc1ob43Vp-9-KpeMe_b-fiOQrr0',
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.82 Safari/537.36'
}

meme_header = {
    'Authorization': 'Bearer k+G6i2Tn4edDpPZPOz/rgKvM6KE=',
    'Content-Type': 'application/json'
}

payload = ("{\n  \"text\": \"Mini Bitcoin is a cryptocurrency.Hype,fun,pleasure,excitement,anticipation\"\n}")

last_active_epoch = 0
temp_array = []

OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY


def generate_meme_batch():
    print("fetching a new image batch")
    global temp_array
    meme_response = request('POST',
                            "https://app.supermeme.ai/api/v1/meme/image",
                            headers=meme_header, data=payload)
    print(meme_response)
    meme_json = meme_response.json()
    for index, meme in enumerate(meme_json["memes"]):
        img_data = requests.get(meme).content
        with open(f'img_buffer\\img{index}.jpg', 'wb') as handler:
            handler.write(img_data)
    handler.close()
    # then read each image and upload ti to piranta then grab all the link and place them into the array
    directory_in_str = 'img_buffer\\'
    directory = os.fsencode(directory_in_str)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        cloudinary.uploader.upload(f'{directory_in_str}{filename}')
        print("uploaded: " + str(filename))


def fetch_cloud_img_links():
    global temp_array
    result = cloudinary.Search() \
        .expression("resource_type:image").execute()
    items = result.get("resources")
    for item in items:
        temp_array.append(item["url"])


@bot.message_handler(commands=['meme'])  # use supreme meme api
def send_meme(message):
    global last_active_epoch
    if last_active_epoch == 0:
        last_active_epoch = time.time()
    if time.time() > last_active_epoch + 2.5 * 60 * 60:
        # th = threading.Thread(target=generate_meme_batch)
        # th.start()
        last_active_epoch = time.time()
    fetch_cloud_img_links()
    print(len(temp_array))
    random_index = randint(0, len(temp_array) - 1)
    result = str(temp_array[random_index])
    markup = types.InlineKeyboardMarkup()
    share_string = f"https://twitter.com/intent/tweet?text=$mBTC%20"  # needs slight change
    share = types.InlineKeyboardButton("Share on Twitter 𝕏",
                                       url=f'{share_string}')
    markup.row(share)
    bot.send_message("-1002130978267", f"[🔥]({result}) To share an image simply download and attach it to your post\\.",
                     parse_mode='MarkdownV2', reply_markup=markup)


@bot.message_handler(commands=['shill'])  # using gaht gpt 4 to generate shill text that users can use for raids
def mini_btc_assistant(question):
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                # Update this with the query you want to use.
                "content": "create few sentences about Mini Bitcoin for a promotional purpose",

            }
        ]
    )

    # Submit the thread to the assistant (as a new run).
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id="asst_c7GPtuXzVezfLVPpyDx8VE8D")
    print(f" Run Created: {run.id}")

    # Wait for run to complete.
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f" Run Status: {run.status}")
        time.sleep(1)
    else:
        print(f" Run Completed!")

    # Get the latest message from the thread.
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data

    # Print the latest message.
    latest_message = messages[0]
    response = filter_response.filter_msg(latest_message.content[0].text.value)
    a = " "
    print(response)
    filtered_response = re.sub('【[^>]+】', a, response)
    markup = types.InlineKeyboardMarkup()
    share_string = f"https://twitter.com/intent/tweet?text=$mBTC%20{filtered_response}"  # needs slight change
    share = types.InlineKeyboardButton("Share on Twitter 𝕏",
                                       url=f'{share_string}')
    markup.row(share)
    bot.send_message("-1002130978267",
                     "\n" + f"{filtered_response}", reply_markup=markup)


def get_burn_stat():
    burn_wallet = "@MiniBtcBurn"
    funds = str(funds_database.check_user_balance(burn_wallet))
    return funds


@bot.message_handler(commands=['askbot'])  # using gaht gpt 4 to generate shill text that users can use for raids
def mini_btc_assistant(question):
    # Create a thread with a message.
    arguments = question.text.split()
    arguments.pop(0)
    content = " ".join(arguments)
    print(content)
    if len(content) > 40:
        return "This question is too long please make it a bit shorter"
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                # Update this with the query you want to use.
                "content": "limit your response to 45 words and don't mention any uploaded files: " + str(content),
            }
        ]
    )

    # Submit the thread to the assistant (as a new run).
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    print(f" Run Created: {run.id}")

    # Wait for run to complete.
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f" Run Status: {run.status}")
        time.sleep(1)
    else:
        print(f" Run Completed!")

    # Get the latest message from the thread.
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data

    # Print the latest message.
    latest_message = messages[0]
    response = latest_message.content[0].text.value
    a = " "
    print(response)
    filtered_response = re.sub('【[^>]+】', a, response)
    markup = types.InlineKeyboardMarkup()
    share_string = f"https://twitter.com/intent/tweet?text=$mBTC%20{filtered_response}"  # needs slight change
    share = types.InlineKeyboardButton("Share on Twitter 𝕏",
                                       url=f'{share_string}')
    markup.row(share)
    bot.send_message("-1002130978267",
                     "\n" + f"{filtered_response}", reply_markup=markup)


def time_till_halving():
    return str(strftime('%d', localtime(halving_epoch - time.time()))).replace("-", ",") + " days"


def send_test_rewards_info():
    bot.send_message("-1002130978267",
                     f"*🟣 __Vote Bounty Info:__*\n\nVote on the trackers below, and attach a screenshot with the name of the "
                     f"tracker to instantly receive your reward\\.\n\n💸💸 Click any of the links below to get started\\! 💸💸\n\n["
                     f"DexTools](https://www\\.dextools\\.io/app/en/solana/pair-explorer"
                     f"/DDnvC5rvvZeJLuNKBF6xsdqHA6GPKbLxYq8z1bzaotUC?t=1712460479955) hit the 👍🏻 \\(100,000,000 mSatoshis\\) "
                     f"\\(Vote one time\\)\n\n[Birdeye](https://birdeye\\.so/token/mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ"
                     f"?chain=solana) hit the 👍🏻 \\(50,000,000 mSatoshis\\) \\(One time\\)\n\n[DexScreener]("
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


def send_raid_to_earn():
    bot.send_message("-1002130978267", "🟣 *__Raid to earn__*\n\n⚔️ Shill $mBTC on X to a big Crypto Twitter"
                                       " influencer ⚔️\n\nIf your post is raided, you will be tipped *10000000 "
                                       "mSatoshis*\\.\n\n_How to increase the chances of your post getting "
                                       "raided_?\n\n1\\)"
                                       "Reply to a big Crypto Twitter influencer's post that is <2 hours old\n2\\) "
                                       "Include the $mBTC ticker in your reply and tag @mbtc\\_sol\n3\\) Not AI generated "
                                       "and generic\n4\\) Account must not be shadow banned\\. Check "
                                       "here:\n[Shadowban](https://shadowban.yuzurisa.com/)\n\nYou will be tipped upon completion "
                                       "of the raid\\.",
                     parse_mode='MarkdownV2', disable_web_page_preview=True)


def send_twitter_raid_info():
    bot.send_message("-1002130978267",
                     f"*__X/Twitter__*\nWe've introduced an X bounty that can be claimed once every 5 minutes\\.\n\nSimply type "
                     f"'X' in the rewards channel, and attach the screenshot of the shill post made on X\\.\n\nYou must abide "
                     f"by the following requirements with your X post:\n🟣 You must reply to a crypto influencer with more than "
                     f"*50k followers* on a post *less* than *4hrs old*\n🟣 Use the following hashtags in your reply:\n\\$mBTC "
                     f"_\\#Bitcoin \\#BitcoinOnSolana \\#sol \\#meme \\#utility_\n🟣 X account must not be shadow banned\\. Check here:  "
                     f"[Shadowban](https://shadowban\\.yuzurisa\\.com/)\n🟣 And most importantly, please attach the recently made "
                     f"comparison chart in your shill post\\!\n\nComparison chart download: [Link]("
                     f"https://i\\.ibb\\.co/PtzJw86/Comparison\\.png)\nYou are early download: [Link]("
                     f"https://i\\.ibb\\.co/j3L7N6V/Programmed-to-send-2\\.png)\n\nYou will receive *100000000* mSatoshis on "
                     f"submission of the"
                     f"screenshot\\.",
                     parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(commands=['stats'])  # using gaht gpt 4 to generate shill text that users can use for raids
def stats(message):
    time_till_h = time_till_halving()
    supply = getlppoolinfo.get_lp_info()
    holders = str(get_holders())
    burn = get_burn_stat()
    bot.send_message("-1002130978267",  # add holder count
                     f"*__🟣 mBTC Statistics:__*\n\n⌛️ Time until halving : *{time_till_h}*\n💰 Supply left in "
                     f"the Liquidity pool: *{supply}*\n💸 Current Total Supply: *10500*\n🤲 Holder count: *{holders}*\n🔥 Total burned: *{burn}* mSats",
                     parse_mode='MarkdownV2', disable_web_page_preview=True)


def get_holders():
    holder_list = request('GET',
                          "https://pro-api.solscan.io/v1.0/token/holders?tokenAddress"
                          "=mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ&limit=10&offset=0",
                          headers=solscan_header)
    holder_list_json = holder_list.json()
    return int(holder_list_json["total"])


last_reset = 0


def determine_time_left_till_reset():
    reference_reset_leaderboard_time = 1713092400  # seed
    interval = 60 * 60 * 24 * 4  # 4 days
    current_time = time.time()
    absoloute_difference = abs(reference_reset_leaderboard_time - current_time) #time since seed
    epoch_val = int((interval - (absoloute_difference % interval)) // 3600)
    if epoch_val // 24 > 0:
        return str(int(epoch_val/24)) + " days"
    else:
        return str(epoch_val) + " hours"


def poll():  # problem with slscan glitching out idk why

    start_time = time.time()  # use this for lp pool and other stats
    start_time2 = time.time()
    start_time3 = time.time()
    start_time4 = time.time()
    time_till_h = time_till_halving()
    temp_txHash_array = []
    re_launched = True
    current_top_user = ""
    while True:
        #determine_time_left_till_reset()
        # anounce if somone changed place with another user
        if re_launched:
            current_top_user = leaderboard.get_first_place()
        else:
            temp_best = leaderboard.get_first_place()

            if temp_best != current_top_user:
                previous_best = current_top_user
                current_top_user = temp_best
                current_top_user = current_top_user.replace("_", "\\_")
                previous_best = previous_best.replace("_", "\\_")
                bot.send_message("-1002130978267",
                                 f"🥇 {current_top_user} has replaced {previous_best} as a top shiller\\!",
                                 parse_mode='MarkdownV2')
        token_address = "mBTCb8YxTdnp9GfUhz7v5qnNix7iFQCMDWKsUDNp3uJ"
        try:
            spl_transfers = request('GET',
                                    "https://pro-api.solscan.io/v1.0/token/transfer?tokenAddress=" + str(
                                        token_address) + "&limit=20&offset=0",
                                    headers=solscan_header)
            spl_transfers_json = spl_transfers.json()
        except ValueError:
            print("errored")
            continue
        for transfer in spl_transfers_json["items"]:
            if transfer["txHash"] not in temp_txHash_array:
                print("new tx")
                temp_txHash_array.append(transfer["txHash"])
                if float(transfer["amount"]) / 10 ** 11 >= 10:
                    transfer_amount = int(float(transfer["amount"]) / 10 ** 11)
                    amount_of_emojis = transfer_amount // 10
                    string_builder = ""
                    for iterator in range(0, amount_of_emojis):
                        string_builder += " 💸"
                    from_address = transfer["sourceOwnerAccount"]
                    if from_address == "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1" and not re_launched:
                        to_address = transfer["destOwnerAccount"]
                        solsca_link = "https://solscan.io/account/" + str(to_address)
                        huge = ""
                        if float(transfer["amount"]) / 10 ** 11 >= 30:
                            huge = "Mega "
                        bot.send_message("-1002130978267",
                                         f"{string_builder} {huge}Whale Buy \\! *{transfer_amount} mBTC* Transferred to ["
                                         f"Address]({solsca_link})",
                                         parse_mode='MarkdownV2', disable_web_page_preview=True)
        re_launched = False
        if time.time() > start_time + (30 * 60):
            supply = getlppoolinfo.get_lp_info()
            holders = str(get_holders())
            burn = get_burn_stat()
            bot.send_message("-1002130978267",  # add holder count
                             f"*__🟣 mBTC Statistics:__*\n\n⌛️ Time until halving : *{time_till_h}*\n💰 Supply left in "
                             f"the Liquidity pool: *{supply}*\n💸 Current Total Supply: *10500*\n🤲 Holder count: *{holders}*\n🔥 Total burned: *{burn}* mSats",
                             parse_mode='MarkdownV2', disable_web_page_preview=True)
            start_time = time.time()
        if time.time() > start_time2 + (63 * 60):
            send_test_rewards_info()
            start_time2 = time.time()
        if time.time() > start_time4 + (25 * 60):
            send_twitter_raid_info()
            start_time4 = time.time()
        if time.time() > start_time3 + (15 * 60):
            total_earned = leaderboard.get_total_awards()
            task_count = leaderboard.get_total_tasks()
            top_users = leaderboard.get_top_five()
            number_shillers = leaderboard.get_total_users()
            time_left = determine_time_left_till_reset()
            bot.send_message("-1002130978267",
                             f"🟣 *__Shill to earn Leaderboard__*\n\n{top_users}\n💰 Total earned: *{total_earned}* mSats\n📚 Total "
                             f"tasks completed: *{task_count}*\n👯 Number of shillers: *{number_shillers}*\n🕐 Time left: *{time_left}*\n\n👯 [Join rewards group]("
                             f"https://t\\.me/\\+OGXZpC7yGXQ2MDZk)",
                             parse_mode='MarkdownV2', disable_web_page_preview=True)
            start_time3 = time.time()
        time.sleep(5)


if __name__ == "__main__":
    t1 = threading.Thread(target=poll)
    t1.start()
    # generate_meme_batch()
    bot.infinity_polling(timeout=None)
