from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters import IsNotBanned
from loader import bot, dp
from keyboards.default import main_kbd


@dp.message_handler(IsNotBanned(), text='☎ Полезные контакты')
async def cmd_useful_contacts(message: types.Message):
    text = f'<u>Управляющая компания:</u>\n<b>Диспетчерская служба ООО «УЭР-ЮГ»</b>\n<code>+7 4722 35-50-06</code>\n' \
           f'<b>Инженеры ООО «УЭР-ЮГ»</b>\n<code>+7 920 566-28-86</code>\n' \
           f'<b>Бухгалтерия ООО «УЭР-ЮГ»</b>\n<code>+7 4722 35-50-06</code>\n' \
           f'<i>Белгород, Свято-Троицкий б-р, д. 15, подъезд No 1</i>\n\n' \
           f'<u>Телефоны для открытия ворот и шлагбаума:</u>\n' \
           f'<b>Шлагбаум «Набережная»</b>\n<code>+7 920 554-87-74</code>\n' \
           f'<b>Ворота «Харьковские»</b>\n<code>+7 920 554-87-40</code>\n' \
           f'<b>Ворота «Мост»</b>\n<code>+7 920 554-64-06</code>\n' \
           f'<b>Калитка 1 «Мост»</b>\n<code>+7 920 554-42-10</code>\n' \
           f'<b>Калитка 2 «Мост»</b>\n<code>+7 920 554-89-04</code>\n' \
           f'<b>Калитка 3 «Харьковская»</b>\n<code>+7 920 554-87-39</code>\n' \
           f'<b>Калитка 4 «Харьковская»</b>\n<code>+7 920 554-89-02</code>\n\n' \
           f'<b>Охрана</b>\n' \
           f'<code>+7 915 57-91-457</code>\n\n' \
           f'<b>Участковый</b>\n' \
           f'Куленцова Марина Владимировна\n' \
           f'<code>+7 999 421-53-72</code>'

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    text = text
    await message.answer(
        text=text,
        reply_markup=main_kbd,
    )
