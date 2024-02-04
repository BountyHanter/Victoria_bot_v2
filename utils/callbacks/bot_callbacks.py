from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot_data.info import Info
from keyboards.inline import start_buttons
from utils.state.main_states import Bitrix


async def start_bitrix(query: CallbackQuery, bot: Bot, state: FSMContext):
    info = Info()
    await state.update_data(info=info) # Переносим экземпляр в машину состояний
    await query.message.answer('Окей, заполним заказ и отправим в Битрикс')
    await bot.answer_callback_query(query.id)
    await bot.edit_message_reply_markup(query.from_user.id, query.message.message_id)  # удаляем кнопку
    await query.answer()
    await state.set_state(Bitrix.name)
    await query.message.answer('Для начала, введи имя')


async def add_comment_to_discus(query: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.answer_callback_query(query.id)
    await bot.edit_message_reply_markup(query.from_user.id, query.message.message_id)  # удаляем кнопку
    await query.answer()
    await state.set_state(Bitrix.comment_to_discus)
    await query.message.answer('Хорошо, напиши свой комментарий и я добавлю его в обсуждение к сделке')


async def not_comment(query: CallbackQuery, bot: Bot, state: FSMContext):
    # await update_data(state)  # Загружаем данные сделки в кэш
    await state.clear()
    await bot.answer_callback_query(query.id)
    await bot.edit_message_reply_markup(query.from_user.id, query.message.message_id)  # удаляем кнопку
    await query.answer()
    await query.message.answer('Хорошо, что нибудь еще?', reply_markup=start_buttons())
