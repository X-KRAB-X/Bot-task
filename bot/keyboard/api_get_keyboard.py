from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

users_button = InlineKeyboardButton(text='👤 Пользователи', callback_data='users')
posts_button = InlineKeyboardButton(text='📝 Посты', callback_data='posts')
comments_button = InlineKeyboardButton(text='🗣️ Комментарии', callback_data='comments')
albums_button = InlineKeyboardButton(text='📀 Альбомы', callback_data='albums')
photos_button = InlineKeyboardButton(text='🌄 Фотографии', callback_data='photos')
todos_button = InlineKeyboardButton(text='📌 Заметки', callback_data='todos')
cancel_button = InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')


api_get_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [users_button, todos_button],
    [posts_button, comments_button],
    [albums_button, photos_button],
    [cancel_button]
])

only_cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [cancel_button]
])
