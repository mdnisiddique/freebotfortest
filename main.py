
import logging
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ChatMemberHandler

TOKEN = "7834602350:AAFzoh1_rw6wSKekLoIQvy6XxeTSQOg3Lo0"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BAD_WORDS_BN = ["মাল", "হারামি", "চুদ", "গালি১", "গালি২", "গালি৩", "চোদ", "শুয়োর", "চরিত্রহীন", "নষ্টা", "ফকিন্নি", "বাজে", "বোকা", "বালের", "চুদি", "জারজ", "চুদছি", "ভিক্ষুক", "পাগল", "তোর বাপ", "গাঁজা", "চিপা", "চিরুনি", "চু", "ফাক"]
BAD_WORDS_EN = ["fuck", "shit", "bitch", "bastard", "idiot", "dumb", "moron", "stupid", "asshole", "sucker", "loser", "jerk", "damn", "freak", "crap", "piss", "retard", "dick", "cock", "hell", "slut", "hoe", "screw", "whore", "pussy"]

trigger_words = ["help", "problem", "সাহায্য", "সমস্যা", "হেল্প", "সমস"]

referral_channel_link = "https://t.me/freelancer_ni"
referral_message = f"আমাদের সকল রেফার লিংক নিচের চ্যানেলে দেওয়া ও পিন করা আছে, রেফার লিংক পেতে দয়া করে নিচের Telegram চ্যানেলে জয়েন করুন.!👇👉\n{referral_channel_link}"

user_warnings = {}

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        name = member.full_name
        await update.message.reply_text(f"Hello {name}. আমাদের Telegram গ্রুপে জয়েন করার জন্য আপনাকে অসংখ্য ধন্যবাদ.!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_id = update.message.from_user.id

    if any(bad in text for bad in BAD_WORDS_BN + BAD_WORDS_EN):
        user_warnings[user_id] = user_warnings.get(user_id, 0) + 1
        try:
            await update.message.delete()
        except:
            pass

        if user_warnings[user_id] == 1:
            await update.message.chat.restrict_member(user_id, ChatPermissions(can_send_messages=False), until_date=3600)
        elif user_warnings[user_id] == 2:
            await update.message.chat.restrict_member(user_id, ChatPermissions(can_send_messages=False), until_date=86400)
        elif user_warnings[user_id] >= 3:
            await update.message.chat.restrict_member(user_id, ChatPermissions(can_send_messages=False), until_date=259200)
        return

    if any(word in text for word in trigger_words):
        await update.message.reply_text(f"@{update.message.from_user.username} আপনার কি সমস্যা বা Problem? তা উল্লেখ করে SMS/Voice বা দরকার হলে Screenshot সহ দিয়ে রাখুন.!")

    if "ref" in text or "code" in text or "link" in text or "রেফার" in text:
        await update.message.reply_text(referral_message)

    if "http" in text or "t.me/" in text:
        try:
            await update.message.delete()
        except:
            pass
        await update.message.reply_text(referral_message)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running!")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
