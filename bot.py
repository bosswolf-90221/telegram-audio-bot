bot_code = """
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import yt_dlp
import os

# Token and Bot Name
BOT_TOKEN = "8436279336:AAEBL5FveHlwdfuGx8w6wCYAfDgaxP5O6zg"
BOT_NAME = "@Tuasdsaasfafa_bot"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.startswith("http"):
        await update.message.reply_text("📎 أرسل رابط فيديو من TikTok أو YouTube أو Instagram...")
        return
    file_id = str(update.message.message_id)
    await update.message.reply_text("🔄 جارٍ تحميل الفيديو وتحويله إلى صوت MP3...")

    try:
        ydl_opts = {
            'outtmpl': f'{file_id}.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([text])

        audio_path = f"{file_id}.mp3"
        with open(audio_path, 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file)

        os.remove(audio_path)
    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ أثناء التحميل أو التحويل.")
        print(e)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
"""

file_path = "/mnt/data/bot_Tuasdsaasfafa.py"
with open(file_path, "w", encoding="utf-8") as file:
    file.write(bot_code)

file_path
