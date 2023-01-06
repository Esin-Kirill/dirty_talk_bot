import os
import pyttsx3
from messages import *
from configs import BOT_TOKEN, ADMIN_CHAT_ID
from keyboards import start_keyboard, main_keyboard, main_callback
from aiogram.dispatcher import FSMContext
from functions import get_insult_phrase, get_insult_gif
from aiogram import Bot, Dispatcher, executor, types


# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
voice_engine = pyttsx3.init()
voice_engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
voice_engine.setProperty('rate', 130)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Bot entry point
    """

    username = "motherfucker" if not message.from_user.first_name or message.from_user.first_name == 'None' else message.from_user.first_name
    welcome_msg = WELCOME_MSG_EN.format(username=username)
    await bot.send_message(message.chat.id, welcome_msg, reply_markup=start_keyboard)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    """
    Send help
    """
    await bot.send_message(message.chat.id, HELP_MSG_EN, reply_markup=start_keyboard)


@dp.message_handler(commands=['voice'])
async def send_voice_choice(message: types.Message):
    """
    Change audio voice
    """
    voices_dict = {}
    voices = voice_engine.getProperty('voices')
    voice_msg = VOICE_MSG_EN
    
    for num, voice in enumerate(voices, start=1):
        voices_dict[num] = (voice.id, voice.name)
        voice_msg += f"{num}. {voice.name}\n"

    await bot.send_message(message.chat.id, voice_msg)


async def send_insult(message: types.Message):
    insult_phrase = get_insult_phrase()
    insult_gif = get_insult_gif()
    await bot.send_animation(message.chat.id, insult_gif, caption=insult_phrase, reply_markup=main_keyboard)


@dp.callback_query_handler(main_callback.filter(data='more_insult'))
async def send_insult_callback(query: types.CallbackQuery):
    insult_phrase = get_insult_phrase()
    insult_gif = get_insult_gif()
    await bot.send_animation(query.message.chat.id, insult_gif, caption=insult_phrase, reply_markup=main_keyboard)


@dp.callback_query_handler(main_callback.filter(data='voice_it'))
async def send_insult_audio_callback(query: types.CallbackQuery):
    gif_caption = query.message.caption
    audio_name = f"{query.message.chat.id}-{query.id}.mp3"
    audio_name = os.path.join(os.getcwd(), audio_name)
    voice_engine.save_to_file(gif_caption, audio_name)
    voice_engine.runAndWait()
    await bot.send_voice(query.message.chat.id, open(audio_name, "rb"))
    os.remove(audio_name)


@dp.message_handler()
async def process_main_keyboard(message: types.Message):
    """
    This handler will be called 
    when user presses one of buttons from main_keyboard
    OR writes unknown text
    """

    if message.text.startswith("Let's"):
        await send_insult(message)
    elif message.text.startswith('Change'):
        await send_voice_choice(message)
    else:
        await message.reply("WTF?! I don't know human language...\nLet me show you what I was created for \U0001F519")
        await send_help(message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
