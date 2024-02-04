from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot_messages.bot_funny_answer import bot_responses
from bot_functions.bitrix import add_contact, add_deal, add_company, add_comment_to_discussion
from keyboards.inline import start_buttons, add_extra_comment
from utils.state.main_states import Bitrix
from bot_messages.bot_answer_text import contact_add_error, company_add_error, deal_add_error, deal_add_ok, \
    comment_to_discus_add_error, comment_add_ok


async def say_something(message: Message):
    await message.answer(bot_responses.get_response())


async def bitrix_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.name = get_data.get('name')
    await state.update_data(info=info)  # обновляем info в state
    await state.set_state(Bitrix.second_name)
    await message.answer('Теперь введи фамилию')


async def bitrix_second_name(message: Message, state: FSMContext):
    await state.update_data(second_name=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.second_name = get_data.get('second_name')
    await state.update_data(info=info)  # обновляем info в state
    await state.set_state(Bitrix.company_name)
    await message.answer('Теперь введи название компании')


async def bitrix_company_name(message: Message, state: FSMContext):
    await state.update_data(company_name=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.company_name = get_data.get('company_name')
    await state.update_data(info=info)  # обновляем info в state
    await state.set_state(Bitrix.city)
    await message.answer('Теперь введи город')


async def bitrix_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.city = get_data.get('city')
    await state.update_data(info=info)  # обновляем info в state
    await state.set_state(Bitrix.job_title)
    await message.answer('Теперь введи должность')


async def bitrix_job_title(message: Message, state: FSMContext):
    await state.update_data(job_title=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.job_title = get_data.get('job_title')
    await state.update_data(info=info)  # обновляем info в state
    await state.set_state(Bitrix.tenchat_link)
    await message.answer('Теперь введи ссылку на тенчат')


async def bitrix_tenchat_link(message: Message, state: FSMContext):
    await state.update_data(tenchat_link=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.tenchat_link = get_data.get('tenchat_link')
    await state.update_data(info=info)  # обновляем info в state
    await state.set_state(Bitrix.comment)
    await message.answer('Теперь введи комментарий')


async def bitrix_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.comment = get_data.get('comment')
    await state.update_data(info=info)  # обновляем info в state
    await message.answer('Отлично, сейчас отправлю запрос и отпишусь')

    # Запускаем создание контакта
    contact = add_contact.NewContact(info.name, info.second_name,
                                     info.city, info.job_title,
                                     info.tenchat_link)
    respond_contact_id = contact.send_request()  # Получаем результат создания контакта
    if respond_contact_id is None:
        # Ошибка при создании контакта
        await message.answer(contact_add_error, reply_markup=start_buttons())
        return

    # Запускаем создание компании
    company = add_company.NewCompany(info.company_name)
    respond_company = company.send_request()
    if respond_company is None:
        # Ошибка при создании контакта
        await message.answer(company_add_error, reply_markup=start_buttons())
        return

    # Запускаем создание сделки
    deal = add_deal.NewDeal(info.comment, respond_contact_id, respond_company)
    final_respond = deal.send_request()  # Возвращается 2 элемента [айди сделки в битрикс, номер сделки]
    if final_respond[0] is False:
        # Ошибка при создании сделки
        await message.answer(deal_add_error, reply_markup=start_buttons())
        return
    print(info)
    info.deal_id = final_respond[0]
    info.id_number = final_respond[1]
    await state.update_data(info=info)  # обновляем info в state
    await message.answer(deal_add_ok, reply_markup=add_extra_comment())


# Добавление комментария в обсуждение
async def comment_to_discussion(message: Message, state: FSMContext):
    await state.update_data(comment_to_discus=message.text)
    get_data = await state.get_data()
    info = get_data.get('info')
    info.comment_to_discus = get_data.get('comment_to_discus')
    await state.update_data(info=info)  # обновляем info в state
    comment_to_discus = add_comment_to_discussion.AddComment(info.comment_to_discus, info.deal_id)
    comment_to_discus.send_request()
    if comment_to_discus is False:
        # Ошибка при создании комментария к обсуждению
        await message.answer(comment_to_discus_add_error, reply_markup=start_buttons())
        return
    await state.clear()
    await message.answer(comment_add_ok, reply_markup=start_buttons())
