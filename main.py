import telebot
from youtubesearchpython import VideosSearch
import yt_dlp
import os

BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Hi! Send /song <song name> to get the audio 🎶")

@bot.message_handler(commands=['song'])
def song(message):
    try:
        query = message.text.replace('/song', '').strip()
        if not query:
            bot.reply_to(message, "Please type song name after /song 😅")
            return
        bot.reply_to(message, f"🎧 Searching `{query}`...")
        videos = VideosSearch(query, limit=1).result()
        link = videos['result'][0]['link']
        title = videos['result'][0]['title']

        bot.reply_to(message, f"⬇️ Downloading **{title}**...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'song.%(ext)s',
            'quiet': True,
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        audio_file = "song.webm"
        if not os.path.exists(audio_file):
            audio_file = "song.m4a"

        bot.send_audio(message.chat.id, open(audio_file, 'rb'), title=title)
        os.remove(audio_file)

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

bot.polling()
