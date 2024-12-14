import discord
from discord.ext import commands
from discord.ui import Button, View

from traceback import format_exc

import json

from datetime import datetime as dt

from random import randint as rint

from requests import get
from bs4 import BeautifulSoup as BS

file = open('config.json', 'r', encoding='utf-8')
config = json.load(file)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
intents.typing = False
intents.guilds = True
intents.invites = True

bot = commands.Bot(config["prefix"], intents=intents)


@bot.event
async def on_ready():
    print('Да начнется магия!')


@bot.event
async def on_member_remove(member):
    """
Обрабатывает событие удаления участника из группу Discord.

Этот метод является обработчиком события, который вызывается, когда участник покидает гильдию. Он обновляет название канала с количеством участников в гильдии.

:param discord.Member member: Участник, который покинул группу.

:example:

>>> member = discord.Member
>>> on_member_remove(member)
>>> Поменяет текст канала с id 1274065202777952330 на f'members: {members}'
"""
    members = len(bot.get_guild(1261800835462074428).members)
    await bot.get_channel(1274065202777952330).edit(name=f'members: {members}')


@bot.event
async def on_member_join(member):
    """
Обрабатывает событие присоединения участника в группу Discord.

Эта функция добавляет нового участника в базу данных, дает ему стандартную роль, а также пишет в чат приветствие.

:param discord.Member member: Информация по участнику, который присоединился в группу.

example:

>>> member = discord.Member
>>> on_member_join(member)
>>> Добавит нового участника в базу данных, даст ему стандартную роль, а также напишет в чат приветствие.
    """
    try:
        with open("information.json", "r") as json_file:
            json_dict = json.load(json_file)

        member_id = str(member.id)

        if (member_id in json_dict["information"].keys()):
            json_dict["information"][member_id]["been"] += 1
            with open("information.json", "w") as json_file:
                json.dump(json_dict, json_file, indent=4)
            return await member.add_roles(discord.utils.get(member.guild.roles, id=1263194300301447198))

        members = len(bot.get_guild(1261800835462074428).members)

        with open("information.json", "r") as json_file:
            json_dict = json.load(json_file)

            json_dict["information"][member_id] = {"been": 1}

            json_dict["information"][member_id].update({"royals": 10})

            json_dict["information"][member_id].update({"invites": 0})

            json_dict["information"][member_id].update({"time": []})

            with open("information.json", "w") as json_file:
                json.dump(json_dict, json_file, indent=4)

        embed = discord.Embed(title=f'Добро пожаловать! Ты {members}th участник!',
                              description="",
                              color=discord.Color.blue())

        await bot.get_channel(1262414805801635911).send(member.mention, embed=embed)

        # роль skuf
        await member.add_roles(discord.utils.get(member.guild.roles, id=1263194300301447198))

        await bot.get_channel(1274065202777952330).edit(name=f'members: {members}')
    except:
        print(
            f'Ошибка в ивенте on_member_join\n{format_exc()}\n////////////////////////////////////////////////////////////////////////////////////////////')

# ADMIN_COMMAND


@bot.command(name="update_json")
async def update_json(ctx):
    """
Обрабатывает команду update_json.

Эта функция обновляет базу данных, добавляя в нее тех участников, которых в ней нет.

:param discord.Context ctx: Этот объект предоставляет информацию о контексте, в котором была вызвана команда, включая данные о сообщении, канале, авторе и сервере.

:example:

>>> ctx = discord.Context
>>> update_json(ctx)
>>> Изменит файл базы данных, добавив в него всех недостающих участников.
    """
    try:
        if "Direct Message with" in str(ctx.channel):
            return
        if ctx.author.id != 854662130682691585:
            return print(f'{ctx.author.global_name} с id: {ctx.author.id}, пытается использоваться команду update_json!\nДата: {dt.now()}')

        await ctx.channel.purge(limit=1)
        members = ctx.guild.members

        for member in members:
            member_id = str(member.id)

            with open("information.json", "r") as json_file:
                json_dict = json.load(json_file)

                if not (member_id in json_dict["information"].keys()):
                    json_dict["information"][member_id] = {"been": 1}

                    json_dict["information"][member_id].update({"royals": 10})

                    json_dict["information"][member_id].update({"invites": 0})

                    json_dict["information"][member_id].update({"time": []})

                    with open("information.json", "w") as json_file:
                        json.dump(json_dict, json_file, indent=4)
    except:
        print(
            f'Ошибка в команде update_json:\n{format_exc()}\n////////////////////////////////////////////////////////////////////////////////////////////')

