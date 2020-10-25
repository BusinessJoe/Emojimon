import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import random
from guess import guess_poke
import json

TOKEN = ""

client = commands.Bot(command_prefix='!em')

trainers = {}


@client.event
async def on_ready():
    """Tells me the bot is now ready to start using. Start the spawn coroutine loop.
    """
    print("A wild game idea has appeared")


@client.command()
async def begin_hunt(ctx):
    spawn_loop.start()


@client.command()
async def spotted(ctx):
    """A testing function to make sure bot is working as intended
    """
    await spawn()


@client.command()
async def guess(ctx):
    msg = await ctx.send(guess_poke(
        'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/microsoft/209/reversed-hand-with-middle-finger-extended_1f595.png'))

    def check(reaction, user):
        return reaction.message.id == msg.id and user != client.user and str(reaction.emoji) == '🖕'
    # This portion will later be change so it can work on all supported emojis
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
        await ctx.send(f'Congrats {user.name}, you have been using discord way too much')
    except asyncio.TimeoutError:
        await ctx.send('Oh well, guess y\'all just dumb')


@client.command()
async def new_trainer(ctx):
    global trainers
    trainers[ctx.message.author.id] = []
    await ctx.send(f'Welcome to the club, starts by catching emojimons as they spawn randomly')


@tasks.loop(seconds=10)
async def spawn_loop():
    rand = random.randint(1, 6)
    if rand == 6:
        await spawn()
    else:
        pass


async def spawn():
    """Responsible for spawning a pokemon. Spawn windows starts every 10 seconds for testing purposes.
    """
    global trainers
    channel = client.get_channel(746939037297934426)
    emoji = client.get_emoji(769571475061473302)

    embed_item = discord.Embed(
        title="A wild middle finger has appeared", description="Catch it",
        color=0xffff00,
        url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    )
    embed_item.set_thumbnail(  # This portion should be taken from the json file
        url='https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/microsoft/209/reversed-hand-with-middle-finger-extended_1f595.png')
    msg = await channel.send(embed=embed_item)
    await msg.add_reaction(emoji)

    def check(reaction, user):
        return reaction.message.id == msg.id and user != client.user

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=5.0, check=check)
        await user.send('The pokemon got away')
        if user.id in trainers:
            await channel.send(f'{user.name} has caught the pokemon')
            trainers[user.id].append('🖕')  # This will probably be replaced with sth from the json file
            print(trainers)
        else:
            await reaction.message.channel.send('Oops, it looks like you\'r not a trainer yet, and thus not qualified'
                                                'to catch this emojimon. Join the club using new_trainer command.')
    except asyncio.TimeoutError:
        await msg.channel.send('The pokemon slipped away')


client.run(TOKEN)
