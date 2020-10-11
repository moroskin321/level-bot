import discord
from discord.ext import commands
from Question import *
quiz_work = False
lvl = {}

token = "NzU1NzM0OTMyNTY3MDk3MzQ0.X2HnAA.nlwlRXSg9ZU4APeMI6bhZgybduQ"
bot = commands.Bot(command_prefix = '!')

q1 = Question('Что за блок?', './Pictures/0.png', 'почва душ')
q2 = Question('Что получится?', './Pictures/1.png', 'фонарь душ')
q = [q1, q2]
qn = 0
def get_levels():
    file = open('Levels.txt', 'r')
    for line in file:
        line = line.split()
        lvl[line[0]] =  int(line[1])
    file.close()

def save_levels():
    file = open('Levels.txt', 'w')
    s = ''
    for i in lvl.keys():
        s += i + ' ' + str(lvl[i]) + '\n'
    file.write(s)
    file.close()


@bot.event
async def on_ready():
    print('Я готов ничего не делать')
    get_levels()

def is_admin(ctx):
    for role in ctx.author.roles:
        if role.name == 'Глава мафии':
            return True
    return False

@bot.command(brief = 'показывает уровни остальных участников',
description = 'если полез сюда потому-что не понял значит тупой как валенок')
async def statistics(ctx):
    await ctx.channel.send('Здесь будет статистика всех участников')
    answer = ''
    for i in lvl.keys():
        answer += i + ' - ' + str(lvl[i]) + '\n'
    await ctx.channel.send(answer)


@bot.command(brief = 'показывает твой уровень',
description = 'если сюда полез потому-что не понял значит тупой как валенок')
async def my_level(ctx):
    await ctx.channel.send('У персонажа ' + str(ctx.author) + ' уровень ' + str(lvl[str(ctx.author)]))

@bot.command(brief = 'активирует систему уровней', description = 'выдает 1 уровень и добавляет вас в систему')
async def start(ctx):
    lvl[str(ctx.author)] = 1
    save_levels()

@bot.command()
async def set_level(ctx, name, level):
    if is_admin(ctx):
        lvl[name] = int(level)
        await ctx.channel.send('У персонажа ' + name + ' уровень ' + str(lvl[name]))
    else:
        await ctx.channel.send('Ошибка 1: Недостаточно прав')
    save_levels()

@bot.command()
async def level_up(ctx, name, level):
    if is_admin(ctx):
        lvl[name] += int(level)
        await ctx.channel.send('У персонажа ' + name + ' уровень ' + str(lvl[name]))
    else:
        await ctx.channel.send('Ошибка 1: Недостаточно прав')
    save_levels()


def level_up(name):
    lvl[name] += 1
    save_levels()


@bot.command()
async def Admin_menu(ctx):
    if is_admin(ctx):
        lvl[str(ctx.author)] = 'Admin'

@bot.command()
async def ask(ctx):
    global quiz_work
    if is_admin(ctx):
        quiz_work = True
        global qn
        global q
        await ctx.channel.send(q[qn].text)
        await ctx.channel.send(file = discord.File(q[qn].image_path))
    else:
        await ctx.channel.send('Ошибка 1: Недостаточно прав')

@bot.event
async def on_message(ctx):
    global quiz_work
    if quiz_work:
        global qn
        global q
        if ctx.content.lower() == q[qn].answer:
            await ctx.channel.send(str(ctx.author) + ' Правильно')
            level_up(str(ctx.author))
            await ctx.channel.send('У персонажа ' + str(ctx.author) + ' уровень ' + str(lvl[str(ctx.author)]))
            quiz_work = False
            qn += 1
    await bot.process_commands(ctx)

bot.run(token)