# ADMIN_COMMAND


@bot.command(name="del")
async def delete(ctx, amount=0):
    """
Обрабатывает команду del.

Удаляет заданное количество сообщений.

:param discord.Context ctx: Этот объект предоставляет информацию о контексте, в котором была вызвана команда, включая данные о сообщении, канале, авторе и сервере..
:param int amount: Заданное количество удаляемых сообщений. (подефолту стоит 0)

:example:

>>> ctx = discord.Context
>>> amount = 1
>>> delete(ctx, 1)
>>> Удалит 1 сообщение.
    """
    try:
        if "Direct Message with" in str(ctx.channel):
            return
        if ctx.author.id != 854662130682691585:
            return print(f'{ctx.author.global_name} с id: {ctx.author.id}, пытается использоваться команду del!\nДата: {dt.now()}')
        await ctx.channel.purge(limit=amount + 1)
    except:
        print(
            f'Ошибка в команде del:\n{format_exc()}\n////////////////////////////////////////////////////////////////////////////////////////////')


@bot.command(name="royals")
async def get_user_royals(ctx):
    """
Обрабатывает команду royals.

Пишет участнику его количетсво виртуальной валюты.

:param discord.Context ctx: Этот объект предоставляет информацию о контексте, в котором была вызвана команда, включая данные о сообщении, канале, авторе и сервере..

:example:

>>> ctx = discord.Context
>>> get_user_royals(ctx)
>>> Напишет в чат количество виртуальной валюты у участника.
    """
    try:
        if "Direct Message with" in str(ctx.channel):
            return
        if ctx.channel.id != 1271812837928337408:
            return
        await ctx.channel.purge(limit=1)
        with open("information.json", "r") as json_file:
            json_dict = json.load(json_file)
            await ctx.send(f'{ctx.author.mention} у вас {json_dict["information"][str(ctx.author.id)]["royals"]} royal coins :gem:')
    except:
        print(
            f'Ошибка в команде royals:\n{format_exc()}\n////////////////////////////////////////////////////////////////////////////////////////////')

# ADMIN_COMMAND


