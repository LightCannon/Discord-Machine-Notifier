import discord
import asyncio
from dotenv import load_dotenv
import os
from datetime import datetime
from utils import *
import threading


"Designed by Camilo Mora and Developed by LightCannon"
# Create empty lists for machines
ActiveMachines = []
NonWorkingMachines = []

load_dotenv()
CHANNEL_ID = int(os.getenv('BOT_CHANNEL_ID'))
TIMEOUT = int(os.getenv('MACHINE_TIMEOUT'))
RISK_MARGIN_NOTIFICATION_SECONDS = int(os.getenv('RISK_MARGIN_NOTIFICATION_SECONDS'))
UPDATE_RATE = int(os.getenv('UPDATE_RATE'))
MSG_LIMIT = 50
READY = False

client = discord.Client(intents=discord.Intents.all())
emailer = EmailSender()
channel = None
lock = threading.Lock()

margin_risk = {}


@client.event
async def on_ready():
    global channel
    global READY
    
    print("Bot is ready")
    # Delete all messages in the channel when bot starts
    channel = client.get_channel(CHANNEL_ID)
    
    limit = 100
    while True:
        # async for msg in channel.history(limit=LIMIT):
        #     limit += 1
        #     
        # if limit == 0:
        #     break
        msgs = await channel.purge(limit=limit, bulk=True)
        print (len(msgs))
        await asyncio.sleep(1)
        limit = len(msgs)
        if limit == 0:
            break
    
    
    #m = await channel.purge(limit=MSG_LIMIT)
    #while len(m) > 0:
    #    m = await channel.purge(limit=MSG_LIMIT)
    #    await asyncio.sleep(0.05)

    print('All messages are deleted')
    READY = True
    # channel = client.get_channel(CHANNEL_ID)
    asyncio.ensure_future(check_machines_status())
    # await message.delete()

@client.event
async def on_message(message):
    if not READY:
        return
    
    messages_id = []
    
    if message.channel.id != CHANNEL_ID:
        return
    
    if channel is None:
        return
    # Get message ID and machine name
    message_id = message.id
    machine_name = message.content.split()[0]

    # if message.content.lower().find('risk of margin') > -1:
    #     if margin_risk.get(machine_name, None) is None:
    #         emailer.send_notification_msg(f"{machine_name} is at risk of marging")
    #         margin_risk[machine_name] = datetime.now()
    #         
    #     last_notification = datetime.now() - margin_risk[machine_name]
    #     delta_s = abs(last_notification.total_seconds())
    #     
    #     if delta_s >= RISK_MARGIN_NOTIFICATION_SECONDS:
    #         emailer.send_notification_msg(f"{machine_name} is at risk of marging")
    #         margin_risk[machine_name] = datetime.now()
    # else:
    #     # check if we were at risk of margining before
    #     if margin_risk.get(machine_name, None) is not None:
    #         emailer.send_notification_msg(f"{machine_name} has avoided risk of marging")
    #         del margin_risk[machine_name]

    # Get all messages in channel that have the same machine name
    async for m in channel.history(limit=None):
        if m.content.split()[0] == machine_name:
            messages_id.append(m.id)

    # Delete all messages in the channel except the last one
    for id in messages_id:
        if id != message_id:
            msg = await channel.fetch_message(id)
            await msg.delete()
    
    # Check if machine name is not in ActiveMachines
    if machine_name not in ActiveMachines:
        lock.acquire()
        ActiveMachines.append(machine_name)
        emailer.send_notification_msg(f'{machine_name} Started to work')
        lock.release()
        
        
async def check_machines_status():
    global channel
    while True:
        lock.acquire()
        machines = {k:None for k in ActiveMachines}
        lock.release()
        current_time = datetime.now()
        async for message in channel.history(limit=None):
            msg_machine = message.content.split()[0]
            
            # for machine_name in ActiveMachines:
            if machines.get(msg_machine, None) is None:
                machines[msg_machine] = message.created_at
            
            if len([k for k,v in machines.items() if v is None]) == 0:
                break
            
        for machine,msg_time in machines.items():
            if msg_time is None:
                continue
            delta = current_time - datetime_from_utc_to_local(msg_time)
            delta_s = abs(delta.total_seconds())
            if delta_s > TIMEOUT and machine not in NonWorkingMachines:
                # print(delta.seconds )
                NonWorkingMachines.append(machine)
                emailer.send_notification_msg(f"{machine} is not working")
            
            elif delta_s < TIMEOUT and machine in NonWorkingMachines:
                NonWorkingMachines.remove(machine)
                emailer.send_notification_msg(f"{machine} is working again")
                
        await asyncio.sleep(UPDATE_RATE)
            


client.run(os.getenv('BOT_TOKEN'))