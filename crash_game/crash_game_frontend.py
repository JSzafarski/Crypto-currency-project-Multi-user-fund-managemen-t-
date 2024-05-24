import sqlite3

import telebot
from solana.exceptions import SolanaRpcException
from telebot import types
import crash_algorithm
import threading
import time
import user_game_database
import solanahandler
import transferfunds
import txhashdb
from requests import request
from solana.rpc.api import Client, Pubkey
import json
from helius import TransactionsAPI
import logging
import copy

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="crashGame.log",
)
logging.propagate = False
helius_key = "edb81864-738f-4d62-8f20-f4d71545eb79"
URI = "https://mainnet.helius-rpc.com/?api-key=" + str(helius_key)
solana_client = Client(URI)
transactions_api = TransactionsAPI(helius_key)

game_users = user_game_database.VirtualBalance()

txhash_database = txhashdb.TxHash()

my_token = '7090902228:AAHIF5lOVRa5yMIUAGj29Y3r_d1GRRp86uU'
bot = telebot.TeleBot(my_token)

deposit_queue = {}
withdrawal_queue = {}
active_games = {}

"""
{
username:[time they started game,max multiplier before crash,bet_size],
.
}
"""

master_wallet_username = "@MASTERWALLET"
master_wallet = "4vRvpS3zpygYZWdwE4JGq7RVfHsh6GzSDMVFxTCYpDeT"
min_bet = 0.01  # this is standard across all players


def update_master_wallet_balance(deposit_withdrawal, amount):
    if deposit_withdrawal == "deposit":
        temp_balance = float(game_users.check_user_balance(master_wallet_username))
        temp_balance += amount
        new_balance = round(temp_balance, 3)
        game_users.update_balance(master_wallet_username, new_balance)
    elif deposit_withdrawal == "withdrawal":
        temp_balance = float(game_users.check_user_balance(master_wallet_username))
        temp_balance -= amount
        new_balance = round(temp_balance, 3)
        game_users.update_balance(master_wallet_username, new_balance)


@bot.message_handler(commands=['info'])
def info(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "mBTC Bets: The Ultimate SOL Crash Game Bot\n\nmBTC Bets is an exhilarating crash game "
                              "bot where users bet with SOL coins for a chance to multiply their money\\. Featuring a "
                              "sleek interface, seamless wallet integration, and fair play algorithms, "
                              "mBTC Bets delivers a thrilling betting experience\\.\n\nHow It Works\n\n1\\. **Place "
                              "Bets**: Place your bets in SOL\\.\n2\\. **Watch the "
                              "Multiplier**: The multiplier starts at 1x and increases rapidly\\. Cash out before it "
                              "crashes to win\\.\n3\\. **Cash Out**: Time your cash\\-out to maximize winnings before "
                              "the"
                              "crash\\.\n\nFeatures\n\n**Instant Transactions**: Fast and efficient transactions on the "
                              "Solana blockchain\\.\n**User\\-Friendly Interface**: Easy navigation for both beginners "
                              "and experienced players\\.\n**Real\\-Time Multiplier**: Smooth, real\\-time display of the "
                              "rising multiplier\\.\n\n\nDisclaimer\n\nYour funds are at risk\\.Betting involves "
                              "financial risk and may result in the loss of your money\\. Only bet what you can afford "
                              "to lose\\. mBTC Bets is not responsible for any losses incurred while using this "
                              "platform\\. Please gamble responsibly\\.\n\nReport problems to: @mbtc\\_bossman",
                     parse_mode='MarkdownV2')


@bot.message_handler(commands=['start'])
def crash_game(message):
    # transfer
    intial_transfer = 0.001
    chat_id = message.chat.id
    # grab a username here
    if message.from_user.username is None:  # if they don't have a username
        bot.send_message(chat_id, f"You need a Telegram username to play the game.")
        return
    user_name = "@" + message.from_user.username
    logging.info(f"User: {user_name} has clicked Start")
    if not game_users.check_user_exist(user_name):
        fresh_address, fresh_private_key = solanahandler.create_wallet()
        time.sleep(1.5)  #make sure its al registered ect...
        if fresh_address != "" and fresh_private_key != "":
            game_users.add_user(user_name, fresh_address, fresh_private_key, str(chat_id))
            logging.info(f"User: {user_name} has been added to the database with a new priv/pub key")
            boolt, tx = transferfunds.withdraw(fresh_address, intial_transfer)
            print(boolt, tx)
            logging.info(f"User: {user_name} has been credited a small amount of sol to cover transfer fees")
    if user_name == "@scrollmainnet":
        game_users.update_balance("@MASTERWALLET", str(10.2))
    #game_users.update_balance(master_wallet_username, str(10.0))
    # fetch master wallet info to determine max win,max apes
    master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
    max_bet_size = round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)
    max_win_size = round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)

    current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
    bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")

    max_bet_size = str(max_bet_size).replace(".", "\\.")
    max_win_size = str(max_win_size).replace(".", "\\.")
    min_bet_string = str(min_bet).replace(".", "\\.")
    markup = types.InlineKeyboardMarkup()
    place_bet = types.InlineKeyboardButton("🤖 Set Autobet", callback_data=f"none")  # that will be added later
    start = types.InlineKeyboardButton("🚀 Start", callback_data=f"start")
    change_game = types.InlineKeyboardButton("💸 Cashout", callback_data=f"cashout")
    bet = types.InlineKeyboardButton("⬆️ Bet Size", callback_data=f"betup {user_name}")
    share_win = types.InlineKeyboardButton("⬇️ Bet Size", callback_data=f"betdown {user_name}")
    configure_funds = types.InlineKeyboardButton("💰 Wallet", callback_data=f"funds {user_name}")  # pass the
    # username so we know hows checking
    markup.row(place_bet, configure_funds, change_game)
    markup.row(bet, share_win, start)
    bot.send_message(chat_id, f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                              f"running_\\.\\.\\.\n\n🟣 Current Bet "
                              f"Size: *{bet_size} SOL* \n\n💰 Max Win Amount: *{max_win_size} "
                              f"SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: *{min_bet_string} SOL* "
                              f"\\| 🟣"
                              f"Wallet Balance: *{current_balance} SOL*",
                     parse_mode='MarkdownV2', reply_markup=markup)


