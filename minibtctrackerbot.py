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

# Enter your Assistant ID here.
ASSISTANT_ID = "asst_OdboRIxKhLQrirwYRHZFhyZd"

# Make sure your API key is set as an environment variable.
client = OpenAI(api_key="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")
halving_epoch = 1713808215  # check again if this is accurate
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
        fetch_cloud_img_links()
    if time.time() > last_active_epoch + 2.5 * 60 * 60:
        th = threading.Thread(target=generate_meme_batch)
        th.start()
        last_active_epoch = time.time()
        fetch_cloud_img_links()
    random_index = randint(0, len(temp_array) - 1)
    result = str(temp_array[random_index])
    markup = types.InlineKeyboardMarkup()
    share_string = f"https://twitter.com/intent/tweet?text=$mBTC%20"  # needs slight change
    share = types.InlineKeyboardButton("Share on Twitter 𝕏",
                                       url=f'{share_string}')
    markup.row(share)
    bot.send_message("-1002130978267", f"[🔥]({result}) To share an image simply download and attach it to your post\\.", parse_mode='MarkdownV2', reply_markup=markup)


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
                     "\n"+f"{filtered_response}",reply_markup=markup)


def time_till_halving():
    return str(strftime('%d', localtime(halving_epoch - time.time()))).replace("-", ",") + " days"


def poll():
    start_time = time.time()
    time_till_h = time_till_halving()
    while True:
        print("polling...")
        if time.time() > start_time + (30 * 60):
            bot.send_message("-1002130978267",
                             f"*__🟣 mBTC Statistics:__*\n\n⌛️ Time until halving : *{time_till_h}*",
                             parse_mode='MarkdownV2')
            start_time = time.time()
        time.sleep(10)


if __name__ == "__main__":
    # generate_meme_batch()
    bot.infinity_polling(timeout=None)
