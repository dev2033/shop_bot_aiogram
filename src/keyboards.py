from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from dialogs import msg


product_b = KeyboardButton(msg.product_m)
check_faq_b = KeyboardButton(msg.check_faq_m)
change_faq_b = KeyboardButton(msg.change_faq_m)
add_product_b = KeyboardButton(msg.add_product_m)
remove_product_b = KeyboardButton(msg.remove_product_m)
remove_all_product_b = KeyboardButton(msg.remove_all_product_m)
change_qiwi_b = KeyboardButton(msg.change_qiwi_m)
check_qiwi_b = KeyboardButton(msg.check_qiwi_m)

user_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
user_keyboard.add(product_b, check_faq_b)

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
admin_keyboard.add(product_b, check_faq_b)
admin_keyboard.add(change_faq_b)
admin_keyboard.add(add_product_b, remove_product_b)
admin_keyboard.add(remove_all_product_b)
admin_keyboard.add(change_qiwi_b)
admin_keyboard.add(check_qiwi_b)

delete_confirmation = InlineKeyboardMarkup()
yes_button = InlineKeyboardButton(
    msg.yes_delete_all_item,
    callback_data='yes_delete_all_items'
)
no_button = InlineKeyboardButton(
    msg.no_delete_all_item,
    callback_data='no_delete_all_items'
)
back_button = InlineKeyboardButton(
    msg.back_msg,
    callback_data='back_btn'
)
delete_confirmation.add(yes_button, no_button)
delete_confirmation.add(back_button)
