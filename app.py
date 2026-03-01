import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
from moviepy.editor import *

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل السكريبت وسأحولّه إلى فيديو 🎬")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # توليد صوت
    tts = gTTS(text=text, lang='ar')
    tts.save("voice.mp3")

    # خلفية سوداء عمودية
    background = ColorClip(size=(720,1280), color=(0,0,0), duration=15)

    # إدخال الصوت
    audio = AudioFileClip("voice.mp3")
    background = background.set_audio(audio)

    # كتابة نص
    txt_clip = TextClip(text, fontsize=50, color='white', size=(680,None), method='caption')
    txt_clip = txt_clip.set_position(("center","center")).set_duration(audio.duration)

    final = CompositeVideoClip([background, txt_clip])
    final.write_videofile("video.mp4", fps=24)

    await update.message.reply_video(video=open("video.mp4","rb"))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
