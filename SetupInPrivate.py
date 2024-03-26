from telebot import asyncio_filters
import asyncio
from telebot.async_telebot import AsyncTeleBot, types
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup
import userfunds
from solders.pubkey import Pubkey
import payout

my_token = '7082036186:AAFU9hgPpyUFfCtfM7N1nF070tzsHawDgnA'
bot = AsyncTeleBot(my_token, state_storage=StateMemoryStorage())

funds_database = userfunds.FundsDatabase()

token_twenty_two_addy = ""
master_funds_wallet_priv_key = ""


class MyStates(StatesGroup):
    proces_addy = State()


# start
@bot.message_handler(commands=['start'])
async def start(message):
    chat_id = message.chat.id  # need to figure out how to get user id as this will be the point of reference to tip
    # the user
    username = message.from_user.username
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


@bot.message_handler(
    commands=['masterbalance'])  # also need to eqully deduct for each dev they tip because it treated as same pot
async def start(message):  # will credit the dev some virtual credits
    if funds_database.check_user_exist("@CryptoSniper000"):  # use it for will too
        funds_database.update_balance("@CryptoSniper000", 100000000000)


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
        # will only get to this point if the user balance is non-zero!
        balance = funds_database.check_user_balance(username)
        wallet = funds_database.get_user_wallet(username)
        tx_result = payout.fund_user(wallet, balance)
        if "Signature:" in tx_result:
            txn_hash = "https://solscan.io/tx/" + str(tx_result.spllit()[1])
            await bot.send_message(chat_id, f"Transaction has been Confirmed : {txn_hash}")
            funds_database.update_balance(username, 0)
        else:
            await bot.send_message(chat_id, "Transaction failed Please retry")
        # here if confirmed deduct balance.
    elif response == "no_withdraw":
        await bot.send_message(chat_id, "Ok I will not Withdraw funds")
        return


if __name__ == "__main__":
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    loop = asyncio.get_event_loop()
    coros = [bot.polling()]
    loop.run_until_complete(asyncio.gather(*coros))
