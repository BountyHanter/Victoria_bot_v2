from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.callbacks.callback_class_filter import MyCallback


def start_buttons():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Создать сделку',
            callback_data=MyCallback(foo='Bitrix24').pack()),
        )
    return builder.as_markup()


def add_extra_comment():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Добавить',
            callback_data=MyCallback(foo='add_comment_to_dicscussion').pack()),
        InlineKeyboardButton(
            text='Не добавлять',
            callback_data=MyCallback(foo='not_add_comment_to_dicscussion').pack()),

    )
    return builder.as_markup()