from dataclasses import dataclass


@dataclass(frozen=True)
class Messages:
    product_m: str = "🎁 Товары"
    check_faq_m: str = "ℹ️ FAQ"
    change_faq_m: str = "ℹ️ Изменить FAQ 🖍"
    add_product_m: str = "📘 Добавить товар"
    remove_product_m: str = "📙 Удалить товар"
    remove_all_product_m: str = "📕 Удалить все товары"
    change_qiwi_m: str = "🔏 Изменить QIWI кошелёк"
    check_qiwi_m: str = "🔐 Проверить QIWI кошелёк"


msg = Messages()
