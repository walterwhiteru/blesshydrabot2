import time

from config import *
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetHistoryRequest
import asyncio

client = TelegramClient(f'telegram', api_id, api_hash)
client.start()


async def delete(source_channel: str, limit: int = 100):
    source_channel_entity = await client.get_entity(source_channel)
    source_posts = await client(GetHistoryRequest(
        peer=await client.get_input_entity(source_channel_entity),
        limit=limit,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0))
    print('Deleting')
    await client.delete_messages(source_channel_entity, source_posts.messages)


if __name__ == '__main__':
    client.loop.run_until_complete(delete('https://t.me/astrology15', 2000))
