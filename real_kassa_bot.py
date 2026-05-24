import os
# real_kassa_bot.py
import json
import random
from datetime import datetime, time

from telegram import (
    ReplyKeyboardMarkup,
    Update,
    BotCommand,
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN = os.getenv("TOKEN")
ADMIN_ID = 7400308603

months = [
    "Январь",
    "Февраль",
    "Март",
    "Апрель",
    "Май",
    "Июнь",
    "Июль",
    "Август",
    "Сентябрь",
    "Октябрь",
    "Ноябрь",
    "Декабрь",
]

friends = []
payments = {}
history = []

history_month_index = datetime.now().month % 12

current_queue = []
current_index = 0


# =========================
# SAVE / LOAD FRIENDS
# =========================


def save_friends():

    with open("friends.json", "w", encoding="utf-8") as file:
        json.dump(friends, file, ensure_ascii=False)



def load_friends():

    global friends

    try:
        with open("friends.json", "r", encoding="utf-8") as file:
            friends = json.load(file)

    except:
        friends = []


# =========================
# SAVE / LOAD PAYMENTS
# =========================


def save_payments():

    with open("payments.json", "w", encoding="utf-8") as file:
        json.dump(payments, file, ensure_ascii=False)



def load_payments():

    global payments

    try:
        with open("payments.json", "r", encoding="utf-8") as file:
            payments = json.load(file)

    except:
        payments = {}


# =========================
# SAVE / LOAD QUEUE
# =========================


def save_queue():

    data = {
        "queue": current_queue,
        "index": current_index,
    }

    with open("queue.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)



def load_queue():

    global current_queue
    global current_index

    try:
        with open("queue.json", "r", encoding="utf-8") as file:

            data = json.load(file)

            current_queue = data["queue"]
            current_index = data["index"]

    except:
        current_queue = []
        current_index = 0


# =========================
# SAVE / LOAD HISTORY
# =========================


def save_history():

    with open("history.json", "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False)



def load_history():

    global history

    try:
        with open("history.json", "r", encoding="utf-8") as file:
            history = json.load(file)

    except:
        history = []

def load_month():

    global history_month_index

    try:

        with open("month.json", "r", encoding="utf-8") as file:

            data = json.load(file)

            history_month_index = data["month_index"]

    except:

        history_month_index = 4


def save_month():

    data = {
        "month_index": history_month_index
    }

    with open("month.json", "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )

# =========================
# START
# =========================

async def set_commands(app):

    commands = [

        BotCommand("start", "Запуск бота"),

        BotCommand("help", "Список команд"),
        
        BotCommand("join", "Вступить в кассу"),

        BotCommand("leave", "Выйти из кассы"),

        BotCommand("members", "Участники"),

        BotCommand("history", "История кассы"),

        BotCommand("nextmonth", "Следующий месяц"),
        
        BotCommand("finish", "Завершить кассу"),

        BotCommand("add", "Добавить участника"),

        BotCommand("remove", "Удалить участника"),
    ]

    await app.bot.set_my_commands(commands)
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = (
        "📘 Команды бота\n\n"

        "🎲 Касса:\n"
        "Жеребьёвка — создать новую кассу\n"
        "📅 Кто отвечает — текущий участник\n"
        "📅 Очередь — вся очередь\n"
        "📢 Напомнить — напоминание\n"
        "/nextmonth — следующий месяц\n"
        "/finish — завершить кассу\n\n"

        "💰 Оплаты:\n"
        "/pay Имя — отметить оплату\n"
        "/payments — список оплат\n\n"

        "👥 Участники:\n"
        "/join — вступить\n"
        "/leave — выйти\n"
        "/members — список участников\n"
        "/add Имя — добавить участника\n"
        "/remove Имя — удалить участника\n\n"

        "📜 История:\n"
        "/history — история кассы"
    )

    await update.message.reply_text(message)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["🎲 Жеребьёвка"],
        ["📅 Кто отвечает"],
        ["📋 Очередь"],
        ["📢 Напомнить"],
        ["📜 История"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    message = (
        "🤖 Добро пожаловать в Кассу\n\n"

        "📘 Что умеет бот:\n\n"

        "🎲 Жеребьёвка — создать кассу\n"
        "📅 Кто отвечает — текущий участник\n"
        "📋 Очередь — вся очередь\n"
        "📢 Напомнить — напоминание\n"
        "📜 История — прошлые кассы\n\n"

        "⚙️ Команды:\n"
        "/nextmonth — следующий месяц\n"
        "/finish — завершить кассу\n"
        "/help — все команды\n\n"

        "👥 Участие:\n"
        "/join — вступить в кассу\n"
        "/leave — выйти из кассы\n"
        "/members — список участников\n\n"

        "💰 Оплаты:\n"
        "/pay Имя\n"
        "/payments\n\n"

        "👇 Нажми кнопки ниже"
    )

    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
    )

# =========================
# ADD FRIEND
# =========================
async def add_friend(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        name = context.args[0]

        friends.append(name)

        save_friends()

        await update.message.reply_text(
            f"✅ {name} добавлен"
        )

    except:
        await update.message.reply_text(
            "❌ Используй: /add Имя"
        )


# =========================
# REMOVE FRIEND
# =========================


async def remove_friend(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        name = context.args[0]

        friends.remove(name)

        save_friends()

        await update.message.reply_text(
            f"❌ {name} удалён"
        )

    except:
        await update.message.reply_text(
            "❌ Человек не найден"
        )

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    
    user = update.effective_user

    name = user.username or user.first_name


    if name in friends:

        await update.message.reply_text(
            "⚠️ Ты уже участвуешь в кассе"
        )

        return

    friends.append(name)

    save_friends()

    await update.message.reply_text(
        f"✅ {name} теперь участвует в кассе"
    )


async def leave(update: Update, context: ContextTypes.DEFAULT_TYPE):

    
    user = update.effective_user

    name = user.username or user.first_name


    if name not in friends:

        await update.message.reply_text(
            "❌ Тебя нет в кассе"
        )

        return

    friends.remove(name)

    save_friends()

    await update.message.reply_text(
        f"👋 {name} вышел из кассы"
    )


# =========================
# MEMBERS
# =========================


async def members(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(friends) == 0:

        await update.message.reply_text(
            "❌ Список пуст"
        )

        return

    message = "👥 Участники\n\n"

    for name in friends:
        message += f"• {name}\n"

    await update.message.reply_text(message)

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        name = context.args[0]

        payments[name] = "✅"

        save_payments()

        await update.message.reply_text(
            f"💰 {name} оплатил кассу"
        )

    except:

        await update.message.reply_text(
            "❌ Используй: /pay Имя"
        )


async def show_payments(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = "💰 Оплаты\n\n"

    if len(payments) == 0:

        message += "Пока никто не оплатил"

    else:

        for name, status in payments.items():

            message += f"✅ {name}\n"

    await update.message.reply_text(message)

# =========================
# HISTORY
# =========================


async def show_history(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = "📜 История кассы\n\n"

    if len(history) == 0:

        message += "История пока пустая"

    else:

        for item in history:
            message += f"• {item}\n"

    await update.message.reply_text(message)


# =========================
# KASSA
# =========================

async def kassa(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global current_queue
    global payments
    global current_index
    global history_month_index

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "⛔ Только админ может запускать жеребьёвку"
        )

        return

    if current_queue:

        await update.message.reply_text(
            "⛔ Текущая касса ещё не завершена"
        )

        return

    payments = {}

    save_payments()

    current_queue = friends.copy()

    random.shuffle(current_queue)

    current_index = 0

    save_queue()

    message = "────────────\n"
    message += "🎲 КАССА\n"
    message += "────────────\n\n"

    for i, name in enumerate(current_queue, start=1):

        message += f"{i}️⃣ {name}\n"

    message += "\nУдачи 😎"

    await update.message.reply_text(message)

# =========================
# CURRENT PERSON
# =========================


async def next_person(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global current_index

    if len(current_queue) == 0:

        await update.message.reply_text(
            "❌ Очередь пока пустая"
        )

        return

    person = current_queue[current_index]

    await update.message.reply_text(
        f"📅 Сейчас отвечает: {person}"
    )


# =========================
# REMIND
# =========================


async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global current_index

    if len(current_queue) == 0:

        await update.message.reply_text(
            "❌ Очередь пока пустая"
        )

        return

    person = current_queue[current_index]

    await update.message.reply_text(
        f"📢 Напоминание: сейчас отвечает {person}"
    )


# =========================
# QUEUE
# =========================


async def queue(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(current_queue) == 0:

        await update.message.reply_text(
            "❌ Очередь пока пустая"
        )

        return

    message = "📅 Очередь по месяцам\n\n"

    month_index = history_month_index

    for i, name in enumerate(current_queue):

        message += f"{months[month_index]} — {name}\n"

        month_index = (month_index + 1) % 12

    await update.message.reply_text(message)


# =========================
# NEXT MONTH
# =========================

async def next_month(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global current_index
    global history_month_index

    if len(current_queue) == 0:

        await update.message.reply_text(
            "❌ Очередь пока пустая"
        )

        return

    history.append(
        f"{months[history_month_index]} — {current_queue[current_index]}"
    )

    save_history()

    current_index = (current_index + 1) % len(current_queue)

    history_month_index = (history_month_index + 1) % 12

    save_month()

    save_queue()

    if current_index == 0:

        current_queue.clear()

        save_queue()

        await update.message.reply_text(
            "✅ Касса завершена\n\n🎲 Сделайте новую жеребьёвку"
        )

    else:

        await update.message.reply_text(
            "➡️ Касса перешла к следующему человеку"
        )

async def finish_kassa(update: Update, context: ContextTypes.DEFAULT_TYPE):

    global current_queue
    global current_index
    global payments

    current_queue.clear()

    current_index = 0

    payments.clear()

    save_queue()

    save_payments()

    await update.message.reply_text(
        "❌ Текущая касса завершена"
    )

# =========================
# BUTTONS
# =========================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    user = update.effective_user

    name = user.username or user.first_name

    if name not in friends:

        await update.message.reply_text(
            "❗ Сначала вступите в кассу:\n/join"
        )

        return

    if text == "🎲 Жеребьёвка":

        await kassa(update, context)

    elif text == "📅 Кто отвечает":

        await next_person(update, context)

    elif text == "📋 Очередь":

        await queue(update, context)

    elif text == "📢 Напомнить":

        await remind(update, context)

    elif text == "📜 История":

        await show_history(update, context)

    else:

        await update.message.reply_text(
            "❓ Неизвестная команда"
        )


# =========================
# AUTO NEXT MONTH
# =========================


async def auto_next_month(context: ContextTypes.DEFAULT_TYPE):

    global current_index

    if len(current_queue) == 0:
        return

    current_index = (current_index + 1) % len(current_queue)

    save_queue()

async def auto_reminder(context: ContextTypes.DEFAULT_TYPE):

    if len(current_queue) == 0:
        return

    person = current_queue[current_index]

    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=(
            "💰 Напоминание о кассе\n\n"
            f"👤 Сейчас отвечает: {person}"
        )
    )

# =========================
# LOAD DATA
# =========================


load_payments()
load_friends()
load_queue()
load_history()
load_month()



# =========================
# APP
# =========================
# =========================
# APP
# =========================

app = Application.builder().token(TOKEN).build()

# COMMANDS
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))

app.add_handler(CommandHandler("join", join))
app.add_handler(CommandHandler("leave", leave))

app.add_handler(CommandHandler("members", members))

app.add_handler(CommandHandler("add", add_friend))
app.add_handler(CommandHandler("remove", remove_friend))

app.add_handler(CommandHandler("history", show_history))

app.add_handler(CommandHandler("pay", pay))
app.add_handler(CommandHandler("payments", show_payments))

app.add_handler(CommandHandler("nextmonth", next_month))
app.add_handler(CommandHandler("finish", finish_kassa))



# BUTTONS
app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        buttons
    )
)

# COMMAND MENU
app.post_init = set_commands

# AUTO JOBS
job_queue = app.job_queue

job_queue.run_monthly(
    auto_next_month,
    when=time(hour=18, minute=0),
    day=-1,
)

job_queue.run_daily(
    auto_reminder,
    time(hour=18, minute=0),
    days=(4,),
    chat_id=-1002569285133,
)

print("🤖 Бот запущен...")

app.run_polling()






