import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# ---------- FSM ----------
class TestState(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()


# ---------- Клавиатуры ----------
start_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✨ Начать тест", callback_data="start_test")]
    ]
)


def question_kb(answers: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, callback_data=key)]
            for key, text in answers.items()
        ]
    )


# ---------- Старт ----------
@dp.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "✨ Привет. Этот короткий тест поможет определить твой личный символ года — "
        "образ, который будет поддерживать тебя и напоминать о важном.\n\n"
        "Ответь интуитивно, здесь нет «правильных» вариантов.",
        reply_markup=start_kb
    )


@dp.callback_query(F.data == "start_test")
async def start_test(call: CallbackQuery, state: FSMContext):
    await state.set_state(TestState.q1)
    await state.update_data(score={"star": 0, "fire": 0, "shield": 0, "heart": 0})

    await call.message.answer(
        "1️⃣ Как ты входишь в этот год?",
        reply_markup=question_kb({
            "shield": "🛡 Спокойно и осознанно",
            "heart": "🤍 С чувством перемен",
            "fire2": "🔥 Через внутренний вызов",
            "star": "⭐️ С надеждой и ожиданием"
        })
    )
    await call.answer()


# ---------- Вопрос 1 ----------
@dp.callback_query(TestState.q1)
async def q1(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    score = data["score"]

    if call.data.startswith("fire"):
        score["fire"] += 1
    elif call.data == "shield":
        score["shield"] += 1
    elif call.data == "star":
        score["star"] += 1

    await state.update_data(score=score)
    await state.set_state(TestState.q2)

    await call.message.answer(
        "2️⃣ Что для тебя сейчас важнее всего?",
        reply_markup=question_kb({
            "shield": "🛡 Защита и границы",
            "fire": "🔥 Рост и развитие",
            "heart": "🤍 Любовь и близость",
            "star": "⭐️ Ясность и направление"
        })
    )
    await call.answer()


# ---------- Вопрос 2 ----------
@dp.callback_query(TestState.q2)
async def q2(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["score"][call.data] += 1

    await state.set_state(TestState.q3)
    await call.message.answer(
        "3️⃣ Что ты чаще выбираешь?",
        reply_markup=question_kb({
            "star": "⭐️ Интуицию",
            "fire": "🔥 Действие",
            "heart": "🤍 Принятие",
            "shield": "🛡 Наблюдение"
        })
    )
    await call.answer()


# ---------- Вопрос 3 ----------
@dp.callback_query(TestState.q3)
async def q3(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["score"][call.data] += 1

    await state.set_state(TestState.q4)
    await call.message.answer(
        "4️⃣ Какой образ откликается сильнее?",
        reply_markup=question_kb({
            "heart": "🤍 Свет",
            "shield": "🛡 Круг",
            "fire": "🔥 Пламя",
            "star2": "⭐️ Путь"
        })
    )
    await call.answer()


# ---------- Результат ----------
@dp.callback_query(TestState.q4)
async def result(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    score = data["score"]

    if call.data.startswith("star"):
        score["star"] += 1
    else:
        score[call.data] += 1

    symbol = max(score, key=score.get)

    results = {
        "heart": {
            "text": (
                "❤️ **Твой символ года — Сердце**\n\n"
                "Год чувств, близости и искренности.\n"
                "Про честность с собой и тёплые связи.\n\n"
                "💗 Украшение с этим символом —\n"
                "напоминание жить из сердца.\n\n"
                "Твой символ — это не случайность.\n"
                "Его можно носить как напоминание о том,\n"
                "каким ты выбираешь быть в этом году."
            ),
            "images": [
                "heart1.jpg",
                "heart2.jpg",
                "heart3.jpg"
                "heart4.jpg"
            ]
        },

        "fire": {
            "text": (
                "🔥 **Твой символ года — Огонь**\n\n"
                "Год силы и трансформации.\n"
                "Про смелость, честные решения и отказ от того,\n"
                "что больше не твоё.\n\n"
                "🐦‍🔥 Украшение с этим символом —\n"
                "якорь твоей внутренней энергии.\n\n"
                "Твой символ — это не случайность.\n"
                "Его можно носить как напоминание о том,\n"
                "каким ты выбираешь быть в этом году."
            ),
            "images": [
                "fire1.jpg",
                "fire2.jpg",
                "fire3.jpg"
                "fire4.jpg"
            ]
        },

        "star": {
            "text": (
                "🌟 **Твой символ года — Звезда**\n\n"
                "Год ориентира и внутреннего света.\n"
                "Даже если путь не до конца ясен,\n"
                "ты уже движешься в верном направлении.\n\n"
                "💫 Украшение со звездой —\n"
                "напоминание о надежде, вере в себя\n"
                "и своём пути.\n\n"
                "Твой символ — это не случайность.\n"
                "Его можно носить как напоминание о том,\n"
                "каким ты выбираешь быть в этом году."
            ),
            "images": [
                "star1.jpg",
                "star2.jpg",
                "star3.jpg"
                "star4.jpg"
            ]
        },

        "shield": {
            "text": (
                "🛡️ **Твой символ года — ЩИТ / ОБЕРЕГ**\n\n"
                "Год устойчивости и заботы о себе.\n"
                "Про границы, безопасность и опору внутри.\n\n"
                "✨ Украшение-оберег —\n"
                "тихое напоминание, что ты под защитой.\n\n"
                "Твой символ — это не случайность.\n"
                "Его можно носить как напоминание о том,\n"
                "каким ты выбираешь быть в этом году."
            ),
            "images": [
                "shield1.jpg",
                "shield2.jpg",
                "shield3.jpg"
                "shield4.jpg"
            ]
        }
    }

    await call.message.answer(results[symbol], parse_mode="Markdown")
    await state.clear()
    await call.answer()


# ---------- Запуск ----------
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