@bot.command(name="duel")
async def delete(ctx, coins):
    """
Обрабатывает команду duel.

Создает сообщение с игрой на виртуальную валюту.

:param discord.Context ctx: Этот объект предоставляет информацию о контексте, в котором была вызвана команда, включая данные о сообщении, канале, авторе и сервере..
:param int coins: Ставка одной игры.

:example:

>>> ctx = discord.Context
>>> coins = 10
>>> delete(ctx, 10)
>>> Напишет в чат сообщение, в котором можно поиграть в дуэль на виртуальную валюту.
    """
    try:
        if "Direct Message with" in str(ctx.channel):
            return
        if ctx.author.id != 854662130682691585:
            return print(f'{ctx.author.global_name} с id: {ctx.author.id}, пытается использоваться команду duel!\nДата: {dt.now()}')
        if ctx.channel.id != 1265745725073920011:
            return
        await (await ctx.channel.fetch_message(ctx.message.id)).delete()

        with open("information.json", "r") as json_file:
            json_dict = json.load(json_file)
        for i in list(json_dict["games"]["duels"].keys()):
            json_dict["games"]["duels"].pop(i)
        await bot.get_channel(1265745725073920011).purge(limit=5)
        with open("information.json", "w") as json_file:
            json.dump(json_dict, json_file, indent=4)

        coins = int(coins)
        with open("information.json", "r") as json_file:
            json_dict = json.load(json_file)
        embed = discord.Embed(description=f"""
    Игра на {coins} royal coins

    Участник 1: -

    Участник 2: -""")

        async def join_button_callback(interaction: discord.interactions):
            with open("information.json", "r") as json_file:
                json_dict = json.load(json_file)
            if json_dict["information"][str(interaction.user.id)]["royals"] < coins:
                return
            if json_dict["games"]["duels"]["duel " + interaction.data.get("custom_id")]["players"] == 0:
                message = await bot.get_channel(1265745725073920011).fetch_message(json_dict["games"]["duels"]["duel " + interaction.data.get("custom_id")]["message_id"])
                embed = discord.Embed(description=f"""
    Игра на {coins} royal coins

    Участник 1: {interaction.user.global_name}

    Участник 2: -""")
                await message.edit(embed=embed)
                json_dict["games"]["duels"]["duel " + interaction.data.get("custom_id")].update(
                    {"first player nickname": interaction.user.global_name})
                json_dict["games"]["duels"]["duel " + interaction.data.get(
                    "custom_id")].update({"first player id": interaction.user.id})
                json_dict["games"]["duels"]["duel " +
                                            interaction.data.get("custom_id")]["players"] += 1
                with open("information.json", "w") as json_file:
                    json.dump(json_dict, json_file, indent=4)
            elif json_dict["games"]["duels"]["duel " + interaction.data.get("custom_id")]["players"] == 1:
                if json_dict["games"]["duels"]["duel " + interaction.data.get("custom_id")]["first player id"] == interaction.user.id:
                    return
                first_player_id = json_dict["games"]["duels"]["duel " +
                                                              interaction.data.get("custom_id")]["first player id"]

                message = await bot.get_channel(1265745725073920011).fetch_message(json_dict["games"]["duels"]["duel " + interaction.data.get("custom_id")]["message_id"])

                if json_dict["information"][str(first_player_id)]["royals"] < coins:
                    json_dict["games"]["duels"]["duel " + interaction.data.get(
                        "custom_id")]["first player nickname"] = interaction.user.global_name
                    json_dict["games"]["duels"]["duel " + interaction.data.get(
                        "custom_id")]["first player id"] = interaction.user.id
                    with open("information.json", "w") as json_file:
                        json.dump(json_dict, json_file, indent=4)
                    embed = discord.Embed(description=f"""
    Игра на {coins} royal coins

    Участник 1: {interaction.user.global_name}

    Участник 2: -""")

                    return await message.edit(embed=embed)

                embed = discord.Embed(description=f"""
    Игра на {coins} royal coins

    Участник 1: {json_dict["games"]["duels"]["duel " + interaction.data.get("custom_id")]["first player nickname"]}

    Участник 2: {interaction.user.global_name}""")
                await message.edit(embed=embed)

                json_dict["games"]["duels"]["duel " +
                                            interaction.data.get("custom_id")]["players"] += 1

                if rint(1, 2) == 1:
                    winner_id = json_dict["games"]["duels"]["duel " +
                                                            interaction.data.get("custom_id")]["first player id"]
                    loser_id = interaction.user.id
                else:
                    winner_id = interaction.user.id
                    loser_id = json_dict["games"]["duels"]["duel " +
                                                           interaction.data.get("custom_id")]["first player id"]

                json_dict["information"][str(
                    winner_id)]["royals"] += json_dict["games"]["duels"]["duel " + interaction.data.get("custom_id")]["stavka"]
                json_dict["information"][str(
                    loser_id)]["royals"] -= json_dict["games"]["duels"]["duel " + interaction.data.get("custom_id")]["stavka"]
                with open("information.json", "w") as json_file:
                    json.dump(json_dict, json_file, indent=4)

                embed = discord.Embed(description=f"""
    Игра на {coins} royal coins

    Участник 1: -

    Участник 2: -""")

                join_button = Button(
                    label="Join", emoji="✅", style=discord.ButtonStyle.green, custom_id=interaction.data.get("custom_id"))
                join_button.callback = join_button_callback
                button_manager = View(timeout=None)
                button_manager.add_item(join_button)

                await message.edit(embed=embed, view=button_manager)

                json_dict["games"]["duels"]["duel " +
                                            interaction.data.get("custom_id")].pop("first player id")
                json_dict["games"]["duels"]["duel " +
                                            interaction.data.get("custom_id")].pop("first player nickname")
                json_dict["games"]["duels"]["duel " +
                                            interaction.data.get("custom_id")]["players"] = 0
                with open("information.json", "w") as json_file:
                    json.dump(json_dict, json_file, indent=4)

                await bot.get_channel(1268968669505917019).send(embed=discord.Embed(description=f'{bot.get_user(winner_id).mention} выиграл дуэль у {bot.get_user(loser_id).mention} на {coins} royal coins :gem:'))

        join_button = Button(label="Join", emoji="✅", style=discord.ButtonStyle.green, custom_id=str(
            len(json_dict["games"]["duels"].keys()) + 1))
        join_button.callback = join_button_callback
        button_manager = View(timeout=None)
        button_manager.add_item(join_button)

        message = await ctx.channel.send(embed=embed, view=button_manager)

        json_dict["games"]["duels"]["duel " +
                                    str(len(json_dict["games"]["duels"].keys()) + 1)] = {"message_id": message.id}
        json_dict["games"]["duels"]["duel " +
                                    str(len(json_dict["games"]["duels"].keys()))].update({"stavka": coins})
        json_dict["games"]["duels"]["duel " +
                                    str(len(json_dict["games"]["duels"].keys()))].update({"players": 0})

        with open("information.json", "w") as json_file:
            json.dump(json_dict, json_file, indent=4)
    except:
        print(
            f'Ошибка в команде duel:\n{format_exc()}\n////////////////////////////////////////////////////////////////////////////////////////////')


