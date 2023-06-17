from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from database import get_tariffs_family, get_tariffs_unlimited, get_tariff_gb, get_tariff_call, get_tariff_any
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from number import number_check

bot = Bot(token="TOKEN_BOT")
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Для себе').add("Для сім'ї")

for_me = ReplyKeyboardMarkup(resize_keyboard=True)
for_me.add('Інтернет').add("Дзвінки").add('На декілька пристроїв').add('До переглядів тарифів')

internet = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
internet.add('Безлім', '40 ГБ').add('25 ГБ', '8 ГБ').add('7 ГБ', 'До переглядів тарифів')


start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add('Продовжити')

class NumberCheck(StatesGroup):
    GET_NUMBER = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Для початку введіть свій номер телефону (без +38):")
    await NumberCheck.GET_NUMBER.set()


@dp.message_handler(state=NumberCheck.GET_NUMBER)
async def input_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['GET_NUMBER'] = message.text
        nums = data['GET_NUMBER']
        response = number_check(nums)
        if response == "Окей, продовжимо":
            await message.reply(response, reply_markup=start_kb)
        else:
            register_kb = ReplyKeyboardMarkup(resize_keyboard=True)
            register_kb.add('Зареєструвати номер')
            await message.reply(response, reply_markup=register_kb)
    await state.finish()

@dp.message_handler(text=['Зареєструвати номер'])
async def cmd_start(message: types.Message):
    await message.reply("Перенесіть свій номер на сайті: https://mnp.lifecell.ua/uk/mnp/ \nопісля введіть комaнду /start")

@dp.message_handler(lambda message: 'До переглядів тарифів' in message.text or 'Продовжити' in message.text)
async def cmd_start(message: types.Message):
    await message.reply("Привіт! Я допоможу тобі визначити оптимальний тариф Lifecell, для кого замовляєте тариф?",
                        reply_markup=main)

@dp.message_handler(text=["Для сім'ї"])
async def cmd_start(message: types.Message):
    tariffs = get_tariffs_family()
    for tariff in tariffs:
        id, name, price, internet, calls, description, link = tariff
        text = f"📱Тариф: {name}\n" \
               f"💸Ціна: {price}\n" \
               f"🌐Інтернет: {internet}\n" \
               f"📞Дзвінки: {calls}\n" \
               f"📎Опис: {description}"
        link_kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Підключити", url=link)
        link_kb.add(button)
        await message.reply(text, reply_markup=link_kb)

@dp.message_handler(text=["Для себе"])
async def cmd_start(message: types.Message):
    await message.reply('Гаразд, розглянемо персональні тарифи, які послуги вас цікавлять?', reply_markup=for_me)

@dp.message_handler(text=["На декілька пристроїв"])
async def cmd_start(message: types.Message):
    await message.reply('Гаразд, розглянемо персональні тарифи на декілька пристроїв')
    device = [get_tariff_any()]
    for tariff in device:
        id, name, price, internet, calls, description, link = tariff
        text = f"📱Тариф: {name}\n" \
               f"💸Ціна: {price}\n" \
               f"🌐Інтернет: {internet}\n" \
               f"📞Дзвінки: {calls}\n" \
               f"📎Опис: {description}\n"
        link_kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Підключити", url=link)
        link_kb.add(button)
        await message.reply(text, reply_markup=link_kb)

@dp.message_handler(text=["Дзвінки"])
async def cmd_start(message: types.Message):
    await message.reply("Ось тариф, що підійде для вас: ")
    call = [get_tariff_call()]
    for tariff in call:
        id, name, price, internet, calls, description, link = tariff
        text = f"📱Тариф: {name}\n" \
               f"💸Ціна: {price}\n" \
               f"🌐Інтернет: {internet}\n" \
               f"📞Дзвінки: {calls}\n" \
               f"📎Опис: {description}\n"
        link_kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Підключити", url=link)
        link_kb.add(button)
        await message.reply(text, reply_markup=link_kb)

@dp.message_handler(text=["Інтернет"])
async def cmd_start(message: types.Message):
    await message.reply("Виберіть потрібну Вам кількість інтернету" , reply_markup=internet)

@dp.message_handler(text=["Безлім"])
async def cmd_start(message: types.Message):
    await message.reply("Ось цей тариф ідеально підійде Вам: ")
    unlim = get_tariffs_unlimited()
    for tariff in unlim:
        id, name, price, internet, calls, description, advant, link = tariff
        text = f"📱Тариф: {name}\n" \
               f"💸Ціна: {price}\n" \
               f"🌐Інтернет: {internet}\n" \
               f"📞Дзвінки: {calls}\n" \
               f"📎Опис: {description}\n" \
               f"📌Переваги: \n {advant}"
        link_kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Підключити", url=link)
        link_kb.add(button)
        await message.reply(text, reply_markup=link_kb)

@dp.message_handler(text=["40 ГБ","25 ГБ", "8 ГБ", "7 ГБ"])
async def cmd_start(message: types.Message):
    text = message.text
    await message.reply(f"Ось тарифи з {text} інтернету: ")
    tariff = get_tariff_gb(text)
    if tariff is not None:
        id, name, price, internet, calls, description, link = tariff
        text = f"📱Тариф: {name}\n" \
               f"💸Ціна: {price}\n" \
               f"🌐Інтернет: {internet}\n" \
               f"📞Дзвінки: {calls}\n" \
               f"📎Опис: {description}\n"
        link_kb = InlineKeyboardMarkup()
        button = InlineKeyboardButton(text="Підключити", url=link)
        link_kb.add(button)
        await message.reply(text, reply_markup=link_kb)
    else:
        await message.reply("Тарифів з такою кількістю інтернету не знайдено.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
