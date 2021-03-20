from aiogram.dispatcher.filters.state import StatesGroup, State


class ProductState(StatesGroup):
    """Стейт для Товаров"""
    name_product = State()
    description_product = State()
    price_product = State()
    data_product = State()


class FaqState(StatesGroup):
    """Стейт для FAQ"""
    upd_faq = State()


class QiwiState(StatesGroup):
    """Стейт для Qiwi"""
    login = State()
    token = State()