@bot.slash_command(name="skin_shop", description="Skin_Shop menu")
async def skin_shop(interaction: discord.interactions):
    """
Обрабатывает слэш команду skin_shop.

Пишет в чат сообщение, в котором можно купить скины за игровую валюту.

:param discord.interactions interaction: Этот объект предоставляет информацию о контексте, в котором была вызвана команда, включая данные о сообщении, канале, авторе и сервере..

:example:

>>> interaction = discord.interactions
>>> skin_shop(interaction: discord.interactions)
>>> Напишет в чат сообщение, в котором можно купить скины за игровую валюту.
    """
    try:
        if "Direct Message with" in str(interaction.channel.id):
            return
        if interaction.user.id != 854662130682691585:
            return print(f'{interaction.user.global_name} с id: {interaction.user.id}, пытается использоваться команду skin_shop!\nДата: {dt.now()}')
        if interaction.channel.id != 1273712968399458325:
            return

        await bot.get_channel(1273712968399458325).purge(limit=5)

        button_manager = View(timeout=None)

        async def skin_button_callback(interaction: discord.interactions):
            if interaction.user.id != 854662130682691585:
                return

            with open("information.json", "r") as json_file:
                json_dict = json.load(json_file)

            async for message in bot.get_channel(interaction.channel.id).history():
                if message.id != json_dict["shop"]["message_id"]:
                    await bot.get_channel(1273712968399458325).purge(limit=1)

            link = "https://rust.tm/?t=all&p=1&sd=desc"
            responce = get(link).text
            soup = BS(responce, 'lxml')
            max_page = int(soup.find('span', id="total_pages").text)

            link = f'https://rust.tm/?t=all&p={str(rint(1, (max_page - 1)))}&sd=desc'
            responce = get(link).text
            soup = BS(responce, 'lxml')
            block = soup.find('div', id="applications")
            divs = block.find_all('div')

            spisok = []
            for div in divs:
                if div.get('class') == ['image']:
                    sp = [div.get('style').lstrip(
                        "background-image: url(").rstrip(");")]
                if div.get('class') == ['price']:
                    cost = float(div.text.strip().replace(' ', ''))
                    if cost > 100:
                        sp.append(int(cost * 1.1))
                if div.get('class') == ['name']:
                    sp.append(div.text.strip())
                    if len(sp) == 3:
                        spisok.append(sp)
                    if len(spisok) == 6:
                        break

            embed_1 = discord.Embed(
                title=f'**1️⃣: {spisok[0][2]}**', description=f'**{spisok[0][1]}** :gem:', color=discord.Color.blue()).set_image(url=f'{spisok[0][0]}')
            embed_2 = discord.Embed(
                title=f'**2️⃣: {spisok[1][2]}**', description=f'**{spisok[1][1]}** :gem:', color=discord.Color.blue()).set_image(url=f'{spisok[1][0]}')
            embed_3 = discord.Embed(
                title=f'**3️⃣: {spisok[2][2]}**', description=f'**{spisok[2][1]}** :gem:', color=discord.Color.blue()).set_image(url=f'{spisok[2][0]}')
            embed_4 = discord.Embed(
                title=f'**4️⃣: {spisok[3][2]}**', description=f'**{spisok[3][1]}** :gem:', color=discord.Color.blue()).set_image(url=f'{spisok[3][0]}')
            embed_5 = discord.Embed(
                title=f'**5️⃣: {spisok[4][2]}**', description=f'**{spisok[4][1]}** :gem:', color=discord.Color.blue()).set_image(url=f'{spisok[4][0]}')
            embed_6 = discord.Embed(
                title=f'**6️⃣: {spisok[5][2]}**', description=f'**{spisok[5][1]}** :gem:', color=discord.Color.blue()).set_image(url=f'{spisok[5][0]}')

            shop_message = await interaction.channel.fetch_message(json_dict["shop"]["message_id"])

            skin_shop_view = View(timeout=None)

            async def skin_1_button_callback(interaction: discord.interactions):
                skin_name = interaction.data.get("custom_id").split("  ")[0]
                skin_cost = int(interaction.data.get(
                    "custom_id").split("  ")[1])
                with open("information.json", "r") as json_file:
                    json_dict = json.load(json_file)
                if json_dict["information"][str(interaction.user.id)]["royals"] >= skin_cost:
                    json_dict["information"][str(
                        interaction.user.id)]["royals"] -= skin_cost
                    with open("information.json", "w") as json_file:
                        json.dump(json_dict, json_file, indent=4)
                    await bot.get_channel(1274488341726756904).send(f'{interaction.user.mention} только что купил {skin_name} стоимостью в {skin_cost} :gem:!\nЗа получением скина пишите администрации!\nСпасибо за покупку!')
                else:
                    return

            skin_1_button = Button(label="", emoji="1️⃣", style=discord.ButtonStyle.green,
                                   custom_id=f'{str(spisok[0][2])}   {str(spisok[0][1])}')
            skin_1_button.callback = skin_1_button_callback
            skin_shop_view.add_item(skin_1_button)

            async def skin_2_button_callback(interaction: discord.interactions):
                skin_name = interaction.data.get("custom_id").split("  ")[0]
                skin_cost = int(interaction.data.get(
                    "custom_id").split("  ")[1])
                with open("information.json", "r") as json_file:
                    json_dict = json.load(json_file)
                if json_dict["information"][str(interaction.user.id)]["royals"] >= skin_cost:
                    json_dict["information"][str(
                        interaction.user.id)]["royals"] -= skin_cost
                    with open("information.json", "w") as json_file:
                        json.dump(json_dict, json_file, indent=4)
                    await bot.get_channel(1274488341726756904).send(f'{interaction.user.mention} только что купил {skin_name} стоимостью в {skin_cost} :gem:!\nЗа получением скина пишите администрации!\nСпасибо за покупку!')
                else:
                    return

            skin_2_button = Button(label="", emoji="2️⃣", style=discord.ButtonStyle.green,
                                   custom_id=f'{str(spisok[1][2])}   {str(spisok[1][1])}')
            skin_2_button.callback = skin_2_button_callback
            skin_shop_view.add_item(skin_2_button)

            async def skin_3_button_callback(interaction: discord.interactions):
                skin_name = interaction.data.get("custom_id").split("  ")[0]
                skin_cost = int(interaction.data.get(
                    "custom_id").split("  ")[1])
                with open("information.json", "r") as json_file:
                    json_dict = json.load(json_file)
                if json_dict["information"][str(interaction.user.id)]["royals"] >= skin_cost:
                    json_dict["information"][str(
                        interaction.user.id)]["royals"] -= skin_cost
                    with open("information.json", "w") as json_file:
                        json.dump(json_dict, json_file, indent=4)
                    await bot.get_channel(1274488341726756904).send(f'{interaction.user.mention} только что купил {skin_name} стоимостью в {skin_cost} :gem:!\nЗа получением скина пишите администрации!\nСпасибо за покупку!')
                else:
                    return

            skin_3_button = Button(label="", emoji="3️⃣", style=discord.ButtonStyle.green,
                                   custom_id=f'{str(spisok[2][2])}   {str(spisok[2][1])}')
            skin_3_button.callback = skin_3_button_callback
            skin_shop_view.add_item(skin_3_button)

            async def skin_4_button_callback(interaction: discord.interactions):
                skin_name = interaction.data.get("custom_id").split("  ")[0]
                skin_cost = int(interaction.data.get(
                    "custom_id").split("  ")[1])
                with open("information.json", "r") as json_file:
                    json_dict = json.load(json_file)
                if json_dict["information"][str(interaction.user.id)]["royals"] >= skin_cost:
                    json_dict["information"][str(
                        interaction.user.id)]["royals"] -= skin_cost
                    with open("information.json", "w") as json_file:
                        json.dump(json_dict, json_file, indent=4)
                    await bot.get_channel(1274488341726756904).send(f'{interaction.user.mention} только что купил {skin_name} стоимостью в {skin_cost} :gem:!\nЗа получением скина пишите администрации!\nСпасибо за покупку!')
                else:
                    return

            skin_4_button = Button(label="", emoji="4️⃣", style=discord.ButtonStyle.green,
                                   custom_id=f'{str(spisok[3][2])}   {str(spisok[3][1])}')
            skin_4_button.callback = skin_4_button_callback
            skin_shop_view.add_item(skin_4_button)

            async def skin_5_button_callback(interaction: discord.interactions):
                skin_name = interaction.data.get("custom_id").split("  ")[0]
                skin_cost = int(interaction.data.get(
                    "custom_id").split("  ")[1])
                with open("information.json", "r") as json_file:
                    json_dict = json.load(json_file)
                if json_dict["information"][str(interaction.user.id)]["royals"] >= skin_cost:
                    json_dict["information"][str(
                        interaction.user.id)]["royals"] -= skin_cost
                    with open("information.json", "w") as json_file:
                        json.dump(json_dict, json_file, indent=4)
                    await bot.get_channel(1274488341726756904).send(f'{interaction.user.mention} только что купил {skin_name} стоимостью в {skin_cost} :gem:!\nЗа получением скина пишите администрации!\nСпасибо за покупку!')
                else:
                    return

            skin_5_button = Button(label="", emoji="5️⃣", style=discord.ButtonStyle.green,
                                   custom_id=f'{str(spisok[4][2])}   {str(spisok[4][1])}')
            skin_5_button.callback = skin_5_button_callback
            skin_shop_view.add_item(skin_5_button)

            async def skin_6_button_callback(interaction: discord.interactions):
                skin_name = interaction.data.get("custom_id").split("  ")[0]
                skin_cost = int(interaction.data.get(
                    "custom_id").split("  ")[1])
                with open("information.json", "r") as json_file:
                    json_dict = json.load(json_file)
                if json_dict["information"][str(interaction.user.id)]["royals"] >= skin_cost:
                    json_dict["information"][str(
                        interaction.user.id)]["royals"] -= skin_cost
                    with open("information.json", "w") as json_file:
                        json.dump(json_dict, json_file, indent=4)
                    await bot.get_channel(1274488341726756904).send(f'{interaction.user.mention} только что купил {skin_name} стоимостью в {skin_cost} :gem:!\nЗа получением скина пишите администрации!\nСпасибо за покупку!')
                else:
                    return

            skin_6_button = Button(label="", emoji="6️⃣", style=discord.ButtonStyle.green,
                                   custom_id=f'{str(spisok[5][2])}   {str(spisok[5][1])}')
            skin_6_button.callback = skin_6_button_callback
            skin_shop_view.add_item(skin_6_button)

            await shop_message.reply(embeds=[embed_1, embed_2, embed_3, embed_4, embed_5, embed_6], view=skin_shop_view)

        skin_button = Button(label="skin", emoji="🏹",
                             style=discord.ButtonStyle.green)
        skin_button.callback = skin_button_callback
        button_manager.add_item(skin_button)

        embed = discord.Embed(title="**Skin shop by RoyalRust**",
                              description="",
                              color=discord.Color.blue())

        message = await interaction.channel.send(embed=embed, view=button_manager)

        with open("information.json", "r") as json_file:
            json_dict = json.load(json_file)
        json_dict["shop"]["message_id"] = message.id
        with open("information.json", "w") as json_file:
            json.dump(json_dict, json_file, indent=4)
    except:
        print(
            f'Ошибка в команде skin_shop:\n{format_exc()}\n////////////////////////////////////////////////////////////////////////////////////////////')


