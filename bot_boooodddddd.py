
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import yt_dlp
import os

# ✅ التوكن يجب إضافته في متغير بيئة باسم BOT_TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_NAME = "boooodddddd_bot"

# 📥 عند استقبال رسالة تحتوي على رابط
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.startswith("http"):
        await update.message.reply_text("📎 أرسل رابط فيديو من TikTok أو YouTube أو Instagram...")
        return

    file_id = str(update.message.message_id)
    await update.message.reply_text("🔄 جارٍ تحميل الفيديو وتحويله إلى صوت MP3...")

    try:
        # إعدادات تحميل الصوت وتحويله
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

        # تحميل الصوت من الفيديو
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([text])

        audio_path = f"{file_id}.mp3"
        with open(audio_path, 'rb') as audio_file:
            await update.message.reply_audio(audio=audio_file)

        os.remove(audio_path)

    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ أثناء التحميل أو التحويل.")
        print(e)

# 🚀 تشغيل البوت
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
