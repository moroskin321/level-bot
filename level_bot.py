import discord
from discord.ext import commands
from Question import *
quiz_work = False
lvl = {}

token = " "
bot = commands.Bot(command_prefix = '!')

q1 = Question('Что за блок?', './Pictures/0.png', 'почва душ')
q2 = Question('Что получится?', './Pictures/1.png', 'фонарь душ')
q = []
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

@bot.command(brief = "Только 'Глава мафии' задать уровень участника",
description = "Только 'Глава мафии' задать уровень участника")
async def set_level(ctx, name, level):
    if is_admin(ctx):
        if not level.isdigit():
            await ctx.channel.send('Ошибка 2: Неверный формат(Уровень должен быть числом)')
            return
        lvl[name] = int(level)
        await ctx.channel.send('У персонажа ' + name + ' уровень ' + str(lvl[name]))
    else:
        await ctx.channel.send('Ошибка 1: Недостаточно прав')
    save_levels()

@bot.command(brief = "Только 'Глава мафии' изменение уровня участника",
description = "Только 'Глава мафии' изменение уровня участника")
async def level_up(ctx, name, level):
    if is_admin(ctx):
        if not level.isdigit():
            await ctx.channel.send('Ошибка 2: Неверный формат(Уровень должен быть числом)')
            return
        if lvl.get(name) != None:
            lvl[name] += int(level)
            await ctx.channel.send('У персонажа ' + name + ' уровень ' + str(lvl[name]))
        else:
            lvl[name] = 1
            lvl[name] += int(level)
            await ctx.channel.send('У персонажа ' + name + ' уровень ' + str(lvl[name]))
    else:
        await ctx.channel.send('Ошибка 1: Недостаточно прав')
    save_levels()


def level_up(name):
    if lvl.get(name) != None:
        lvl[name] += 1
    else:
        lvl[name] = 2
    save_levels()

async def check_end(ctx):
    global q
    global qn
    if qn >= len(q):
        qn = 0
        await ctx.channel.send('викторина сброшена')

@bot.command(brief = "Только 'Глава мафии' старт викторины",
description = "Только 'Глава мафии' старт викторины")
async def ask(ctx):
    global quiz_work
    if is_admin(ctx):
        global q
        if len(q) > 0:
            await check_end(ctx)
            quiz_work = True
            global qn
            question = discord.Embed(
                title = q[qn].text,
                colour = discord.Colour.red())
    #        question.set_image(discord.File(q[qn].image_path))
            await ctx.send(embed = question, file = discord.File(q[qn].image_path))
        else:
            await ctx.channel.send('Ошибка 4: Нет вопросов, просьба обратится к администратору.')
    else:
        await ctx.channel.send('Ошибка 1: Недостаточно прав')
#МЫ СТРАДАЛИ ВСЕ ВРЕМЯ И ВСЕГДА
@bot.command(brief = "Только 'Глава мафии' пропуск вопроса викторины",
description = "Только 'Глава мафии' пропуск вопроса викторины")
async def skip(ctx):
    if is_admin(ctx):
        global quiz_work
        if quiz_work:
            global qn
            quiz_work = False
            qn += 1
            await ctx.send('вопрос пропущен, !ask для следующего вопроса')
        else:
            await ctx.channel.send('Ошибка 3: Нет вопроса для пропуска')
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
            await check_end(ctx)
    await bot.process_commands(ctx)

bot.run(token)
