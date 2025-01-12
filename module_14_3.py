from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

inl_start = InlineKeyboardMarkup()
but1 = InlineKeyboardButton(text = 'Рассчитать норму калорий', callback_data='calories')
but2 = InlineKeyboardButton(text = 'Формулы расчета', callback_data='formulas')
inl_start.add(but1)
inl_start.add(but2)


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button)
kb.add(button2)
kb.add(button3)

kb_buy = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text='Product1', callback_data = 'product_buying')],
    [InlineKeyboardButton(text='Product2', callback_data = 'product_buying')],
    [InlineKeyboardButton(text='Product3', callback_data = 'product_buying')],
    [InlineKeyboardButton(text='Product4', callback_data = 'product_buying')]
    ]
)

class UserState(StatesGroup):
    adress = State()
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = inl_start)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer("Формула для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()

@dp.callback_query_handler(text = 'product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1,5):
        text = f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}'
        with open(f'kart/{i}.png', "rb") as img:
            await message.answer_photo(img, text)
    await message.answer("Выберите продукт для покупки ", reply_markup = kb_buy)

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = kb)

@dp.message_handler(text=['Информация'])
async def info_message(message):
    await message.answer('Это бот только учится быть ботом')

@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст ')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message,state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес ')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    await message.answer('ща рассчитаю')
    weig_ = int(data['weight'])
    grow_ = int(data['growth'])
    age_ = int(data['age'])
    norma = 10*weig_+6.25*grow_-5*age_-161
    await message.answer(f'Норма калорий {norma} калорий')
    await state.finish()

@dp.message_handler()
async def all_messages(message):
    await message.answer('я еще не знаю такие слов')
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)
