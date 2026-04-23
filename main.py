import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Боргузории токен аз файли .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Кнопкаҳо ---

def get_main_menu():
    """Reply Keyboard барои менюи асосӣ"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="📝 Анкета")
    builder.button(text="🖼 Фиристодани сурат")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def get_inline_link():
    """Inline Keyboard барои пайванд"""
    builder = InlineKeyboardBuilder()
    builder.button(text="👨‍💻 Муаллифи бот", url="https://github.com")
    builder.button(text="✅ Фаҳмо", callback_data="done")
    return builder.as_markup()

# --- Ҳендлерҳо (Handlers) ---

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Салом {message.from_user.full_name}! Ин боти лоиҳавии ман аст.\n"
        "Яке аз функсияҳоро интихоб кунед:",
        reply_markup=get_main_menu()
    )

@dp.message(F.text == "📝 Анкета")
async def start_survey(message: types.Message):
    await message.answer(
        "Биёед шинос шавем! 👋\n\n"
        "1. Номи шумо чист?\n"
        "2. Чандсола ҳастед?\n"
        "3. Кадом забони барномасозиро дӯст медоред?"
    )

@dp.message(F.text == "🖼 Фиристодани сурат")
async def ask_photo(message: types.Message):
    await message.answer("Лутфан, ягон сурат фиристед. Ман онро таҳлил мекунам! 📸")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.reply(
        "Раҳмат! Сурати шумо бо муваффақият қабул шуд. ✅",
        reply_markup=get_inline_link()
    )

@dp.callback_query(F.data == "done")
async def process_callback(callback: types.CallbackQuery):
    await callback.answer("Ташаккур!")
    await callback.message.answer("Шумо тугмаи Inline-ро санҷидед. Бот омода аст!")

# --- Иҷрои бот ---

async def main():
    print("Бот фаъол шуд...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот хомӯш шуд.")