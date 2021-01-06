import discord
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
import asyncio
import random
from image_edit import guess_poke, battle_screen
from battle_calc import damage_calculation
import pickle
import time
import os
from datetime import datetime
from emojimon import Emoji, move, Trainer

TOKEN = os.environ["DISCORD_TOKEN"]

client = commands.Bot(command_prefix='!em')
emoji_list = []
trainer_list = []
trainer_id_list = []
local_time = ''


@client.event
async def on_ready():
    """Tells me the bot is now ready to start using. Start the spawn coroutine loop.
    """
    global emoji_list
    global trainer_list
    global trainer_id_list
    global local_time

    print("A wild game idea has appeared")
    with open("CompleteEmojiDex.dat", "rb") as f:
        emoji_list = pickle.load(f)

    with open("TrainerList.dat", "rb") as f:
        trainer_list = pickle.load(f)

    trainer_id_list = [i.id for i in trainer_list]
    local_time = datetime.now()


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
    todo: implement radar chart from matplotlib to generate visuals on emojimon's powers
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
    """
    Command for challenging another user
    :param ctx: context parameter
    :param target: the challenged user
    todo: Get emoji index from player
    todo: Restrict player from challenging self (unless if that player is me, because bug testing duh)
    todo: Add restrictions to ability usage
    """
    global trainer_id_list
    global trainer_list
    global emoji_list
    global local_time

    reactions = ["👍", "👎"]
    responses = ["yes", "no"]

    if ctx.author.id not in trainer_id_list:
        msg = await ctx.send(f"{ctx.author.name}, you are not currently a trainer, do you want to join?")
        answer = await select_one_from_list(ctx, ctx.author, responses, reactions, selection_message=msg)
        if answer == "yes":
            trainer_list.append(Trainer(ctx.author.name, ctx.author.id, emoji_list[0], local_time.strftime("%x")))
            trainer_id_list.append(ctx.author.id)
            with open('TrainerList.dat', 'wb') as f:  # AUTOSAVES!!!
                pickle.dump(trainer_list, f)

            await ctx.send(f"Welcome to the club {ctx.author.name}. Let's get going with your challenge.")
        else:
            await ctx.send(f'Then why tf did you even challenge?')
            return

    try:
        user = client.get_user(int(''.join([i for i in target if i.isdigit()])))
    except:
        await ctx.send("Target is not valid, make sure you are mentioning them with '@'")
        return

    if user == client.user:  # If the challenger is dumb enough to challenge a bot
        await ctx.send("No you dumbass I'm the referee not the player")
        return

    if user.id not in trainer_id_list:
        msg = await user.send(f"{user.name}, you are not currently a trainer, do you want to join?")
        answer = await select_one_from_list(user, user, responses, reactions, selection_message=msg)
        if answer == "yes":
            trainer_list.append(Trainer(user.name, user.id, emoji_list[0], local_time.strftime("%x")))
            trainer_id_list.append(user.id)
            with open('TrainerList.dat', 'wb') as f:  # AUTOSAVES!!!
                pickle.dump(trainer_list, f)
            await user.send(f"Welcome to the club {user.name}.")
            await ctx.send(f"Welcome to the club {user.name}.")
        else:
            await user.send(f'Alright then, guess not')
            await ctx.send(f'{user.name} cannot accept the challenge as he/she/they/pronoun is not a trainer.')
            return

    await ctx.send(f"{ctx.author.name} has challenged {user.name} to a battle.")
    msg = await user.send(f'{ctx.author.name} has challenged you to a battle. Do you accept?')

    answer = await select_one_from_list(user, user, responses, emojis=reactions, selection_message=msg)
    if answer == responses[0]:
        await battle(ctx, ctx.author, user)
    elif answer == responses[1]:
        await ctx.send(f'{user.name} has turned down the challenge.')


async def battle(ctx, challenger, challenged):
    """
    Battle Sequence
    :param ctx: context parameter
    :param challenger, challenged: respective players in the battle
    :param index1: Index of challenger's emoji
    :param index2: Index of challenged emoji
    todo: Can I somehow make this a looping coroutine? Not even sure if doing that would be beneficial
    todo: Basically the whole battle sequence
    todo: Reference the emoji from the player's inventory instead of the index, as well as add trainer pass for battle
    """
    global emoji_list
    global trainer_list
    global trainer_id_list

    challenger_emoji = trainer_list[trainer_id_list.index(challenger.id)].team[0]
    challenged_emoji = trainer_list[trainer_id_list.index(challenged.id)].team[0]

    index1 = challenger_emoji.emojiNumber
    index2 = challenged_emoji.emojiNumber

    msg = await ctx.send(f"Battle's starting! {challenger.name} has summoned {challenger_emoji.name}")
    image = await ctx.send(file=discord.File(fp=battle_screen(index1), filename='image.jpeg'))
    await asyncio.sleep(3)
    await msg.delete()
    await image.delete()

    msg = await ctx.send(f"{challenged.name} has summoned {challenged_emoji.name}")  # Referencing emoji from index
    image = await ctx.send(
        file=discord.File(fp=battle_screen(index1, index2),
                          filename='image.jpeg')
        )
    await asyncio.sleep(3)
    await msg.delete()
    await image.delete()

    challenger_hp = challenger_emoji.maxHp
    challenged_hp = challenged_emoji.maxHp

    # The list of moves available to each players
    # Moves are referenced by name, so todo: reference moves in emoji class as actual move object
    challenger_moves = \
        [challenger_emoji.move1, challenger_emoji.move2, challenger_emoji.move3, challenger_emoji.move4]
    challenged_moves = \
        [challenged_emoji.move1, challenged_emoji.move2, challenged_emoji.move3, challenged_emoji.move4]

    while True:
        move_chosen = await select_one_from_list(ctx, challenger, challenger_moves)
        msg = await ctx.send(f"{challenger_emoji.name} used {move_chosen}")
        image = await ctx.send(file=discord.File(fp=battle_screen(index1, index2, "gun1"), filename='Image.jpeg'))
        calc = damage_calculation(challenger_emoji, challenged_emoji, move_chosen)
        challenged_hp -= calc[1]  # This is the damage dealt

        await asyncio.sleep(3)
        await msg.delete()
        msg = await ctx.send(
            f"The move was {calc[0]}, dealt {calc[1]} damage. {challenged_emoji.name} has {challenged_hp} hp left"
        )
        if challenged_hp <= 0:
            await ctx.send(f'{challenged_emoji.name} has fallen into depression')
            break
        await asyncio.sleep(3)
        await msg.delete()  # Delete message to avoid spamming chat
        await image.delete()

        # Challenged trainer's turn
        move_chosen = await select_one_from_list(ctx, challenged, challenged_moves)
        msg = await ctx.send(f"{challenged_emoji.name} used {move_chosen}")
        # No need for a second move_chosen cuz it's turn_based anyways
        image = await ctx.send(file=discord.File(fp=battle_screen(index1, index2, "knife2"), filename='Image.jpeg'))
        calc = damage_calculation(challenged_emoji, challenger_emoji, move_chosen)
        challenger_hp -= calc[1]
        await asyncio.sleep(3)
        await msg.delete()
        msg = await ctx.send(
            f"The move was {calc[0]}, dealt {calc[1]} damage. {challenger_emoji.name} has {challenger_hp} hp left"
        )
        if challenger_hp <= 0:
            await ctx.send(f'{challenger_emoji.name} has fallen into depression')
            break
        await asyncio.sleep(3)
        await msg.delete()
        await image.delete()


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
        messages = [f"{author.name}, choose the following:"]
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
