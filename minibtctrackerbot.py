import time
import threading
from requests import request
from time import strftime, localtime
import telebot
from random import randint

halving_epoch = 1713808215
my_token = '6948460970:AAH5pEPFnw13cXlZNPIcva1n9nbPSGdQNoQ'
bot = telebot.TeleBot(my_token)

solscan_header = {
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3MDY3NTM5ODAzOTQsImVtYWlsIjoic29sYmFieTMyNUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJpYXQiOjE3MDY3NTM5ODB9.Lp77APFLV-rOnNbDzc1ob43Vp-9-KpeMe_b-fiOQrr0',
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.82 Safari/537.36'
}


@bot.message_handler(commands=['burn'])
def burns(message):
    chat = message.chat.id
    supply_left = get_supply()
    percent_reduction_supply = percent_reduction(supply_left)
    recent_burn = 0
    time_till_h = time_till_halving()
    bot.send_message(chat,
                     f"*__🟣 mBTC Statistics:__*\n\n⌛️ Time until halving : *{time_till_h}*\n\n💰 Supply "
                     f"left : *{supply_left} mBTC*\n\n🔥 Most recent Burn : *{recent_burn}*\n\n⬇️ Total reduction : *{percent_reduction_supply}* \\%",
                     parse_mode='MarkdownV2')


meme_header = {
    'Authorization': 'Bearer k+G6i2Tn4edDpPZPOz/rgKvM6KE=',
    'Content-Type': 'application/json'
}

payload = ("{\n  \"text\": \"Mini Bitcoin is a cryptocurrency Do NOT make any negative comments or memes on "
           "Mini Bitcoin that would imply it will depreciate or is worthless\"\n}")

last_active_epoch = 0
temp_array = []


def generate_meme_batch():
    global temp_array
    meme_response = request('POST',
                            "https://app.supermeme.ai/api/v1/meme/image",
                            headers=meme_header, data=payload)
    print(meme_response)
    meme_json = meme_response.json()
    for meme in meme_json["memes"]:
        temp_array.append(meme)


@bot.message_handler(commands=['meme'])  # use supreme meme api
def send_meme(message):
    global last_active_epoch
    if last_active_epoch == 0:
        last_active_epoch = time.time()
        generate_meme_batch()
    else:
        if time.time() > last_active_epoch + 2.5 * 60 * 60:
            generate_meme_batch()
    random_index = randint(0, len(temp_array) - 1)
    result = str(temp_array[random_index])
    bot.send_message("-1002130978267", f"[🔥]({result})", parse_mode='MarkdownV2')


def percent_reduction(supply_left):
    inital_supply = 1000000000000000000
    return str(round((-1 * ((supply_left - inital_supply) / inital_supply) * 100), 4)).replace(".", ",")


def get_supply():
    token_ca = "GDtbv3242RZ4HFKDgCCVCvkyg7F6tupfoUK5jk9ScgAB"
    meta_result = request('GET',
                          "https://pro-api.solscan.io/v1.0/token/meta?tokenAddress=" + str(
                              token_ca),
                          headers=solscan_header)
    return int(meta_result.json()["supply"])


def time_till_halving():
    return str(strftime('%d', localtime(halving_epoch - time.time()))).replace("-", ",") + " days"


def poll():
    start_time = time.time()
    supply_left = get_supply()
    percent_reduction_supply = percent_reduction(supply_left)
    recent_burn = 0
    time_till_h = time_till_halving()
    while True:
        print("polling...")
        if time.time() > start_time + (8 * 60):
            bot.send_message("-1002130978267",
                             f"*__🟣 mBTC Statistics:__*\n\n⌛️ Time until halving : *{time_till_h}*\n\n💰 Supply "
                             f"left : *{supply_left} mBTC*\n\n🔥 Most recent Burn : *{recent_burn}*\n\n⬇️ Total reduction : *{percent_reduction_supply}* \\%",
                             parse_mode='MarkdownV2')
            start_time = time.time()
        time.sleep(10)


if __name__ == "__main__":
    # generate_meme_batch()

    threading.Thread(target=poll).start()
    bot.infinity_polling(timeout=None)