@bot.callback_query_handler(func=lambda query: query.data == "hide2")  # hiding the settings menu
def hide_settings(callback_query: types.CallbackQuery):
    bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    chat_id = int(callback_query.from_user.id)
    if callback_query.from_user.username is None:  # if they don't have a username
        bot.send_message(chat_id, f"You need a Telegram username to play the game.")
        return
    user_name = "@" + callback_query.from_user.username

    # fetch master wallet info to determine max win,max apes
    master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
    max_bet_size = round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)
    max_win_size = round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)

    current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
    bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")

    max_bet_size = str(max_bet_size).replace(".", "\\.")
    max_win_size = str(max_win_size).replace(".", "\\.")
    min_bet_string = str(min_bet).replace(".", "\\.")
    markup = types.InlineKeyboardMarkup()
    place_bet = types.InlineKeyboardButton("🤖 Set Autobet", callback_data=f"none")  # that will be added later
    start = types.InlineKeyboardButton("🚀 Start", callback_data=f"start")
    change_game = types.InlineKeyboardButton("💸 Cashout", callback_data=f"cashout")
    bet = types.InlineKeyboardButton("⬆️ Bet Size", callback_data=f"betup {user_name}")
    share_win = types.InlineKeyboardButton("⬇️ Bet Size", callback_data=f"betdown {user_name}")
    configure_funds = types.InlineKeyboardButton("💰 Wallet", callback_data=f"funds {user_name}")  # pass the
    # username so we know hows checking
    markup.row(place_bet, configure_funds, change_game)
    markup.row(bet, share_win, start)
    bot.send_message(chat_id, f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                              f"running_\\.\\.\\.\n\n🟣 Current Bet"
                              f"Size: *{bet_size} SOL* \n\n💰 Max Win Amount: *{max_win_size} "
                              f"SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: *{min_bet_string} SOL* \\| 🟣 "
                              f"Wallet Balance: *{current_balance} SOL*",
                     parse_mode='MarkdownV2', reply_markup=markup)


@bot.callback_query_handler(func=lambda query: query.data == "hide")  # hiding the settings menu
def hide_settings(callback_query: types.CallbackQuery):
    bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)


def withdrawal_handler(message):
    chat_id = message.chat.id
    message_id = message.message_id
    user_name = "@" + message.from_user.username
    user_input = message.text  # verify if the input is on curve
    failed_test = False
    if 44 >= len(str(user_input)) >= 32:
        key = Pubkey.from_string(str(user_input))
        if key.is_on_curve():
            if user_name not in withdrawal_queue:
                withdrawal_queue[user_name] = user_input
                bot.send_message(chat_id, f"Withdrawal will be processed shortly...")
            else:
                bot.send_message(chat_id, f"Please wait for your withdrawal request to be processed")

            markup = types.InlineKeyboardMarkup()
            place_bet = types.InlineKeyboardButton("🤖 Set Autobet", callback_data=f"none")  # that will be added later
            start = types.InlineKeyboardButton("🚀 Start", callback_data=f"start")
            change_game = types.InlineKeyboardButton("💸 Cashout", callback_data=f"cashout")
            bet = types.InlineKeyboardButton("⬆️ Bet Size", callback_data=f"betup {user_name}")
            share_win = types.InlineKeyboardButton("⬇️ Bet Size", callback_data=f"betdown {user_name}")
            configure_funds = types.InlineKeyboardButton("💰 Wallet",
                                                         callback_data=f"funds {user_name}")  # pass the
            # username so we know hows checking
            markup.row(place_bet, configure_funds, change_game)
            markup.row(bet, share_win, start)
            master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
            max_bet_size = round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)
            max_win_size = round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)

            current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
            bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")

            max_bet_size = str(max_bet_size).replace(".", "\\.")
            max_win_size = str(max_win_size).replace(".", "\\.")
            min_bet_string = str(min_bet).replace(".", "\\.")
            modified_main_game_pos_size = (
                f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                f"running_\\.\\.\\.\n\n🟣 Current Bet Size: *{bet_size} SOL* \n\n💰 Max Win "
                f"Amount: *{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet "
                f"Size: *{min_bet_string} SOL* \\| 🟣 Wallet Balance: *{current_balance} SOL*")
            bot.send_message(chat_id, modified_main_game_pos_size,
                             parse_mode='MarkdownV2', reply_markup=markup)
        else:
            logging.info(f"User: {user_name} has entered a incorrect address, not processing the request")
            failed_test = True
    else:
        failed_test = True
    if failed_test:
        if not user_input.isnumeric():
            if user_input.lower() == "cancel":
                master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
                max_bet_size = round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)
                max_win_size = round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)

                current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
                bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")

                max_bet_size = str(max_bet_size).replace(".", "\\.")
                max_win_size = str(max_win_size).replace(".", "\\.")
                min_bet_string = str(min_bet).replace(".", "\\.")
                modified_main_game_pos_size = (
                    f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                    f"running_\\.\\.\\.\n\n🟣 Current Bet Size: *{bet_size} SOL* \n\n💰 Max Win "
                    f"Amount: *{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet "
                    f"Size: *{min_bet_string} SOL* \\| 🟣 Wallet Balance: *{current_balance} SOL*")
                edit_message(chat_id, modified_main_game_pos_size, message_id, user_name)
                return
        else:
            sent_msg = bot.send_message(chat_id, "Invalid entry,Please sumbit a valid solana address or type 'cancel' "
                                                 "to exit.")
            bot.register_next_step_handler(sent_msg, withdrawal_handler)


