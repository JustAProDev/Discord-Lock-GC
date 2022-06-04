import asyncio
import discord
import requests
import json
from discord.ext import commands
from discord.utils import get

token = "yourtokenhere"

Tokon = commands.Bot(description='Yurei', command_prefix=';', self_bot=True)

Tokon.lockgc = []
Tokon.headers = {
    'authorization': token,
}

@Tokon.event
async def lockloop():
    while True:
        if not Tokon.lockgc == []:
            for gcid in Tokon.lockgc:
                response = requests.put(f'https://discordapp.com/api/v8/channels/{gcid}/recipients/1337',headers=Tokon.headers)
                if response.status_code == 429:
                    response_c = response.text
                    response_content = json.loads(response_c)
                    lockedsec = response_content.get('retry_after')
                else:
                    headers = {"Authorization": token}
                    payload = {"content": "__**successfully Locked GC Master Yurei !**__", "nonce": gcid}
                    response = requests.post(url=f'https://discord.com/api/v9/channels/{gcid}/messages', headers=headers, json=payload)
                    for i in range(30):
                        response = requests.put(f'https://discordapp.com/api/v8/channels/{gcid}/recipients/1337',headers=Tokon.headers)
        await asyncio.sleep(0.8)

@Tokon.event
async def on_connect():
  print("Connected Master !")
  await lockloop()

@Tokon.command()
async def lock(ctx, groupid):
    Tokon.lockgc.extend([groupid] * 1)


@Tokon.command()
async def unlock(ctx, groupid=None):
    await ctx.send('__**Unlocked the Group Master !**__')
    if groupid:
        Tokon.lockgc.pop(groupid)
        print(f'Unlocking {groupid} in 120 seconds Master Yurei !')
    else:
        Tokon.lockgc.clear()
        print(f'Unlocked All Groups')

Tokon.run(token, bot=False, reconnect=True)
