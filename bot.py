import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")

async def poll_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ارسال نظرسنجی
    await update.message.reply_poll(
        question="آیا در رانینگ این هفته حضور دارید؟",
        options=["بله، شرکت میکنم✌️😍", "این هفته نمیام😴"],
        is_anonymous=False
    )

    # دکمه شیشه‌ای
    keyboard = [[InlineKeyboardButton("✅️ می‌پذیرم", callback_data="accept")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "لطفاً قبل از اولین حضور مرامنامه را مطالعه کرده و عبارت «می‌پذیرم» را ارسال کنید",
        reply_markup=reply_markup
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="✅️ «می‌پذیرم»"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("poll", poll_command))
app.add_handler(CallbackQueryHandler(button_click))

app.run_polling()
