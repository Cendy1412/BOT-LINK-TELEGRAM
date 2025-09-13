import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

async def get_direct_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_obj = None
    file_name = None

    if update.message.document:
        file_obj = update.message.document
        file_name = file_obj.file_name
    elif update.message.video:
        file_obj = update.message.video
        file_name = "video.mp4"
    elif update.message.audio:
        file_obj = update.message.audio
        file_name = file_obj.file_name or "audio.mp3"

    if file_obj:
        new_file = await context.bot.get_file(file_obj.file_id)
        file_link = f"https://api.telegram.org/file/bot{TOKEN}/{new_file.file_path}"
        await update.message.reply_text(f"📂 {file_name}\n🔗 Link tải trực tiếp:\n{file_link}")
    else:
        await update.message.reply_text("❌ Bot chỉ hỗ trợ file/document/video/audio thôi nhé.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(
        filters.Document.ALL | filters.VIDEO | filters.AUDIO,
        get_direct_link
    ))

    print("🤖 Bot đang chạy trên Render (PTB v20)...")
    app.run_polling()

if __name__ == "__main__":
    main()
