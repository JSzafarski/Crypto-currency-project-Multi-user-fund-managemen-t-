from telebot import asyncio_filters
import asyncio
from telebot.async_telebot import AsyncTeleBot, types
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
import userfunds
from solders.pubkey import Pubkey
import payout2
import logging

my_token = '7082036186:AAFU9hgPpyUFfCtfM7N1nF070tzsHawDgnA'
bot = AsyncTeleBot(my_token, state_storage=StateMemoryStorage())

funds_database = userfunds.FundsDatabase()
logging.basicConfig(filename='file.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')


class MyStates(StatesGroup):
    proces_addy = State()


# start
@bot.message_handler(commands=['start'])
async def start(message):
    chat_id = message.chat.id  # need to figure out how to get user id as this will be the point of reference to tip
    # the user
    username = message.from_user.username
    print(f"{username} has clicked start")
    if username is None:
        await bot.send_message(chat_id,
                               f"You need an associated username to create an account")
        return
    await bot.send_message(chat_id,
                           f"Welcome {username} to the mBTC tipping bot! \nCheck the commands below to get started, so you can "
                           "start receiving and sending tips to other users with mBTC. \n\n/setwallet - Assign a "
                           "SOL address to your Telegram account\n/checkbalance - Check your tips "
                           "balance\n/withdraw - Withdraw your balance\n\n*Please note you can only send mBTC to "
                           "other users if your balance is above 0.")


# set wallet
@bot.message_handler(commands=['setwallet'])
async def start(message):
    chat_id = message.chat.id
    username = message.from_user.username
    if username is None:
        await bot.send_message(chat_id,
                               f"You need an associated username to create an account")
        return
    if funds_database.check_user_exist("@" + username):
        wallet_addy = funds_database.get_user_wallet("@" + username)
        markup = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton("Yes", callback_data="yes_new_wallet " + str(username) + " " + str(chat_id))
        no = types.InlineKeyboardButton("No", callback_data="no_new_wallet " + str(username) + " " + str(chat_id))
        markup.row(yes, no)
        await bot.send_message(chat_id,
                               f"⚠️ You already have a wallet associated to this account.\nThe wallet is : {wallet_addy}\nYou may "
                               f"change the wallet to a different one.\nWould you like to proceed?",
                               reply_markup=markup)
    else:
        await bot.send_message(chat_id, "Please enter a valid Solana Address")
        await bot.set_state(chat_id, MyStates.proces_addy, chat_id)


@bot.message_handler(commands=['checkbalance'])
async def start(message):
    chat_id = message.chat.id
    username = message.from_user.username
    if username is None:
        await bot.send_message(chat_id,
                               f"You need an associated username to create an account")
        return
    if funds_database.check_user_exist("@" + username):
        funds = funds_database.check_user_balance("@" + username)
        mbtc_balance = float(funds) / float(100000000000)
        await bot.send_message(chat_id, f"💰 Your balance is : {mbtc_balance:.11f} mBTC ({funds} mSatoshis)")
    else:
        await bot.send_message(chat_id, "⚠️ You haven't setup a wallet yet.\nPlease use /start and follow instructions "
                                        "to begin")


@bot.message_handler(commands=['withdraw'])
async def start(message):
    chat_id = message.chat.id
    if message.from_user.username is None:
        await bot.send_message(chat_id,
                               f"You need an associated username to create an account")
        return
    username = "@" + message.from_user.username
    if not funds_database.check_user_exist(username):
        await bot.send_message(chat_id, "⚠️ You have not associated a wallet to this account!")
        return
    if not int(funds_database.check_user_balance(username)) > 0:
        await bot.send_message(chat_id, "⚠️ Unable to withdraw a zero balance!")
        return
    wallet = funds_database.get_user_wallet(username)
    markup = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton("Yes", callback_data="yes_withdraw " + str(username) + " " + str(chat_id))
    no = types.InlineKeyboardButton("No", callback_data="no_withdraw " + str(username) + " " + str(chat_id))
    markup.row(yes, no)
    await bot.send_message(chat_id,
                           f"⚠️ You are withdrawing all the tips collected to the wallet : \n\n    *{wallet}*\n\nWould you like to proceed?",
                           reply_markup=markup, parse_mode='MarkdownV2')


# im going to add another admin tool to manually update user balances
@bot.message_handler(
    commands=['masterbalance'])  # also need to eqully deduct for each dev they tip because it treated as same pot
async def start(message):  # will credit the dev some virtual credits
    if funds_database.check_user_exist("@CryptoSniper000"):  # use it for will too
        current_dev_balance = int(funds_database.check_user_balance("@CryptoSniper000"))
        print(current_dev_balance)
        funds_database.update_balance("@CryptoSniper000", 100000000000+current_dev_balance)
        print("masterbalance added "+str(funds_database.check_user_balance("@CryptoSniper000")))