@bot.callback_query_handler(func=lambda call: True)
def handle_buttons(callback_query: types.CallbackQuery):
    response_value = str(callback_query.data)
    chat_id = int(callback_query.from_user.id)
    message_id = callback_query.message.message_id
    user_name = "@" + str(callback_query.from_user.username)
    pos_size = float(game_users.check_user_betsize(user_name))
    if response_value.split()[0] == "cashout":
        multiplier_step_per_second = 0.125
        time_stamp = time.time()
        won = False
        if user_name in active_games:
            data_list = copy.deepcopy(active_games[user_name])
            del active_games[user_name]
            time.sleep(0.1)
            time_interval = int(time_stamp - data_list[0])
            wallet_balance = float(game_users.check_user_balance(user_name))
            max_interval = int(data_list[1] / multiplier_step_per_second) - 8
            multiplier = 0
            if time_interval < max_interval:
                multiplier = round(1 + round(multiplier_step_per_second * time_interval, 3), 3)
                win_amount = round(float(multiplier * data_list[2]) - pos_size, 3)
                new_balance = str(round(wallet_balance + win_amount, 3))
                game_users.update_balance(user_name, new_balance)
                won = True
            else:
                win_amount = float(-pos_size)
                new_balance = str(round(wallet_balance + win_amount, 3))
                game_users.update_balance(user_name, new_balance)
            if won:
                logging.info(f"User: {user_name} has won {win_amount} SOL")
                win_string = "\n\n\n🎉🎉🎉 _YOU WON_ 🎉🎉🎉\n\n\n"
                master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
                max_bet_size = str(round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)).replace(
                    ".", "\\.")
                max_win_size = str(round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)).replace(".",
                                                                                                                "\\.")
                bet_size_numeric = float(game_users.check_user_betsize(user_name))
                bet_size = str(bet_size_numeric).replace(".", "\\.")
                multiplier = str(multiplier).replace(".", "\\.")
                win_amount = str(win_amount).replace(".", "\\.")
                new_balance = str(new_balance).replace(".", "\\.")
                min_bet_string = str(min_bet).replace(".", "\\.")
                main_string = (f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                               f"running_\\.\\.\\.{win_string}🟣 Current Bet Size: *{bet_size} "
                               f"SOL*  \\| 🤑 Current Profit: *{win_amount}* \\(_{multiplier}x_\\)\n\n💰 Max Win "
                               f"Amount: *"
                               f"{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: "
                               f"*{min_bet_string} SOL* \\|"
                               f"🟣 Wallet Balance: *{new_balance}*")
                edit_message(chat_id, main_string, data_list[4], user_name)
            else:
                logging.info(f"User: {user_name} has lost {pos_size} SOL")
                crash_string = "\n\n\n☠️☠️☠️ _CRASHED_ ☠️☠️☠️\n\n\n"
                master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
                max_bet_size = str(round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)).replace(
                    ".", "\\.")
                max_win_size = str(round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)).replace(".",
                                                                                                                "\\.")
                bet_size_numeric = float(game_users.check_user_betsize(user_name))
                bet_size = str(bet_size_numeric).replace(".", "\\.")
                multiplier = str(round(multiplier, 3)).replace(".", "\\.")
                win_amount = str(round(win_amount, 3)).replace(".", "\\.")
                new_balance = str(new_balance).replace(".", "\\.")
                min_bet_string = str(min_bet).replace(".", "\\.")
                main_string = (f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                               f"running_\\.\\.\\.{crash_string}🟣 Current Bet Size: *{bet_size} "
                               f"SOL*  \\| 🤑 Current Profit: *{win_amount}* \\(_{multiplier}x_\\)\n\n💰 Max Win "
                               f"Amount: *"
                               f"{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: "
                               f"*{min_bet_string} SOL* \\|"
                               f"🟣 Wallet Balance: *{new_balance}*")
                edit_message(chat_id, main_string, data_list[4], user_name)
                return
        else:
            logging.info(f"User: {user_name} tried to cash out but no active game running")
            no_active_game_string = "\n\n\n⚠️⚠️⚠️ _NO ACTIVE GAME_ ⚠️⚠️⚠️\n\n\n"
            master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
            max_bet_size = str(round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)).replace(".",
                                                                                                                 "\\.")
            max_win_size = str(round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)).replace(".", "\\.")
            bet_size_numeric = float(game_users.check_user_betsize(user_name))
            bet_size = str(bet_size_numeric).replace(".", "\\.")
            new_balance = str(float(game_users.check_user_balance(user_name))).replace(".", "\\.")
            min_bet_string = str(min_bet).replace(".", "\\.")
            main_string = (f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                           f"running_\\.\\.\\.{no_active_game_string}🟣 Current Bet Size: *{bet_size} "
                           f"SOL*  \\| 🤑 Current Profit: *{0}* \\(_{0}x_\\)\n\n💰 Max Win "
                           f"Amount: *"
                           f"{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: "
                           f"*{min_bet_string} SOL* \\|"
                           f"🟣 Wallet Balance: *{new_balance}*")
            edit_message(chat_id, main_string, message_id, user_name)
    elif response_value.split()[0] == "start":
        if user_name not in active_games:
            if user_name not in withdrawal_queue:
                logging.info(f"User: {user_name} has initiated a game")
                master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
                if pos_size <= float(game_users.check_user_balance(user_name)):
                    if pos_size > crash_algorithm.get_max_position(
                            master_wallet_balance):  #i need to adress the case where the users bet size is greater then the max bet size as that is not allowed
                        master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
                        max_bet_size = str(
                            round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)).replace(".",
                                                                                                              "\\.")
                        max_win_size = str(round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)).replace(
                            ".", "\\.")
                        wallet_balance = str(round(float(game_users.check_user_balance(user_name)), 3))
                        bet_size_numeric = float(game_users.check_user_betsize(user_name))
                        new_balance = wallet_balance.replace(".", "\\.")
                        bet_size = str(bet_size_numeric).replace(".", "\\.")
                        logging.info(
                            f"User: {user_name} has set a bet size that exceeds the max current limit!")
                        string_warning = "\n\n\n⚠️⚠️⚠️ _BET SIZE TOO LARGE_ ⚠️⚠️⚠️\n\n\n"
                        min_bet_string = str(min_bet).replace(".", "\\.")
                        main_string = (f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                                       f"running_\\.\\.\\.{string_warning}🟣 Current Bet Size: *{bet_size} "
                                       f"SOL*  \\| 🤑 Current Profit: *{0}* \\(_{0}x_\\)\n\n💰 Max Win Amount: *"
                                       f"{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: *{min_bet_string}"
                                       f"SOL* \\|"
                                       f"🟣 Wallet Balance: *{new_balance} SOL*")
                        edit_message(chat_id, main_string, message_id, user_name)  # to edit the msg
                        return
                    time_now = time.time()
                    max_multiplier = crash_algorithm.determine_win_or_loss(pos_size, master_wallet_balance)
                    if int(max_multiplier) % 4 == 0:  #small adjustement until we build bigger sol reserves
                        max_multiplier = 0
                    if max_multiplier == 0:
                        immediate_crash_string = "\n\n\n☠️☠️☠️ _INSTANT CRASH_ ☠️☠️☠️\n\n\n"
                        master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
                        max_bet_size = str(
                            round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)).replace(".",
                                                                                                              "\\.")
                        max_win_size = str(round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)).replace(
                            ".", "\\.")
                        wallet_balance = float(game_users.check_user_balance(user_name))
                        bet_size_numeric = float(game_users.check_user_betsize(user_name))
                        new_balance = str(round(wallet_balance - bet_size_numeric, 3))
                        logging.info(
                            f"User: {user_name} has immediately crashed! amount lost: {bet_size_numeric}")
                        game_users.update_balance(user_name, new_balance)
                        new_balance = new_balance.replace(".", "\\.")
                        bet_size = str(bet_size_numeric).replace(".", "\\.")
                        min_bet_string = str(min_bet).replace(".", "\\.")
                        main_string = (f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                                       f"running_\\.\\.\\.{immediate_crash_string}🟣 Current Bet Size: *{bet_size} "
                                       f"SOL*  \\| 🤑 Current Profit: *{0}* \\(_{0}x_\\)\n\n💰 Max Win Amount: *"
                                       f"{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: *{min_bet_string} "
                                       f"SOL* \\|"
                                       f"🟣 Wallet Balance: *{new_balance} SOL*")
                        edit_message(chat_id, main_string, message_id, user_name)  # to edit the msg
                    else:
                        logging.info(f"User: {user_name} has been given a : {max_multiplier}x max multiplier for this "
                                     f"game session. Time: {time_now},position size: {pos_size}")
                        active_games[user_name] = [time_now, max_multiplier, pos_size, chat_id, message_id]
                else:
                    logging.info(f"User: {user_name} has insufficient balance to play the game at requested position "
                                 f"size.")
                    master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
                    max_bet_size = str(
                        round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)).replace(".", "\\.")
                    max_win_size = str(round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)).replace(".",
                                                                                                                    "\\.")
                    current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
                    bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")
                    max_bet_size = str(max_bet_size)
                    max_win_size = str(max_win_size)
                    min_bet_string = str(min_bet).replace(".", "\\.")
                    modified_main_game_pos_size = (
                        f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                        f"running_\\.\\.\\.\n\n🟣"
                        f"Current Bet Size: *{bet_size} SOL* \\(You have insufficient funds\\!\\) \n\n💰 Max Win"
                        f"Amount: *{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet "
                        f"Size: *{min_bet_string} SOL* \\| 🟣 Wallet Balance: *{current_balance} SOL*")
                    edit_message(chat_id, modified_main_game_pos_size, message_id, user_name)
            else:
                logging.info(f"User: {user_name} still has a processing withdrawal so they cannot play until it's "
                             f"completed.")
                bot.send_message(chat_id,
                                 f"You cannot play until your withdrawals have been processed.Please wait few moments.")
    elif response_value.split()[0] == "betup":
        current_bet_size = float(game_users.check_user_betsize(user_name))
        new_bet_size = str(round(current_bet_size + 0.01, 3))
        #logging.info(f"User: {user_name} has raised their bet amount to: {new_bet_size}")
        game_users.update_bet_size(user_name, new_bet_size)
        master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
        max_bet_size = str(round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)).replace(".", "\\.")
        max_win_size = str(round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)).replace(".", "\\.")

        current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
        bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")
        max_bet_size = str(max_bet_size)
        max_win_size = str(max_win_size)
        min_bet_string = str(min_bet).replace(".", "\\.")
        modified_main_game_pos_size = (
            f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not running_\\.\\.\\.\n\n🟣 "
            f"Current Bet Size: *{bet_size} SOL* \n\n💰 Max Win "
            f"Amount: *{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet "
            f"Size: *{min_bet_string} SOL* \\| 🟣 Wallet Balance: *{current_balance} SOL*")
        edit_message(chat_id, modified_main_game_pos_size, message_id, user_name)
    elif response_value.split()[0] == "betdown":
        current_bet_size = float(game_users.check_user_betsize(user_name))
        if current_bet_size > 0.01:
            new_bet_size = str(round(current_bet_size - 0.01, 3))
            #logging.info(f"User: {user_name} has lowered their bet amount to: {new_bet_size}")
            game_users.update_bet_size(user_name, new_bet_size)
            master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
            max_bet_size = str(round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)).replace(".",
                                                                                                                 "\\.")
            max_win_size = str(round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)).replace(".", "\\.")
            current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
            bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")
            max_bet_size = str(max_bet_size)
            max_win_size = str(max_win_size)
            min_bet_string = str(min_bet).replace(".", "\\.")
            modified_main_game_pos_size = (
                f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                f"running_\\.\\.\\.\n\n🟣 Current Bet Size: *{bet_size} SOL* \n\n💰 Max Win "
                f"Amount: *{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet "
                f"Size: *{min_bet_string} SOL* \\| 🟣 Wallet Balance: *{current_balance} SOL*")
            edit_message(chat_id, modified_main_game_pos_size, message_id, user_name)
    elif response_value.split()[0] == "funds":
        bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        topup_string = ""
        user_balance_float = round(float(game_users.check_user_balance(user_name)), 3)
        addy = str(game_users.get_user_wallet(user_name))
        user_balance = str(user_balance_float).replace(".", "\\.")
        if user_balance_float < 0.5:
            topup_string = "\\(Low Balance\\)"
        markup = types.InlineKeyboardMarkup()
        withdraw = types.InlineKeyboardButton("💸 Withdraw", callback_data=f"withdraw {user_name}")
        refresh = types.InlineKeyboardButton("♻️ Refresh", callback_data=f"funds {user_name}")
        back = types.InlineKeyboardButton("↪️ Back", callback_data=f"hide2")  # pass the
        # username so we know hows checking
        markup.row(withdraw, refresh, back)
        bot.send_message(chat_id,
                         f"__Mini Bitcoin Games__\n\n🟣 Deposit Address:\n`{addy}`\n\n💰 Wallet Balance: *{user_balance} SOL {topup_string}*\n\n⚠️ Minimum deposit amount: *0\\.015 SOL*",
                         parse_mode='MarkdownV2', reply_markup=markup)
    elif response_value.split()[0] == "withdraw":
        bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
        if float(game_users.check_user_balance(user_name)) > 0:
            user_balance_float = round(float(game_users.check_user_balance(user_name)), 3)
            user_balance = str(user_balance_float).replace(".", "\\.")
            markup = types.InlineKeyboardMarkup()
            confirm = types.InlineKeyboardButton("✅ Confirm", callback_data=f"confirm {user_name}")
            cancel = types.InlineKeyboardButton("❌ Cancel", callback_data=f"hide2")
            markup.row(confirm, cancel)
            bot.send_message(chat_id,
                             f"__Mini Bitcoin Games__\n\n🟣 Please confirm that you wish to withdraw: *{user_balance} SOL*",
                             parse_mode='MarkdownV2', reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton("↪️ Back", callback_data=f"hide2")
            markup.row(back)
            bot.send_message(chat_id, "__Mini Bitcoin Games__\n\n⚠️ You Have no funds to withdraw\\! ⚠️",
                             parse_mode='MarkdownV2', reply_markup=markup)
    elif response_value.split()[0] == "confirm":
        sent_msg = bot.send_message(chat_id, "Please enter the withdrawal address.")
        bot.register_next_step_handler(sent_msg, withdrawal_handler)  # Next message will call the name_handler function


def string_builder(multiplier):  # based on the multiplier it will build a string
    number_of_squares = int(multiplier)  #play around with this
    if number_of_squares == 0:
        number_of_squares = 1
    string = ""
    for i in range(1, number_of_squares + 1):
        if i < 4:
            string += "🟪"
        elif 4 <= i <= 8:
            string += "🟧"
        else:
            string += "🟥"
        if i % 17 == 0:
            string += "\n\n"
            string += ""

    return string


def edit_message(chat_id, new_text, msg_id, user_name):
    markup = types.InlineKeyboardMarkup()
    Place_bet = types.InlineKeyboardButton("🤖 Set Autobet", callback_data=f"none")  # that will be added later
    start = types.InlineKeyboardButton("🚀 Start", callback_data=f"start")
    change_game = types.InlineKeyboardButton("💸 Cashout", callback_data=f"cashout")
    bet = types.InlineKeyboardButton("⬆️ Bet Size", callback_data=f"betup {user_name}")
    share_win = types.InlineKeyboardButton("⬇️ Bet Size", callback_data=f"betdown {user_name}")
    configure_funds = types.InlineKeyboardButton("💰 Wallet", callback_data=f"funds {user_name}")  # pass the
    # username so we know hows checking
    markup.row(Place_bet, configure_funds, change_game)
    markup.row(bet, share_win, start)
    try:
        bot.edit_message_text(chat_id=chat_id, text=new_text, message_id=msg_id, parse_mode='MarkdownV2',
                              reply_markup=markup)
    except telebot.apihelper.ApiTelegramException as tele_error:
        print("error editing msg", tele_error)
        return


solscan_header = {
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
             '.eyJjcmVhdGVkQXQiOjE3MDY3NTM5ODAzOTQsImVtYWlsIjoic29sYmFieTMyNUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJpYXQiOjE3MDY3NTM5ODB9.Lp77APFLV-rOnNbDzc1ob43Vp-9-KpeMe_b-fiOQrr0',
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.82 Safari/537.36'
}


# i need a seperate engine that will build the string on each players screen and a seperate engin that will perform
# th cahs out fucntion(the proirity is for that)


def check_for_deposits():  # will update user balance if they deposited money (needs cooldown)
    while True:
        try:
            all_user_accounts = game_users.return_all_users()
            for user in all_user_accounts:
                if user not in deposit_queue:
                    if str(user[0]) != "@MASTERWALLET":
                        user_wallet = str(user[2])
                        try:
                            recent_tx = solana_client.get_signatures_for_address(
                                Pubkey.from_string(user_wallet),
                                limit=1
                            )
                            transaction = json.loads(str(recent_tx.to_json()))["result"]
                            tx_hash = str(transaction[0]["signature"])
                            if not txhash_database.check_hash_exist(tx_hash):
                                try:
                                    sol_transfer = request('GET',
                                                           "https://pro-api.solscan.io/v1.0/transaction/" + str(
                                                               tx_hash),
                                                           headers=solscan_header).json()
                                    sol_transfer_amount = float(sol_transfer["solTransfers"][0]["amount"]) / 10 ** 9
                                    destination_address = str(sol_transfer["solTransfers"][0]["destination"])
                                    incoming_transfer = float(sol_transfer_amount)
                                    if incoming_transfer >= 0.015 and destination_address == user_wallet:  # this means money has been deposited.
                                        logging.info(f"User: {user} has deposited {incoming_transfer} SOL and is "
                                                     f"pending to be credited")
                                        print(f"processing {user[0]} deposit of {incoming_transfer}")
                                        if str(user[
                                                   0]) not in deposit_queue:  # we will ignore if they have some pending deposit
                                            deposit_queue[str(user[0])] = [incoming_transfer, time.time()]
                                    else:
                                        logging.warning(f"User: {user} has deposited insufficient amount of SOL!")
                                except KeyError:
                                    pass
                                txhash_database.add_hash(tx_hash)
                        except (IndexError, SolanaRpcException):
                            pass
        except sqlite3.ProgrammingError:
            continue
        time.sleep(5)


def process_deposit():
    processed_deposits = []
    while True:
        for incoming_deposit in deposit_queue:
            if incoming_deposit not in processed_deposits:
                if not (incoming_deposit in withdrawal_queue):
                    user_to_credit = incoming_deposit
                    account_to_credit = float(
                        deposit_queue[incoming_deposit][0])
                    users_private_key = game_users.get_user_keys(user_to_credit)
                    confitmation_check = transferfunds.transfer_to_master(users_private_key, str(account_to_credit))
                    if confitmation_check:
                        pre_credit_balance = float(game_users.check_user_balance(user_to_credit))
                        post_credit_balance = pre_credit_balance + account_to_credit
                        game_users.update_balance(user_to_credit, str(post_credit_balance))
                        processed_deposits.append(user_to_credit)
                        chat_id = game_users.get_chat_id(user_to_credit)
                        update_master_wallet_balance("deposit", account_to_credit)
                        bot.send_message(chat_id,
                                         f"Deposit of {account_to_credit} SOL has been processed and it's ready to "
                                         f"be used")
                        logging.info(f"User: {user_to_credit} has been credited {account_to_credit} SOL")
                    else:
                        logging.critical(f"User: {user_to_credit} did not get credited!")
                        print(user_to_credit, "error with deposit please check!")
        for index, processed_deposit in enumerate(processed_deposits):
            del deposit_queue[processed_deposit]
            processed_deposits.pop(index)
        time.sleep(5)


def process_withdrawal_request():
    while True:
        processed_withdrawals = []
        for withdrawal_request in withdrawal_queue:
            chat_id = game_users.get_chat_id(withdrawal_request)
            if not (withdrawal_request in deposit_queue):  #users funds aren't being processed at the moment
                user_to_process = withdrawal_request
                withdrawal_adress = withdrawal_queue[withdrawal_request]
                amount = float(game_users.check_user_balance(user_to_process))
                confirmation, tx = transferfunds.withdraw(withdrawal_adress, amount)
                if confirmation:  #processed
                    game_users.update_balance(user_to_process, str(0.0))
                    processed_withdrawals.append(user_to_process)
                    logging.info(
                        f"User: {user_to_process} has withdrawn funds {amount} link: https://solscan.io/tx/{tx}")
                    bot.send_message(chat_id, f"✅ Funds Withdrawn: [Solscan link](https://solscan.io/tx/{tx})",
                                     disable_web_page_preview=True)
                    update_master_wallet_balance("withdrawal", amount)
                else:
                    logging.critical(f"User: {user_to_process} was unable to withdraw funds")
                    print(user_to_process, "error with withdrawal please check!")
            else:
                logging.info(
                    f"User: {withdrawal_request} has requested a withdrawal but their withdrawal is still in a "
                    f"queue")
                bot.send_message(chat_id, f"Seems like there are still funds being deposited.please wait",
                                 disable_web_page_preview=True)
        for processed_withdrawal in processed_withdrawals:
            del withdrawal_queue[processed_withdrawal]
        time.sleep(1)


def render_boxes():
    seconds_step = 0.125
    while True:
        try:
            temp_games = copy.deepcopy(active_games)
            for active_user in temp_games:
                if active_user in active_games:
                    master_wallet_balance = 0
                    while True:
                        try:
                            master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
                            break
                        except (TypeError, sqlite3.ProgrammingError):
                            print("db error trying again...")
                            continue
                    if active_user in active_games:
                        max_bet_size = str(
                            round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)).replace(".",
                                                                                                              "\\.")
                        max_win_size = str(round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)).replace(
                            ".", "\\.")
                        intial_balance = float(game_users.check_user_balance(active_user))
                        bet_size_numeric = round(float(game_users.check_user_betsize(active_user)), 3)
                        bet_size = str(bet_size_numeric).replace(".", "\\.")
                        chat_id = active_games[active_user][3]
                        msg_id = active_games[active_user][4]
                        start_time = active_games[active_user][0]
                        current_multiplier = round(1 + round((time.time() - start_time) * seconds_step, 3), 3)
                        current_box_string = string_builder(current_multiplier)
                        # here quickly update it on their telegram
                        multiplier_numeric = current_multiplier
                        multiplier = str(multiplier_numeric).replace(".", "\\.")
                        profit = str(round(multiplier_numeric * bet_size_numeric, 3)).replace(".", "\\.")
                        current_balance = str(
                            round(intial_balance + (multiplier_numeric * bet_size_numeric), 3)).replace(
                            ".", "\\.")  # to be changed to custom
                        string_to_add = f"\n\n\n🚀 {current_box_string}\\({multiplier}x\\)\n\n\n"
                        min_bet_string = str(min_bet).replace(".", "\\.")
                        main_string = (f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is "
                                       f"running_\\.\\.\\.{string_to_add}🟣 Current Bet Size: *{bet_size} "
                                       f"SOL*  \\| 🤑 Current Profit: *{profit}* \\(_{multiplier}x_\\)\n\n💰 Max Win Amount: *"
                                       f"{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: *{min_bet_string} SOL* \\| "
                                       f"🟣 Wallet Balance: *{current_balance} SOL*")
                        edit_message(chat_id, main_string, msg_id, active_user)  # to edit the msg
        except (RuntimeError, KeyError) as err:
            print(err)
            print("error")
            pass
        time.sleep(0.09)


