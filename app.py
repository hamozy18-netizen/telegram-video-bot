import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل السكريبت وسأصنع لك فيديو 🎬")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # توليد الصوت
    tts = gTTS(text=text, lang='ar')
    tts.save("voice.mp3")

    # إنشاء فيديو خلفية سوداء + صوت باستخدام ffmpeg فقط
    subprocess.run([
        "ffmpeg",
        "-f", "lavfi",
        "-i", "color=c=black:s=720x1280:d=20",
        "-i", "voice.mp3",
        "-shortest",
        "-c:v", "libx264",
        "-c:a", "aac",
        "video.mp4"
    ])

    await update.message.reply_video(video=open("video.mp4", "rb"))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
