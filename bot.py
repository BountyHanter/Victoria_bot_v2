import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command

from bot_messages import bitrix_messages as bm
from utils.callbacks.bot_callbacks import start_bitrix, add_comment_to_discus, not_comment
from utils.callbacks.callback_class_filter import MyCallback
from utils.settings import bot_logger
from bot_commands.commands import set_commands
from bot_functions.tech_functions import start, cancel
from utils.state.main_states import Bitrix


async def dev_message_startup(bot: Bot):
    await bot.send_message(977249859, 'Бот Виктории Битрикс запущен')


async def dev_message_shutdown(bot: Bot):
    await bot.send_message(977249859, 'Бот Виктории Битрикс остановлен')


async def start_bot():
    load_dotenv()
    token = os.getenv('DEV_TOKEN')
    bot = Bot(token=token, parse_mode='MarkdownV2')
    await set_commands(bot)
    dp = Dispatcher()
    loger = bot_logger.bot_logger()

    dp.startup.register(dev_message_startup)
    dp.shutdown.register(dev_message_shutdown)
    dp.message.register(start, CommandStart())
    dp.message.register(cancel, Command(commands='cancel'))
    # --------------------------------------------------
    # Заполнение сделки
    dp.callback_query.register(start_bitrix, MyCallback.filter(F.foo == 'Bitrix24')) # Старт
    dp.message.register(bm.bitrix_name, Bitrix.name)
    dp.message.register(bm.bitrix_second_name, Bitrix.second_name)
    dp.message.register(bm.bitrix_company_name, Bitrix.company_name)
    dp.message.register(bm.bitrix_city, Bitrix.city)
    dp.message.register(bm.bitrix_job_title, Bitrix.job_title)
    dp.message.register(bm.bitrix_tenchat_link, Bitrix.tenchat_link)
    dp.message.register(bm.bitrix_comment, Bitrix.comment)
    dp.callback_query.register(add_comment_to_discus, MyCallback.filter(F.foo == 'add_comment_to_dicscussion'))
    dp.message.register(bm.comment_to_discussion, Bitrix.comment_to_discus)
    dp.callback_query.register(not_comment, MyCallback.filter(F.foo == 'not_add_comment_to_dicscussion'))
    # --------------------------------------------------
    dp.message.register(bm.say_something)

    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем сообщения которые получил бот до запуска
    try:
        await dp.start_polling(bot)
    except Exception as e:
        loger.error("An error occurred: ", exc_info=True)

    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start_bot())