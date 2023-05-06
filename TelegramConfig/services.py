from telegram import Update
from telegram.ext import ContextTypes
import logging
import re
import db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class TelegramServices:
    
    def messageHandler(message):
        context = re.sub(r'[^a-zA-Z | \u0600-\u06FF]+', '', message)
        if context == "price" or context =="قیمت":
            result = db.priceTemplate()
            return result
        elif db.priceTemplate(context) :
            result = db.priceTemplate(context)
            return result
        else: 
            return "متاسفانه درخواست ارسالی مفهوم نبود😞.\nلطفا مجددا تلاش بفرمایید 🙏🏻"
            

    async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(TelegramServices.messageHandler(update.message.text))

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"سلام {update.effective_user.first_name}. به بات رسمی صرافی باینکس خوش اومدی.\n میتونی برای دریافت قیمت کلمه 'قیمت' رو ارسال کنی و یا اسم توکن مورد نظرت رو یا به فارسی یا به انگلیسی بفرستی تا بتونم آخرین قیمت رو بهت بگم.")

    async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
