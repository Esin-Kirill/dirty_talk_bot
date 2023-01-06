from aiogram.utils.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_callback = CallbackData('main', 'data')

# Initialize keybords and buttons
# Start keyboard
button1 = KeyboardButton("Let's fucking go \U0001F63C")
button2 = KeyboardButton("Change audio voice \U0001F3A4")
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
start_keyboard.row(button1, button2)

# Main flow keyboard
button1 = InlineKeyboardButton('More \U0001F4A9', callback_data=main_callback.new(data='more_insult'))
button2 = InlineKeyboardButton('Voice it \U0001F50A', callback_data=main_callback.new(data='voice_it'))
main_keyboard = InlineKeyboardMarkup(row_width=2)
main_keyboard.row(button1, button2)
