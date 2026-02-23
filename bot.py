import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# خواندن توکن از متغیر محیطی
TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    raise ValueError("توکن ربات پیدا نشد! لطفاً در Railway متغیر محیطی TOKEN بسازید.")

# تابع ارسال نظرسنجی و دکمه‌ها
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

# تابع اجرا وقتی کاربر روی دکمه کلیک می‌کند
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user  # اطلاعات کاربر

    # ارسال پیام از طرف ربات با مشخصات کاربر
    text = f"✅️ «می‌پذیرم»\n\nکاربر: {user.full_name}\nیوزرنیم: @{user.username if user.username else 'ندارد'}"

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=text,
        reply_to_message_id=query.message.message_id  # پاسخ به پیام کاربر
    )

    # حذف نوتیفیکیشن دکمه
    await query.answer()

# ساخت و اجرای ربات
app = ApplicationBuilder().token(TOKEN).build()

# اضافه کردن هندلرها
app.add_handler(CommandHandler("poll", poll_command))  # دستور /poll
app.add_handler(CallbackQueryHandler(button_click))   # کلیک روی دکمه

# اجرای ربات
app.run_polling()