@bot.slash_command(name="role_shop", description="Role_Shop menu")
async def role_shop(interaction: discord.interactions):
    """
Обрабатывает слэш команду role_shop.

Пишет в чат сообщение, в котором можно купить роли за игровую валюту.

:param discord.interactions interaction: Этот объект предоставляет информацию о контексте, в котором была вызвана команда, включая данные о сообщении, канале, авторе и сервере..

:example:

>>> interaction = discord.interactions
>>> role_shop(interaction: discord.interactions)
>>> Напишет в чат сообщение, в котором можно купить роли за игровую валюту.
    """
    try:
        if "Direct Message with" in str(interaction.channel.id):
            return
        if interaction.user.id != 854662130682691585:
            return print(f'{interaction.user.global_name} с id: {interaction.user.id}, пытается использоваться команду role_shop!\nДата: {dt.now()}')
        if interaction.channel.id != 1274499415142436876:
            return

        await bot.get_channel(1274499415142436876).purge(limit=5)

        embed_1 = discord.Embed(
            title="Role shop by RoyalRust", color=discord.Color.blue())

        embed_2 = discord.Embed(title="", color=discord.Color.blue())
        embed_2.add_field(name='',
                          value=f'• <@&{1274342413317443645}>\n'
                          "Цена: 750 :gem:\n\n"
                          f'• <@&{1273379005587787838}>\n'
                          "Цена: 500 :gem:",
                          inline=False)

        button_manager = View(timeout=None)

        async def vip_button_callback(interaction: discord.interactions):
            if not ("vip" in [role.name for role in interaction.user.roles]):
                with open("information.json", "r") as json_file:
                    json_dict = json.load(json_file)
                if json_dict["information"][str(interaction.user.id)]["royals"] >= 750:
                    json_dict["information"][str(
                        interaction.user.id)]["royals"] -= 750

                    with open("information.json", "w") as json_file:
                        json.dump(json_dict, json_file, indent=4)

                    await interaction.user.add_roles(discord.utils.get(interaction.user.guild.roles, id=1274342413317443645))

                    await bot.get_channel(1274488341726756904).send(f'{interaction.user.mention} только что купил <@&{1274342413317443645}> стоимостью в 750 :gem:!\nРоль успешно выдана!!\nСпасибо за покупку!')

        vip_button = Button(label="vip", emoji="👑",
                            style=discord.ButtonStyle.green)
        vip_button.callback = vip_button_callback
        button_manager.add_item(vip_button)

        async def media_button_callback(interaction: discord.interactions):
            if not ("media" in [role.name for role in interaction.user.roles]):
                with open("information.json", "r") as json_file:
                    json_dict = json.load(json_file)
                if json_dict["information"][str(interaction.user.id)]["royals"] >= 500:
                    json_dict["information"][str(
                        interaction.user.id)]["royals"] -= 500

                    with open("information.json", "w") as json_file:
                        json.dump(json_dict, json_file, indent=4)

                    await interaction.user.add_roles(discord.utils.get(interaction.user.guild.roles, id=1273379005587787838))

                    await bot.get_channel(1274488341726756904).send(f'{interaction.user.mention} только что купил <@&{1273379005587787838}> стоимостью в 500 :gem:!\nРоль успешно выдана!!\nСпасибо за покупку!')

        media_button = Button(label="media", emoji="🎥",
                              style=discord.ButtonStyle.blurple)
        media_button.callback = media_button_callback
        button_manager.add_item(media_button)

        await interaction.channel.send(embeds=[embed_1, embed_2], view=button_manager)
    except:
        print(
            f'Ошибка в команде role_shop:\n{format_exc()}\n////////////////////////////////////////////////////////////////////////////////////////////')

