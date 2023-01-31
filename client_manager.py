import time
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest
from telethon import hints
import telethon
import resource
import os
import threading
from threading import Thread, enumerate
import config
import logging
logging.basicConfig(level=logging.DEBUG)


def get_entity(client: TelegramClient, username: str) -> 'hints.Entity':
    async def generator():
        return await client.get_entity(username)
    return client.loop.run_until_complete(generator())

async def add(client: TelegramClient, source_entity, destination_entity, limit: int = 100):
    posts = await client(GetHistoryRequest(
        peer=await client.get_input_entity(source_entity),
        limit=limit,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0))
    my_posts = await client(GetHistoryRequest(
        peer=await client.get_input_entity(destination_entity),
        limit=limit,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0))
    i = 0
    for message in reversed(posts.messages):
        try:
            i += 1
            print(f'Копирование {i}-ого поста с канала {source_entity.title} в канал {destination_entity.title}')
            if message.message:
                print(f'{message.message}')
            elif message.media:
                print(f'{type(message.media)}')
            flag = False
            for my_message in my_posts.messages[::-1]:
                try:
                    if my_message.message == message.message:
                        flag = True
                        break
                except:
                    pass
                try:
                    if my_message.media == message.media and message.media is not None:
                        flag = True
                        break
                except:
                    pass
            if flag:
                continue
            if not message.message and not message.media:
                continue
            if message.media:
                if isinstance(message.media, telethon.types.MessageMediaWebPage):
                    await client.send_message(destination_channel, message.message, buttons=message.buttons)
                    return
                await client.send_file(destination_channel, message.media, caption=message.message)
            else:
                await client.send_message(destination_channel, message.message, buttons=message.buttons)
        except:
            print('Не удалось отправить сообщение')
    print('qwe')
    time.sleep(10)
    print('asd')


async def meow(client: TelegramClient):
    await add(client, 'https://t.me/OnlyFansHDR', 'https://t.me/astrology15', 1)


if __name__ == '__main__':
    print(f'{resource.client_manager_welcome}')
    print(f'{resource.NSFW_ART()}')
    current_path = config.current_path
    pid = str(os.getpid())
    myclient = TelegramClient(f'telegram', config.api_id, config.api_hash)
    myclient.start()
    source_channel = 'https://t.me/OnlyFansHDR'
    destination_channel = 'https://t.me/astrology15'
    source_entity = get_entity(myclient, source_channel)
    destination_entity = get_entity(myclient, destination_channel)
    asyncio.run(meow(myclient))
