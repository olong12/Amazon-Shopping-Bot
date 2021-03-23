import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='!')
SHOPPINGLIST = []

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Shopper Bot discord server \n{help()}'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message_content = message.content.lower().strip()
    if message_content.startswith('add'):
        response = add(message_content.split()[1:])
        await message.channel.send('__**' + response + '**__')
    elif message_content.startswith('random'):
        response = random_line()
        await message.channel.send('__**' + response + '**__')
    elif message_content.startswith('remove'):
        response = remove(message_content.split()[1:])
        await message.channel.send('__**' + response + '**__')
    elif message_content.startswith('list'):
        for i in SHOPPINGLIST:
            items = "".join(i)
            await message.channel.send('__**' + items + '**__')
    elif message_content.startswith('write'):
        with open("search_results_urls.txt", "w") as sru:
            sru.write("\n".join(SHOPPINGLIST))
        await message.channel.send("The item(s) have been written to a text file.")
    elif message_content == 'help':
        response = help()
        await message.channel.send(response)

@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

def add(item):
    if len(item) >= 1:
        items = '+'.join(item)
        webpage = 'https://www.amazon.com/s?k={0}'.format(items)
        SHOPPINGLIST.append(webpage)
        return ' '.join(item) + " has been added to the list!"
    else:
        return 'Retype your item'

def remove(item):
    if len(item) >= 1:
        items = '+'.join(item)
        webpage = 'https://www.amazon.com/s?k={0}'.format(items)
        if webpage in SHOPPINGLIST:
            SHOPPINGLIST.remove(webpage)
            return ' '.join(item) + " has been removed from the list!"
        else:
            return 'Item is not part of list.'
    else:
        return 'Retype your item'

def random_line(afile='test.txt', default=None):
    line = default
    for i, aline in enumerate(afile, start=1):
        if randrange(i) == 0:  # random int [0..i)
            line = aline
    return line

#HELP
def help():
    help = "_***WELCOME TO Amazon Shopper Bot! CHECK OUT COMMANDS AND MORE @ GITHUB: https://github.com/olong12/Amazon-Shopping-Bot/ ***_\n"
    return help

client.run(TOKEN)