# ADMIN_COMMAND


@bot.command(name="add_coins")
async def add_coins(ctx, *args):
    """
Обрабатывает команду add_coins.

Эта функция дает участнику с id args[0] виртуальную валюту в количестве args[1]. Строго 2 аргумента подается после ввода команды 1 - id кому начислить валюту 2 - сколько валюты начислять.

:param discord.Context ctx: Этот объект предоставляет информацию о контексте, в котором была вызвана команда, включая данные о сообщении, канале, авторе и сервере.

:example:

>>> ctx = discord.Context
>>> add_coins(ctx, *args)
>>> Даст участнику с id args[0] виртуальную валюту в количестве args[1].
    """
    try:
        if "Direct Message with" in str(ctx.channel):
            return
        if ctx.author.id != 854662130682691585:
            return print(f'{ctx.author.global_name} с id: {ctx.author.id}, пытается использоваться команду end!\nДата: {dt.now()}')
        await (await ctx.channel.fetch_message(ctx.message.id)).delete()
        if len(args) != 2:
            return
        with open("information.json", "r") as json_file:
            json_dict = json.load(json_file)

        json_dict["information"][args[0]]["royals"] += int(args[1])

        await bot.get_channel(1265422217320337520).send(f'{bot.get_user(int(args[0])).mention} получил {args[1]} royals coins :gem: на свой баланс!')

        with open("information.json", "w") as json_file:
            json.dump(json_dict, json_file, indent=4)
    except:
        print(
            f'Ошибка в команде add_coins:\n{format_exc()}\n////////////////////////////////////////////////////////////////////////////////////////////')