def game_polling_engine():  # all this has to do is crash them if they dont cash out tbh
    crash_string = "\n\n\n☠️☠️☠️ _CRASHED_ ☠️☠️☠️\n\n\n"
    seconds_step = 0.125
    while True:
        crashed = []
        temp_games = copy.deepcopy(active_games)
        #if len(temp_games) > 0:  #for debug
        #    print(temp_games)
        for active_user in temp_games:
            master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
            max_win_size = int(crash_algorithm.get_max_win(master_wallet_balance))
            multiplier_step_per_second = 0.125
            time_stamp = time.time()
            data_list = active_games[active_user]
            time_interval = int(time_stamp - data_list[0])
            max_interval = int(data_list[1] / multiplier_step_per_second) - 8
            if time_interval >= max_interval or data_list[2] * (
                    1 + (
                    time_interval * multiplier_step_per_second)) >= max_win_size:  #they cannot profit more than max win too
                crashed.append(active_user)
                break
        for finished_user in crashed:
            data_list = active_games[finished_user]
            print("user crashed: ", finished_user)
            user_to_remove = crashed.pop()
            if user_to_remove in active_games:
                del active_games[user_to_remove]
            master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
            max_bet_size = str(round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)).replace(".",
                                                                                                                 "\\.")
            max_win_size = str(round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)).replace(".", "\\.")
            wallet_balance = float(game_users.check_user_balance(finished_user))
            chat_id = data_list[3]
            msg_id = data_list[4]
            logging.info(f"User: {finished_user} has lost {data_list[2]} SOL,they crashed before a cashout event")
            new_balance = str(round(wallet_balance - data_list[2], 3))
            game_users.update_balance(finished_user, new_balance)
            new_balance = new_balance.replace(".", "\\.")
            bet_size = str(game_users.check_user_betsize(finished_user)).replace(".", "\\.")
            min_bet_string = str(min_bet).replace(".", "\\.")
            main_string = (f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                           f"running_\\.\\.\\.{crash_string}🟣 Current Bet Size: *{bet_size} "
                           f"SOL*  \\| 🤑 Current Profit: *{0}* \\(_{0}x_\\)\n\n💰 Max Win Amount: *"
                           f"{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: "
                           f"*{min_bet_string} SOL* \\|"
                           f"🟣 Wallet Balance: *{new_balance} SOL*")
            edit_message(chat_id, main_string, msg_id, finished_user)  # to edit the msg

        try:
            temp_games = copy.deepcopy(active_games)
            for active_user in temp_games:
                if active_user in active_games:
                    master_wallet_balance = 0
                    while True:
                        try:
                            master_wallet_balance = float(game_users.check_user_balance(master_wallet_username))
                            break
                        except (TypeError, sqlite3.ProgrammingError):
                            print("db error trying again...")
                            continue
                    if active_user in active_games:
                        max_bet_size = str(
                            round(float(crash_algorithm.get_max_position(master_wallet_balance)), 3)).replace(".",
                                                                                                              "\\.")
                        max_win_size = str(round(float(crash_algorithm.get_max_win(master_wallet_balance)), 3)).replace(
                            ".", "\\.")
                        intial_balance = float(game_users.check_user_balance(active_user))
                        bet_size_numeric = round(float(game_users.check_user_betsize(active_user)), 3)
                        bet_size = str(bet_size_numeric).replace(".", "\\.")
                        chat_id = active_games[active_user][3]
                        msg_id = active_games[active_user][4]
                        start_time = active_games[active_user][0]
                        current_multiplier = round(1 + round((time.time() - start_time) * seconds_step, 3), 3)
                        current_box_string = string_builder(current_multiplier)
                        # here quickly update it on their telegram
                        multiplier_numeric = current_multiplier
                        multiplier = str(multiplier_numeric).replace(".", "\\.")
                        profit = str(round(multiplier_numeric * bet_size_numeric, 3)).replace(".", "\\.")
                        current_balance = str(
                            round(intial_balance + (multiplier_numeric * bet_size_numeric), 3)).replace(
                            ".", "\\.")  # to be changed to custom
                        string_to_add = f"\n\n\n🚀 {current_box_string}\\({multiplier}x\\)\n\n\n"
                        min_bet_string = str(min_bet).replace(".", "\\.")
                        main_string = (f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is "
                                       f"running_\\.\\.\\.{string_to_add}🟣 Current Bet Size: *{bet_size} "
                                       f"SOL*  \\| 🤑 Current Profit: *{profit}* \\(_{multiplier}x_\\)\n\n💰 Max Win Amount: *"
                                       f"{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: *{min_bet_string} SOL* \\| "
                                       f"🟣 Wallet Balance: *{current_balance} SOL*")
                        edit_message(chat_id, main_string, msg_id, active_user)  # to edit the msg
        except (RuntimeError, KeyError) as err:
            print(err)
            print("error")
            pass
        time.sleep(0.1)


if __name__ == "__main__":
    t1 = threading.Thread(target=game_polling_engine)
    t2 = threading.Thread(target=check_for_deposits)
    t3 = threading.Thread(target=process_deposit)
    t4 = threading.Thread(target=process_withdrawal_request)
    t5 = threading.Thread(target=render_boxes)
    update_master_wallet_balance("", 0)  #just for testing

    #t5.start()
    t4.start()
    t3.start()
    t2.start()
    t1.start()
    bot.infinity_polling(timeout=None)
