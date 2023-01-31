import telethon.types
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest
import resource
import pathlib
import os
import asyncio
import config


async def add(source_channel, destination_channel, client):
    channel_entity = await client.get_entity(source_channel)
    destination_channel = await client.get_entity(destination_channel)
    posts = await client(GetHistoryRequest(
        peer=channel_entity,
        limit=100,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0))
    my_posts = await client(GetHistoryRequest(
        peer=destination_channel,
        limit=100,
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
            print(f'Копирование {i}-ого поста с канала {channel_entity.title} в канал {destination_channel.title}')
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


async def bladee(task: str, client):
    if task.split(' ')[0] == '/add':
        function, source_channel, destination_channel = task.split(' ')
        await add(source_channel, destination_channel, client)
        # client.loop.run_until_complete(add(source_channel, destination_channel, client))

if __name__ == '__main__':
    print(123)
    client = TelegramClient(f'telegram', config.api_id, config.api_hash)
    client.start()
    print(228)
    asyncio.run(add('https://t.me/OnlyFansHDR', 'https://t.me/astrology15', client))
