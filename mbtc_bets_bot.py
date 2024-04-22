# just set up a mock up template.
import telebot
from telebot import types

my_token = '7090902228:AAHIF5lOVRa5yMIUAGj29Y3r_d1GRRp86uU'
bot = telebot.TeleBot(my_token)




# create the funsing system ( create wallet withdrawal of the sol in the wallet also the ability to view funds)
# mbtc burn statisics section too
@bot.message_handler(commands=['crash'])
def bet_mockup(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    Place_bet = types.InlineKeyboardButton("🤖 Set Autobet", callback_data="rt")
    configure_funds = types.InlineKeyboardButton("🚀 Start", callback_data="rtrt")
    change_game = types.InlineKeyboardButton("💸 Cashout", callback_data="rtrt")
    refer = types.InlineKeyboardButton("⬆️ Bet Size", callback_data="rtr")
    share_win = types.InlineKeyboardButton("😎 Share Win", callback_data="rtrt")
    stats = types.InlineKeyboardButton("Go back", callback_data="rtr")
    markup.row(Place_bet, configure_funds, change_game)
    markup.row(refer, share_win, stats)
    bot.send_message(chat_id, "__Mini Bitcoin Games__\n\n🎲 Current Game: _Crash_ 📈\nℹ️ Status: _Game is "
                              "running_\\.\\.\\.\n\n\n🚀  🟪🟪🟪🟪 \\(4\\.32x\\)\n\n\n🟣 Current Bet "
                              "Size: *0\\.2 SOL*  \\| 🤑 Current Profit: *0\\.864 SOL* \\(_4\\.32x_\\)\n\n💰 Max Win Amount: *48 "
                              "SOL*\n🔹 Min Bet Size: *0\\.01 SOL*",
                     parse_mode='MarkdownV2', reply_markup=markup)


if __name__ == "__main__":
    # generate_meme_batch()
    bot.infinity_polling(timeout=None)
