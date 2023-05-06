from .services import TelegramServices
from telegram.ext import  CommandHandler, MessageHandler, filters



list=[
    CommandHandler('start', TelegramServices.start),
    MessageHandler(filters.TEXT & ~filters.COMMAND, TelegramServices.hello),
    MessageHandler(filters.COMMAND, TelegramServices.unknown)
    ]