# ADMIN_COMMAND


@bot.command(name="del_coins")
async def del_coins(ctx, *args):
    """
Обрабатывает команду del_coins.

Эта функция забирает у участника с id args[0] виртуальную валюту в количестве args[1]. Строго 2 аргумента подается после ввода команды 1 - id у кого забирать валюту 2 - сколько валюты забирать.

:param discord.Context ctx: Этот объект предоставляет информацию о контексте, в котором была вызвана команда, включая данные о сообщении, канале, авторе и сервере.

:example:

>>> ctx = discord.Context
>>> del_coins(ctx, *args)
>>> Забирает у участника с id args[0] виртуальную валюту в количестве args[1].
    """
    try:
        if "Direct Message with" in str(ctx.channel):
            return
        if ctx.author.id != 854662130682691585:
            return print(f'{ctx.author.global_name} с id: {ctx.author.id}, пытается использоваться команду end!\nДата: {dt.now()}')
        await (await ctx.channel.fetch_message(ctx.message.id)).delete()
        if len(args) != 2:
            return
        with open("information.json", "r") as json_file:
            json_dict = json.load(json_file)

        json_dict["information"][args[0]]["royals"] -= int(args[1])

        await bot.get_channel(1265422217320337520).send(f'{bot.get_user(int(args[0])).mention} потерял {args[1]} royals coins :gem: со своего баланса!')

        with open("information.json", "w") as json_file:
            json.dump(json_dict, json_file, indent=4)
    except:
        print(
            f'Ошибка в команде del_coins:\n{format_exc()}\n////////////////////////////////////////////////////////////////////////////////////////////')

