import discord
import time
import keyboard
import pydirectinput
import random
import pyautogui
import concurrent.futures
from CordPlays_KeyCodes import *

# Listens for a message event

client = discord.Client()
new_messages = list()
MAX_QUEUE_LENGTH = 2
MAX_WORKERS = 100
MESSAGE_RATE = 0.5
last_time = time.time()

active_tasks = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)


@client.event
async def on_ready():
    print('Bot is now online and ready to roll')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    try:
        msg = message.content

        if len(new_messages) < MAX_QUEUE_LENGTH:
            print("Got the message: " + msg)
            new_messages.append(msg)
            print(new_messages)
            handle_tasks(active_tasks, last_time)

    except Exception as e:
        print("Encountered exception 1: " + str(e))


def handle_message(message):
    try:
        if message == 'hello':
            time.sleep(1)
            print("hello")
            #message.channel.send('Hi')

        if message == "test":
            print("test")
            time.sleep(5)
            #message.channel.send('test')
            HoldAndReleaseKey(A, 2)
    except Exception as e:
        print("Encountered exception: " + str(e))


def handle_tasks(local_active_tasks, local_last_time):
    local_active_tasks = [t for t in local_active_tasks if not t.done()]

    messages_to_handle = list()

    if not new_messages:
        local_last_time = time.time()
    else:
        r = 1 if MESSAGE_RATE == 0 else (time.time() - local_last_time) / MESSAGE_RATE
        n = int(r * len(new_messages))
        if n > 0:
            messages_to_handle = new_messages[0:n]
            del new_messages[0:n]
            local_last_time = time.time()

    if not messages_to_handle:
        return
    else:
        for message in messages_to_handle:
            if len(local_active_tasks) <= MAX_WORKERS:
                local_active_tasks.append(thread_pool.submit(handle_message, message))
            else:
                print("too many tasks and not enough workers")


discordToken = input("Enter Token: ")
while True:
    client.run(discordToken)
