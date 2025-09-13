from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import os

TOKEN = os.getenv("BOT_TOKEN")

def get_direct_link(update: Update, context: CallbackContext):
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
        file_id = file_obj.file_id
        new_file = context.bot.get_file(file_id)
        file_link = f"https://api.telegram.org/file/bot{TOKEN}/{new_file.file_path}"
        update.message.reply_text(f"📂 {file_name}\n🔗 Link tải trực tiếp:\n{file_link}")
    else:
        update.message.reply_text("❌ Bot chỉ hỗ trợ file/document/video/audio thôi nhé.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.document | Filters.video | Filters.audio, get_direct_link))

    updater.start_polling()
    print("🤖 Bot đang chạy trên Render...")
    updater.idle()

if __name__ == "__main__":
    main()
