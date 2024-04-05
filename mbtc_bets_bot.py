# just set up a mock up template.
import telebot
from telebot import types

my_token = '7090902228:AAHIF5lOVRa5yMIUAGj29Y3r_d1GRRp86uU'
bot = telebot.TeleBot(my_token)


@bot.message_handler(commands=['bet'])
def bet_mockup(message):
    chat_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    Place_bet = types.InlineKeyboardButton("Place a Bet", callback_data="rt")
    configure_funds = types.InlineKeyboardButton("Configure Funding", callback_data="rtrt")
    change_game = types.InlineKeyboardButton("Change Game", callback_data="rtrt")
    refer = types.InlineKeyboardButton("Referrals", callback_data="rtr")
    share_win = types.InlineKeyboardButton("Share Win", callback_data="rtrt")
    stats = types.InlineKeyboardButton("Stats", callback_data="rtr")
    markup.row(Place_bet, configure_funds, change_game)
    markup.row(refer, share_win, stats)
    bot.send_message(chat_id, f"🟣 Mini Bitcoin Bets\n\n🎲 Current Game: *Bet BTC price on the halving event*\n\n✅ Active Bet \\? : *No*\n\n🕐 Time Until Halving :  *15 days , 17:03:50 \\(2432 Blocks\\)*\n\n💰 Max bet size: *1 SOL*\n\n📈 Current Multiplier: *4\\.6x*",
                     parse_mode='MarkdownV2', reply_markup=markup)


if __name__ == "__main__":
    # generate_meme_batch()
    bot.infinity_polling(timeout=None)