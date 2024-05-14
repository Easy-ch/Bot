import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher,html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from keyboards import Keyboards
from messages import messages
from aiogram import types
from aiogram.types import FSInputFile
import math
# Bot token can be obtained via https://t.me/BotFather
TOKEN ='6430079230:AAGxyL2dzCo2LJFSwuTxtmguVKv2fdlxLYw'
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
course = 0
admins = set()
async def deleteweb(bot:Bot):
    await bot.delete_webhook()
async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    await deleteweb(bot)
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def command_start_handler(message:types.Message) -> None:
    await message.answer(messages['welcome_text'],reply_markup= Keyboards.start_keyboard())


@dp.message(lambda c: c.text == 'Рассчитать стоимость товара')
async def change_category(message:types.Message):
    await message.answer(messages['category'],reply_markup=Keyboards.keyboard_cost())

@dp.message(lambda c: c.text == 'Вернуться в главное меню')
async def main_menu(message:types.Message):
    await command_start_handler(message)

@dp.message(lambda c: c.text =='Обувь')
async def photo(message:types.Message):
    photo = FSInputFile('gaid.jpg')
    await bot.send_photo(chat_id=message.chat.id,photo=photo)
    await message.answer(messages['help'])

@dp.message(lambda message: message.text.isdigit())
async def calculation(message:types.Message):
    try:
        global course
        buy=float((message.text).replace(',',''))
        count=math.floor(buy*course+1000)+1800
        await message.answer(f' от {count} ₽ - стоимость вашего заказа (с учетом комиссий)')
    except ValueError:
        await message.answer(messages['warning'])

@dp.message(Command('admin'))
async def admin(message:types.Message):
    await message.answer(messages['password'])

@dp.message(lambda message: message.text)
async def admin_auth(message:types.Message):
    if message.text =='Wn_90090':
        admins.add(message.from_user.id)
        print(message.from_user.id)
        print(admins)
        await message.answer(messages['admin'],reply_markup=Keyboards.admin_keyboard())
        # await course_change(message)
    else:
        await message.answer(messages['adminnot'])

    @dp.message(lambda c: c.text =='Сменить курс') 
    async def course_change(message:types.Message):
        print("User ID:", message.from_user.id)
        await message.answer(messages['course'])
        await message.answer("У вас нет прав для выполнения этой команды.")
    @dp.message(lambda message: message.text.isdigit())
    async def change(message:types.Message):
        global course
        course = float((message.text).replace(',',''))
        await message.answer(f'Новое значение курса: {course}')
        await message.answer("У вас нет прав для выполнения этой команды.")







@dp.message()
async def echo_handler(message:types.Message) -> None:   
        try:
            await message.copy_to(chat_id=message.chat.id)
        except TypeError:
            await message.answer("Nice try!")

    # And the run events dispatching
        await dp.start_polling()

if __name__ == "__main__":
    logging.basicConfig( stream=sys.stdout)
    asyncio.run(main())
    