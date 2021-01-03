import discord
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
import asyncio
import random
from image_edit import guess_poke, battle_screen
import pickle
import time
from emojimon import Emoji

TOKEN = ""

client = commands.Bot(command_prefix='!em')
emoji_list = []
trainers = {}


@client.event
async def on_ready():
    """Tells me the bot is now ready to start using. Start the spawn coroutine loop.
    """
    global emoji_list
    print("A wild game idea has appeared")
    with open("CompleteEmojiDex.dat", "rb") as f:
        emoji_list = pickle.load(f)


@client.command()
async def begin_hunt(ctx):
    """Does exactly what it says: starting the spawn loop
    """
    spawn_loop.start()


@client.command()
async def spotted(ctx):
    """A testing function for spawning to make sure bot is working as intended
    """
    await spawn()


@client.command()
async def guess(ctx):
    """Good ol' guess the pokemon
    """
    await ctx.send("Time for guess the pokemon!")
    msg = await ctx.send(file=discord.File(
        fp=guess_poke(
        'https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/microsoft/209/reversed-hand-with-middle-finger-extended_1f595.png'),
        filename='image.jpeg'
        )
    )

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
    """Adds new trainer to the game
    """
    global trainers
    trainers[ctx.message.author.id] = []
    await ctx.send(f'Welcome to the club, starts by catching emojimons as they spawn randomly')
    role = discord.utils.get(ctx.message.guild.roles, name='Trainer')
    await ctx.message.author.add_roles(role)


@tasks.loop(seconds=10)
async def spawn_loop():
    """The loop coroutine for spawning, it will have a chance of 1/6 every 10 seconds
    """
    rand = random.randint(1, 6)
    if rand == 6:
        await spawn()
    else:
        pass


async def spawn():
    """Responsible for spawning a pokemon. Spawn windows starts every 10 seconds for testing purposes.
    todo: implement pickle instead of json to gain access to the object instead of its list of attributes
    """
    global trainers
    global emoji_list
    channel = client.get_channel(746939037297934426)
    pokeball = client.get_emoji(769571475061473302)

    emoji = random.choice(emoji_list)

    embed_item = discord.Embed(
        title=f"A wild {emoji.name} has appeared", description="Catch it",
        color=0xffff00,
        url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    )
    embed_item.set_thumbnail(  # todo: Find a way to upload .jpg from pc
        url='https://drive.google.com/file/d/1ndOhQuMxfr2pa3WWR3_-MU9JdfjcPW4K/view?usp=sharing')
    msg = await channel.send(embed=embed_item)
    await msg.add_reaction(pokeball)

    def check(reaction, user):
        return reaction.message.id == msg.id and user != client.user

    role = discord.utils.get(msg.guild.roles, name='Trainer')
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=5.0, check=check)
        if role in user.roles:
            await user.send('You got the pokemon, you\'re now responsible for its taxes')
            await channel.send(f'{user.name} has caught the pokemon')
            trainers[user.id].append(emoji.emojiNumber)  # This will probably be replaced with sth from the json file
            print(trainers)
        else:
            await reaction.message.channel.send('Oops, it looks like you\'re not a trainer yet, and thus not qualified '
                                                'to catch this emojimon. Join the club using new_trainer command.')
    except asyncio.TimeoutError:
        await msg.channel.send('The pokemon slipped away')


@client.command()
async def battle_challenge(ctx, target):
    if ctx.author == client.user:  # In the unlikely situation that the message is written by a bot
        return

    try:
        user = client.get_user(int(target[3:-1]))
    except:
        await ctx.send("Target is not valid, make sure you are mentioning them with '@'")

    if user == client.user:
        await ctx.send("No you dumbass I'm the referee not the player")
        return

    await ctx.send(f"{ctx.author.name} has challenged {user.name} to a battle.")
    msg = await user.send(f'{ctx.author.name} has challenged you to a battle. Do you accept?')

    reactions = ["👍", "👎"]
    responses = ["yes", "no"]

    answer = await select_one_from_list(user, user, responses, emojis=reactions, selection_message=msg)
    if answer == responses[0]:
        await battle(ctx, ctx.author, user, 0, 1)
    elif answer == responses[1]:
        await ctx.send(f'{user.name} has turned down the challenge.')


async def battle(ctx, challenger, challenged, index1, index2):
    """
    Battle Sequence
    :param ctx: context parameter
    :param challenger, challenged: respective players in the battle
    :param index1: Index of challenger's emoji
    :param index2: Index of challenged emoji
    :return:
    """
    global emoji_list
    msg = await ctx.send(f"Battle's starting! {challenger.name} has summoned {emoji_list[index1].name}")
    image = await ctx.send(file=discord.File(fp=battle_screen(index1), filename='image.jpeg'))
    time.sleep(3)
    await msg.delete()
    await image.delete()

    msg = await ctx.send(f"{challenged.name} has summoned {emoji_list[index2].name}")
    image = await ctx.send(file=discord.File(fp=battle_screen(index1, index2), filename='image.jpeg'))


async def select_one_from_list(messageable, author, lst, emojis=None, selection_message=None):
    """
    Lets a discord user select an item from a list using reactions.
    Returns the selected item.
    Can raise ValueError and asyncio.TimeoutError.
    """
    if emojis is None:
        emojis = ['0️⃣',
                  '1️⃣',
                  '2️⃣',
                  '3️⃣',
                  '4️⃣',
                  '5️⃣',
                  '6️⃣',
                  '7️⃣',
                  '8️⃣',
                  '9️⃣']
        emojis = emojis[:len(lst)]

    if len(lst) != len(emojis):
        raise ValueError(f'Lengths of lst and emojis are not equal ({len(lst)} != {len(emojis)})')

    if selection_message is None:
        # concatenate each line into a single message before sending
        messages = []
        for emoji, item in zip(emojis, lst):
            messages.append(f'{emoji} {item}')
        selection_message = await messageable.send('\n'.join(messages))

    # react with one emoji for each item
    for emoji in emojis:
        await selection_message.add_reaction(emoji)

    # wait for confirmation from author
    def check(reaction, user):
        return user == author and reaction.message.id == selection_message.id and str(reaction.emoji) in emojis

    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

    selected = lst[emojis.index(str(reaction.emoji))]
    return selected


client.run(TOKEN)
