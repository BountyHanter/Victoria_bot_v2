from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.inline import start_buttons


async def start(message: Message, bot: Bot):
    await message.answer(f'Привет {message.from_user.first_name}, что хочешь сделать??', reply_markup=start_buttons())


async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Все этапы были отменены, можешь начинать сначала', reply_markup=start_buttons())