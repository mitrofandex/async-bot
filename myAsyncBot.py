from pyrogram import Client, MessageHandler, Filters
from pyrogram.errors import UsernameNotOccupied, ChatAdminRequired
import config
from time import time
import asyncio

api_id = config.api_id
api_hash = config.api_hash

app = Client("PyroBot", api_id, api_hash, bot_token=config.token)

async def get_participants(group):
    participants = []

    async def get_chunk(group, offset):
        chunk = await app.get_chat_members(group, offset=offset)
        participants.extend(chunk)

    total = await app.get_chat_members_count(group)
    print(f'Total: {total}')
    tasks = []
    for offset in range(0, total, 200):
        tasks.append(asyncio.create_task(get_chunk(group, offset)))

    await asyncio.gather(*tasks)

    return participants


@app.on_message(Filters.command('start'))
async def start(client, message):
    await message.reply_text(
        f'Hi! This bot can find users who participate at least in two of groups listed. Simply type /get group_1 group_2 ... group_n.')


@app.on_message(Filters.command("get"))
async def get(client, message):
    _, *group_names = message.command

    if len(group_names) < 2:
        await message.reply_text('Specify at least 2 groups.')
        return

    for gname in group_names:
        try:
            await app.get_chat_members(gname)
        except UsernameNotOccupied:
            await message.reply_text(f'The username {gname} is not occupied by anyone. Try again.')
            return
        except Exception:
            await message.reply_text(f'{gname} is a channel, private group or user. Try again.')
            return

    await message.reply_text('Just a second...')


    all_users = set()
    groups = {}
    for gname in group_names:
        pc = await get_participants(gname)
        groups[gname] = set([chatmember.user.id for chatmember in pc])
        all_users |= set((chatmember.user.username, chatmember.user.id) for chatmember in pc)
    
    response = []
    for user in all_users:
        gcount = 0
        if user[0] is None:
            continue
        gs = []
        for gname in groups:
            if user[1] in groups[gname]:
                gcount += 1
                gs.append(f'{gname}')
        
        if gcount >= 2:
            s = f'{user[0]} - ' + ', '.join(gs)
            response.append(s)

    with open(f'results/result-{message.from_user.id}.txt', 'w') as file:
        file.write('\n'.join(response))

    await message.reply_document(f'results/result-{message.from_user.id}.txt')

        
app.run()