# moderator_command


@bot.command(name="ban")
async def ban(ctx, id):
    """
Обрабатывает команду ban.

Эта функция забирает у участника все роли и дает роль BAN.

:param discord.Context ctx: Этот объект предоставляет информацию о контексте, в котором была вызвана команда, включая данные о сообщении, канале, авторе и сервере.
:param int id: id участника, которого нужно забанить.

:example:

>>> ctx = discord.Context
>>> id = 1234567890
>>> ban(ctx, 1234567890)
>>> Забирает роли у участника с id 1234567890 и дает ему роль BAN.
    """
    try:
        if "Direct Message with" in str(ctx.channel):
            return
        if (ctx.channel.id != 1280954033929981962):
            return
        await (await ctx.channel.fetch_message(ctx.message.id)).delete()
        if ("moderator" in [role.name for role in ctx.author.roles]):
            if id.isdigit() == True:
                try:
                    ban_player = ctx.guild.get_member(int(id))
                except:
                    return await bot.get_channel(1280954056033964155).send(f'{ctx.author.mention} пользователя с id: {id} не существует!')
                await ban_player.edit(roles=[ctx.guild.default_role])

                await ban_player.add_roles(discord.utils.get(ctx.author.guild.roles, id=1280532470252441640))

                await bot.get_channel(1280954056033964155).send(f'{ctx.author.mention} забанил {ctx.guild.get_member(int(id)).mention}.')
    except:
        print(
            f'Ошибка в команде ban:\n{format_exc()}\n////////////////////////////////////////////////////////////////////////////////////////////')

bot.run(config["token"])