@bot.message_handler(
    commands=['test333'])
async def send_test_rewards_info(message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "🟣 *__Raid to earn__*\n\n⚔️ Shill $mBTC on X to a big Crypto Twitter"
                                       " influencer ⚔️\n\nIf your post is raided, you will be tipped *10000000 "
                                       "mSatoshis*\\.\n\n_How to increase the chances of your post getting raided_?\n\n1\\) "
                                       "Reply to a big Crypto Twitter influencer's post that is <2 hours old\n2\\) "
                                       "Include the $mBTC ticker in your reply and tag @mbtc\\_sol\n3\\) Not AI generated "
                                       "and generic\n4\\) Account must not be shadow banned\\. Check "
                                       "here:\n[Shadowban](https://shadowban.yuzurisa.com/)\n\nYou will be tipped upon completion "
                                       "of the raid\\.",
                     parse_mode='MarkdownV2', disable_web_page_preview=True)


@bot.message_handler(
    commands=['resetuser'])  # used for withdrawals
async def start(message):  # will credit the dev some virtual credits
    chat_id = message.chat.id
    arguments = message.text.split()
    user_to_reset = arguments[1]

    if funds_database.check_user_exist(user_to_reset):  # use it for will too
        funds_database.update_balance(user_to_reset, 0)
        await bot.send_message(chat_id,
                               f"User reset complete",
                               parse_mode='MarkdownV2')
    else:
        await bot.send_message(chat_id,
                               f"⚠️ User not found",
                               parse_mode='MarkdownV2')


@bot.message_handler(state=MyStates.proces_addy)
async def process_address(message):
    username = message.from_user.username
    wallet = message.text  # check if wallet is on curve!
    chat_id = message.chat.id
    passed = True
    if 44 >= len(str(wallet)) >= 32:
        key = Pubkey.from_string(str(wallet))
        if key.is_on_curve():
            if funds_database.check_user_exist("@" + username):
                funds_database.update_wallet(username, wallet)
                await bot.send_message(chat_id, "Wallet updated!")
                await bot.delete_state(chat_id, chat_id)
                return
            else:
                funds_database.add_user("@" + username, wallet)
                print(f"user @{username} has registered!")
                logging.info(f"user : @{username} registered")
                await bot.send_message(chat_id, "You have been successfully added to the database!")
                await bot.delete_state(chat_id, chat_id)
                return
        else:
            passed = False
    else:
        passed = False
    if not passed:
        if wallet == "stop":
            await bot.send_message(chat_id, "Wallet entry process stopped.")
            await bot.delete_state(message.from_user.id, message.chat.id)
            return
        else:
            await bot.send_message(chat_id, "Invalid entry. Please enter a valid Solana address.\nType 'stop' to stop "
                                            "the"
                                            "process.")
            await bot.set_state(chat_id, MyStates.proces_addy, chat_id)
            return


@bot.callback_query_handler(func=lambda call: True)
async def help_func_callback(callback_query: types.CallbackQuery):
    msg_to_remove = callback_query.message.message_id
    response_value = str(callback_query.data)
    username = response_value.split()[1]
    response = response_value.split()[0]
    chat_id = int(response_value.split()[2])
    await bot.delete_message(chat_id, msg_to_remove)  # remove message
    if response == "yes_new_wallet":
        await bot.send_message(chat_id, "Please enter a valid Solana Address")
        await bot.set_state(chat_id, MyStates.proces_addy, chat_id)
        return
    elif response == "no_new_wallet":
        await bot.send_message(chat_id, "User data unchanged")
        return
    elif response == "yes_withdraw":
        # add a log of withdrawals
        # will only get to this point if the user balance is non-zero!
        balance = funds_database.check_user_balance(username)
        wallet = funds_database.get_user_wallet(username)
        logging.info(f"user : {username} requested a withdrawal of : {balance} to wallet {wallet}")
        print(f"user : {username} requested a withdrawal of : {balance} to wallet {wallet}")
        '''tx_result = payout2.send_tokens(wallet, balance)
        if "tx" in tx_result:
            txn_hash = tx_result
            await bot.send_message(chat_id, f"Transaction has been Confirmed : {txn_hash}")
            funds_database.update_balance(username, 0)'''
        await bot.send_message(chat_id, "Transaction failed Please retry or wait for the team to perform a manual "
                                        "transfer (Minimum withdrawal: 0.15 mBTC) (Mini Bitcoin team is trying to resolve this issue asap ,Funds are "
                                        "SAFU!)\n")
        # here if confirmed deduct balance.
    elif response == "no_withdraw":
        await bot.send_message(chat_id, "Ok I will not Withdraw funds")
        return


if __name__ == "__main__":
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    loop = asyncio.get_event_loop()
    coros = [bot.polling()]
    loop.run_until_complete(asyncio.gather(*coros))
