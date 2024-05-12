import telebot
from solders.pubkey import Pubkey
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

helius_key = "b2571c88-bb50-44bc-aa4f-198451c158b6"
URI = "https://mainnet.helius-rpc.com/?api-key=" + str(helius_key)
solana_client = Client(URI)
transactions_api = TransactionsAPI(helius_key)

game_users = user_game_database.VirtualBalance()

txhash_database = txhashdb.TxHash()

my_token = '7090902228:AAHIF5lOVRa5yMIUAGj29Y3r_d1GRRp86uU'
bot = telebot.TeleBot(my_token)



deposit_queue = {}
withdrawal_queue = {}
current_players = {}
user_who_pressed_stop = []

master_wallet = "HH1ewQT9tbjAe9qb2y833FqAYreSYVHyzxsgxkhEp34L"
min_bet = 0.01  # this is standard across all players


@bot.message_handler(commands=['start'])
def crash_game(
        message):  #every user that makes accoutn will have small amout of sol credited so it account for the intial transfer
    intial_transfer = 0.001
    chat_id = message.chat.id
    # grab a username here
    if message.from_user.username is None:  # if they don't have a username
        bot.send_message(chat_id, f"You need a Telegram username to play the game.")
        return
    user_name = "@" + message.from_user.username
    if not game_users.check_user_exist(user_name):
        fresh_address, fresh_private_key = solanahandler.create_wallet()
        if fresh_address != "" and fresh_private_key != "":
            game_users.add_user(user_name, fresh_address, fresh_private_key, str(chat_id))
            #transfer small amount of sol fro master to help then the transaction process
            transferfunds.withdraw(fresh_address, intial_transfer)

    # fetch master wallet info to determine max win,max apes
    master_wallet_balance = solanahandler.return_solana_balance(master_wallet)
    max_bet_size = int(crash_algorithm.get_max_position(master_wallet_balance))
    max_win_size = int(crash_algorithm.get_max_win(master_wallet_balance))

    current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
    bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")

    max_bet_size = str(max_bet_size)
    max_win_size = str(max_win_size)
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
    bot.send_message(chat_id, f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                              f"running_\\.\\.\\.\n\n🟣 Current Bet "
                              f"Size: *{bet_size} SOL* \n\n💰 Max Win Amount: *{max_win_size} "
                              f"SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: *0\\.1 SOL* \\| 🟣 "
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
    if not game_users.check_user_exist(user_name):
        fresh_address, fresh_private_key = solanahandler.create_wallet()
        if fresh_address != "" and fresh_private_key != "":
            game_users.add_user(user_name, fresh_address, fresh_private_key, str(chat_id))
            # will ad artificial balance to test it
            game_users.update_balance(user_name, "20.0")

    # fetch master wallet info to determine max win,max apes
    master_wallet_balance = solanahandler.return_solana_balance(master_wallet)
    max_bet_size = int(crash_algorithm.get_max_position(master_wallet_balance))
    max_win_size = int(crash_algorithm.get_max_win(master_wallet_balance))

    current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
    bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")

    max_bet_size = str(max_bet_size)
    max_win_size = str(max_win_size)
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
    bot.send_message(chat_id, f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                              f"running_\\.\\.\\.\n\n🟣 Current Bet"
                              f"Size: *{bet_size} SOL* \n\n💰 Max Win Amount: *{max_win_size} "
                              f"SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: *0\\.1 SOL* \\| 🟣 "
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
            Place_bet = types.InlineKeyboardButton("🤖 Set Autobet", callback_data=f"none")  # that will be added later
            start = types.InlineKeyboardButton("🚀 Start", callback_data=f"start")
            change_game = types.InlineKeyboardButton("💸 Cashout", callback_data=f"cashout")
            bet = types.InlineKeyboardButton("⬆️ Bet Size", callback_data=f"betup {user_name}")
            share_win = types.InlineKeyboardButton("⬇️ Bet Size", callback_data=f"betdown {user_name}")
            configure_funds = types.InlineKeyboardButton("💰 Wallet",
                                                         callback_data=f"funds {user_name}")  # pass the
            # username so we know hows checking
            markup.row(Place_bet, configure_funds, change_game)
            markup.row(bet, share_win, start)
            master_wallet_balance = solanahandler.return_solana_balance(master_wallet)
            max_bet_size = int(crash_algorithm.get_max_position(master_wallet_balance))
            max_win_size = int(crash_algorithm.get_max_win(master_wallet_balance))
            current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
            bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")
            max_bet_size = str(max_bet_size)
            max_win_size = str(max_win_size)
            modified_main_game_pos_size = (
                f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                f"running_\\.\\.\\.\n\n🟣 Current Bet Size: *{bet_size} SOL* \n\n💰 Max Win "
                f"Amount: *{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet "
                f"Size: *0\\.1 SOL* \\| 🟣 Wallet Balance: *{current_balance} SOL*")
            bot.send_message(chat_id, modified_main_game_pos_size,
                             parse_mode='MarkdownV2', reply_markup=markup)
        else:
            failed_test = True
    else:
        failed_test = True
    if failed_test:
        if not user_input.isnumeric():
            if user_input.lower() == "cancel":
                master_wallet_balance = solanahandler.return_solana_balance(master_wallet)
                max_bet_size = int(crash_algorithm.get_max_position(master_wallet_balance))
                max_win_size = int(crash_algorithm.get_max_win(master_wallet_balance))
                current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
                bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")
                max_bet_size = str(max_bet_size)
                max_win_size = str(max_win_size)
                modified_main_game_pos_size = (
                    f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                    f"running_\\.\\.\\.\n\n🟣 Current Bet Size: *{bet_size} SOL* \n\n💰 Max Win "
                    f"Amount: *{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet "
                    f"Size: *0\\.1 SOL* \\| 🟣 Wallet Balance: *{current_balance} SOL*")
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
    pool_size = solanahandler.return_solana_balance(master_wallet)
    user_name = "@" + str(callback_query.from_user.username)
    pos_size = float(game_users.check_user_betsize(user_name))
    multiplier, win_loss = crash_algorithm.determine_win_or_loss(pos_size, pool_size)
    max_multiplier = multiplier
    if response_value.split()[0] == "cashout":
        if user_name not in user_who_pressed_stop:
            user_who_pressed_stop.append(user_name)
    elif response_value.split()[0] == "start":
        if user_name not in current_players:
            if user_name not in withdrawal_queue:
                if pos_size <= float(game_users.check_user_balance(user_name)):
                    current_players[user_name] = [chat_id, time.time(), message_id, max_multiplier, 0, "", win_loss]
                else:
                    master_wallet_balance = solanahandler.return_solana_balance(master_wallet)
                    max_bet_size = int(crash_algorithm.get_max_position(master_wallet_balance))
                    max_win_size = int(crash_algorithm.get_max_win(master_wallet_balance))
                    current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
                    bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")
                    max_bet_size = str(max_bet_size)
                    max_win_size = str(max_win_size)
                    modified_main_game_pos_size = (
                        f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                        f"running_\\.\\.\\.\n\n🟣"
                        f"Current Bet Size: *{bet_size} SOL* \\(You have Insufficient funds\\) \n\n💰 Max Win"
                        f"Amount: *{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet "
                        f"Size: *0\\.1 SOL* \\| 🟣 Wallet Balance: *{current_balance} SOL*")
                    edit_message(chat_id, modified_main_game_pos_size, message_id, user_name)
            else:
                bot.send_message(chat_id,
                                 f"You cannot play until your withdrawals have been processed.Please wait few moments.")
    elif response_value.split()[0] == "betup":
        current_bet_size = float(game_users.check_user_betsize(user_name))
        new_bet_size = str(round(current_bet_size + 0.01, 3))
        game_users.update_bet_size(user_name, new_bet_size)
        master_wallet_balance = solanahandler.return_solana_balance(master_wallet)
        max_bet_size = int(crash_algorithm.get_max_position(master_wallet_balance))
        max_win_size = int(crash_algorithm.get_max_win(master_wallet_balance))

        current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
        bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")
        max_bet_size = str(max_bet_size)
        max_win_size = str(max_win_size)

        modified_main_game_pos_size = (
            f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not running_\\.\\.\\.\n\n🟣 "
            f"Current Bet Size: *{bet_size} SOL* \n\n💰 Max Win "
            f"Amount: *{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet "
            f"Size: *0\\.1 SOL* \\| 🟣 Wallet Balance: *{current_balance} SOL*")
        edit_message(chat_id, modified_main_game_pos_size, message_id, user_name)
    elif response_value.split()[0] == "betdown":
        current_bet_size = float(game_users.check_user_betsize(user_name))
        if current_bet_size > 0.01:
            new_bet_size = str(round(current_bet_size - 0.01, 3))
            game_users.update_bet_size(user_name, new_bet_size)
            master_wallet_balance = solanahandler.return_solana_balance(master_wallet)
            max_bet_size = int(crash_algorithm.get_max_position(master_wallet_balance))
            max_win_size = int(crash_algorithm.get_max_win(master_wallet_balance))
            current_balance = str(round(float(game_users.check_user_balance(user_name)), 3)).replace(".", "\\.")
            bet_size = str(game_users.check_user_betsize(user_name)).replace(".", "\\.")
            max_bet_size = str(max_bet_size)
            max_win_size = str(max_win_size)
            modified_main_game_pos_size = (
                f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                f"running_\\.\\.\\.\n\n🟣 Current Bet Size: *{bet_size} SOL* \n\n💰 Max Win "
                f"Amount: *{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet "
                f"Size: *0\\.1 SOL* \\| 🟣 Wallet Balance: *{current_balance} SOL*")
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
    number_of_squares = int(multiplier)
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
    except telebot.apihelper.ApiTelegramException:
        return


solscan_header = {
    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
             '.eyJjcmVhdGVkQXQiOjE3MDY3NTM5ODAzOTQsImVtYWlsIjoic29sYmFieTMyNUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJpYXQiOjE3MDY3NTM5ODB9.Lp77APFLV-rOnNbDzc1ob43Vp-9-KpeMe_b-fiOQrr0',
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.82 Safari/537.36'
}


def check_for_deposits():  # will update user balance if they deposited money (needs cooldown)
    while True:
        all_user_accounts = game_users.return_all_users()
        for user in all_user_accounts:
            if user not in deposit_queue:
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
                                print(f"processing {user[0]} deposit of {incoming_transfer}")
                                if str(user[
                                           0]) not in deposit_queue:  # we will ignore if they have some pending deposit
                                    deposit_queue[str(user[0])] = [incoming_transfer, time.time()]
                        except KeyError:
                            pass
                        txhash_database.add_hash(tx_hash)
                except IndexError:
                    pass
        time.sleep(2)


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
                        bot.send_message(chat_id,
                                         f"Deposit of {account_to_credit} SOL has been processed and it's ready to "
                                         f"be used")
                    else:
                        print(user_to_credit, "error with deposit please check!")
        for index, processed_deposit in enumerate(processed_deposits):
            del deposit_queue[processed_deposit]
            processed_deposits.pop(index)
        time.sleep(1)


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
                    #send a conformation mdg here:
                    bot.send_message(chat_id, f"✅ Funds Withdrawn: [Solscan link](https://solscan.io/tx/{tx})",
                                     disable_web_page_preview=True)
                else:
                    print(user_to_process, "error with withdrawal please check!")
            else:
                bot.send_message(chat_id, f"Seems like there are still funds being deposited.please wait",
                                 disable_web_page_preview=True)
        for prcessed_withdrawal in processed_withdrawals:
            del withdrawal_queue[prcessed_withdrawal]
        time.sleep(1)


def game_polling_engine():
    'break the polling until user preses cash out or looses(doesnt cash out before the crash '
    seconds_step = 0.65  # tweak the speed here (0.5-2.0)(kep at 0.75 normally i think)
    multiplier_step = 0.25  # +0.25%
    crash_string = "\n\n\n☠️☠️☠️ _CRASHED_ ☠️☠️☠️\n\n\n"
    immidiate_crash_string = "\n\n\n☠️☠️☠️ _INSTANT CRASHED_ ☠️☠️☠️\n\n\n"
    win_string = "\n\n\n🎉🎉🎉 _YOU WON_ 🎉🎉🎉\n\n\n"
    while True:
        for user in current_players:  # means they have not stopped the game yet (this shold take under few milliseconds)
            if current_players[user][6] != "no":  # they lost already
                master_wallet_balance = solanahandler.return_solana_balance(master_wallet)
                max_bet_size = int(crash_algorithm.get_max_position(master_wallet_balance))
                max_win_size = int(crash_algorithm.get_max_win(master_wallet_balance))
                intial_balance = float(game_users.check_user_balance(user))
                bet_size_numeric = float(game_users.check_user_betsize(user))
                bet_size = str(bet_size_numeric).replace(".", "\\.")
                chat_id = current_players[user][0]
                msg_id = current_players[user][2]
                start_time = current_players[user][1]
                # each mult increment is every 2 seconds
                current_multiplier_step = int((time.time() - start_time) // seconds_step)
                if current_multiplier_step == 0:
                    current_multiplier_step = 1
                current_multiplier = 1 + (multiplier_step * current_multiplier_step)
                current_players[user][4] = current_multiplier
                current_box_string = string_builder(current_multiplier)
                # here quickly update it on their telegram
                multiplier_numeric = current_multiplier
                multiplier = str(multiplier_numeric).replace(".", "\\.")
                profit = str(round(multiplier_numeric * bet_size_numeric, 3)).replace(".", "\\.")
                current_balance = str(round(intial_balance + (multiplier_numeric * bet_size_numeric), 3)).replace(".",
                                                                                                                  "\\.")  # to be changed to custom
                string_to_add = f"\n\n\n🚀 {current_box_string}\\({multiplier}x\\)\n\n\n"
                main_string = (f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is "
                               f"running_\\.\\.\\.{string_to_add}🟣 Current Bet Size: *{bet_size} "
                               f"SOL*  \\| 🤑 Current Profit: *{profit}* \\(_{multiplier}x_\\)\n\n💰 Max Win Amount: *"
                               f"{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: *0\\.1 SOL* \\| "
                               f"🟣 Wallet Balance: *{current_balance} SOL*")
                edit_message(chat_id, main_string, msg_id, user)  # to edit the msg
                current_players[user].append(current_multiplier)
                current_players[user].append(current_box_string)
        removed_players = []
        for user in current_players:
            master_wallet_balance = solanahandler.return_solana_balance(master_wallet)
            max_bet_size = int(crash_algorithm.get_max_position(master_wallet_balance))
            max_win_size = int(crash_algorithm.get_max_win(master_wallet_balance))
            if current_players[user][4] > current_players[user][3] or current_players[user][6] == "no":
                # their balance need to be reduced by their bet size
                # balance - bet size = new balance as they lost
                wallet_balance = float(game_users.check_user_balance(user))
                chat_id = int(current_players[user][0])
                msg_id = current_players[user][2]
                bet_size_numeric = float(game_users.check_user_betsize(user))
                new_balance = str(round(wallet_balance - bet_size_numeric, 3))
                game_users.update_balance(user, new_balance)
                new_balance = new_balance.replace(".", "\\.")
                bet_size = str(bet_size_numeric).replace(".", "\\.")
                if current_players[user][6] == "no":
                    crash_string = immidiate_crash_string
                main_string = (f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                               f"running_\\.\\.\\.{crash_string}🟣 Current Bet Size: *{bet_size} "
                               f"SOL*  \\| 🤑 Current Profit: *{0}* \\(_{0}x_\\)\n\n💰 Max Win Amount: *"
                               f"{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: *0\\.1 "
                               f"SOL* \\|"
                               f"🟣 Wallet Balance: *{new_balance} SOL*")
                edit_message(chat_id, main_string, msg_id, user)  # to edit the msg
                removed_players.append(user)
            if user in user_who_pressed_stop and user not in removed_players:
                if current_players[user][4] > current_players[user][3]:
                    wallet_balance = float(game_users.check_user_balance(user))
                    chat_id = int(current_players[user][0])
                    msg_id = current_players[user][2]
                    bet_size_numeric = float(game_users.check_user_betsize(user))
                    new_balance = str(round(wallet_balance - bet_size_numeric, 3))
                    game_users.update_balance(user, new_balance)
                    new_balance = new_balance.replace(".", "\\.")
                    bet_size = str(bet_size_numeric).replace(".", "\\.")
                    main_string = (f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                                   f"running_\\.\\.\\.{crash_string}🟣 Current Bet Size: *{bet_size} "
                                   f"SOL*  \\| 🤑 Current Profit: *{0}* \\(_{0}x_\\)\n\n💰 Max Win Amount: *"
                                   f"{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: "
                                   f"*0\\.1 SOL* \\|"
                                   f"🟣 Wallet Balance: *{new_balance} SOL*")
                    edit_message(chat_id, main_string, msg_id, user)  # to edit the msg
                    removed_players.append(user)
                else:
                    wallet_balance = float(game_users.check_user_balance(user))
                    chat_id = int(current_players[user][0])
                    msg_id = current_players[user][2]
                    bet_size_numeric = float(game_users.check_user_betsize(user))
                    bet_size = str(bet_size_numeric).replace(".", "\\.")
                    multiplier = str(float(current_players[user][4])).replace(".", "\\.")
                    win_numeric = round(float(current_players[user][4]) * bet_size_numeric, 3)
                    win_amount = str(win_numeric).replace(".", "\\.")
                    new_balance = str(round(wallet_balance + win_numeric, 3))
                    game_users.update_balance(user, new_balance)
                    new_balance = new_balance.replace(".", "\\.")
                    main_string = (f"__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is Not "
                                   f"running_\\.\\.\\.{win_string}🟣 Current Bet Size: *{bet_size} "
                                   f"SOL*  \\| 🤑 Current Profit: *{win_amount}* \\(_{multiplier}x_\\)\n\n💰 Max Win "
                                   f"Amount: *"
                                   f"{max_win_size} SOL*\n🔹 Max Bet Size: *{max_bet_size} SOL*\n🔹 Min Bet Size: "
                                   f"*0\\.1 SOL* \\|"
                                   f"🟣 Wallet Balance: *{new_balance}*")
                    edit_message(chat_id, main_string, msg_id, user)  # to edit the msg
                    removed_players.append(user)
                    user_who_pressed_stop.remove(user)
                    # they won
        for removed_player in removed_players:
            if removed_player in current_players:
                del current_players[removed_player]
        time.sleep(0.5)  # small pause


if __name__ == "__main__":
    t1 = threading.Thread(target=game_polling_engine)
    t2 = threading.Thread(target=check_for_deposits)
    t3 = threading.Thread(target=process_deposit)
    t4 = threading.Thread(target=process_withdrawal_request)

    t4.start()
    t3.start()
    t2.start()
    t1.start()
    bot.infinity_polling(timeout=None)
