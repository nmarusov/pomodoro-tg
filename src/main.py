"""Телеграм-бот для получения исторических справок."""

import os
from asyncio import sleep
from telethon import TelegramClient, events

POMODORO = 25 * 60
SMALL_REST = 5 * 60
BIG_REST = 15 * 60

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

if os.path.exists(dotenv_path):
    from dotenv import load_dotenv

    load_dotenv(dotenv_path)

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")

bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

cmd_stop = False
task_time = 0


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    """Send a message when the command /start is issued."""
    await event.respond("Вас приветствует бот Помодоро от Санька!")
    await timer()
    raise events.StopPropagation


# @bot.on(events.NewMessage)
# async def query(event):
#     await event.respond("Работает!")


@bot.on(events.NewMessage(pattern="/reset"))
async def reset(event):
    """
    State:
    0 - первый помидор
    1 - первый маленький отдых
    2 - второй помидор
    3 - второй маленький отдых
    4 - третий помидор
    5 - третий маленький отдых
    6 - четвёртый помидор
    7 - большой отдых
    """
    global cmd_stop, task_time

    def next_state():
        global task_time
        nonlocal state

        task_time = 0
        state = (state + 1) % 8

    await event.respond("Начата новая задача.")
    state = 0
    cmd_stop = False
    task_time = 0

    while True:
        if state == 6:
            if task_time == POMODORO:
                await event.respond("Пора сделать большой перерыв.")
                next_state()
        elif state == 7:
            if task_time == BIG_REST:
                await event.respond("Приступайте к работе.")
                next_state()
        elif state % 2 == 0:
            if task_time == POMODORO:
                await event.respond("Пора сделать маленький перерыв.")
                next_state()
        elif state % 2 != 0:
            if task_time == SMALL_REST:
                await event.respond("Приступайте к работе.")
                next_state()

        if cmd_stop:
            return

        await sleep(1)  # 1 секунда


@bot.on(events.NewMessage(pattern="/stop"))
async def stop(event):
    global cmd_stop
    cmd_stop = True
    await event.respond("Таймер остановлен.")


async def timer():
    global task_time

    while True:
        await sleep(1)  # 1 секунда
        task_time += 1
        print(task_time)


def main():
    """Start the bot."""
    print("Starting the bot...")
    bot.run_until_disconnected()
    print("Bye!")


if __name__ == "__main__":
    main()
