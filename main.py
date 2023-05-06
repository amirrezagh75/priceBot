from pydantic import BaseSettings
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder
from TelegramConfig import handlers


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class Settings(BaseSettings):

    T_TOKEN: str

    class Config:
        env_file = ".env"


settings = Settings()


def main() -> None:
    app = ApplicationBuilder().token(settings.T_TOKEN).build()
    app.add_handlers(handlers=handlers.list)
    app.run_polling()


if __name__ == '__main__':
    main()
