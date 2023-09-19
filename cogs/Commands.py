import asyncio
from datetime import datetime
from time import sleep
import discord
from discord.ext.commands.core import command
import wikipedia
import os
import random
import wolframalpha
from itertools import cycle
from reddit_scraper import *
from discord.ext import commands
from autocorrect import Speller

file = open('Movesets.txt', 'r')
x = list(file.read().lower().split('\n'))

import sys
from datetime import date

months = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}
Month = months[str(date.today()).split('-')[1]]
Date = str(date.today()).split('-')[-1]

schedule = {
    "Monday":
    ["CTIP", "UT", "UT", "Free", "Break", "History Civics", "IT", "Biology"],
    "Tuesday": [
        "CTIP", "Free", "Maths", "Chemistry", "Break", "Free", "English",
        "German"
    ],
    "Wednesday": [
        "CTIP", "Physics", "History Civics", "Yoga", "Break", "Maths", "Art",
        "Geography"
    ],
    "Thursday":
    ["CTIP", "IT", "Physics", "Maths", "Break", "ENglish", "German", "PE"],
    "Friday": [
        "CTIP (Work Education)", "Chemistry", "Biology", "Geography", "Break",
        "English", "Maths", "German"
    ]
}

schedule2 = {
    "Monday":
    ["CTIP", "UT", "UT", "Free", "Break", "Biology", "Chemistry", "Geography"],
    "Tuesday":
    ["CTIP", "Maths", "Hindi", "English", "Break", "IT", "Physics", "Art"],
    "Wednesday": [
        "CTIP", "Geography", "Biology", "History Civics", "Break", "Maths",
        "Hindi", "PE"
    ],
    "Thursday": [
        "CTIP", "IT", "Maths", "History Civics", "Break", "Free", "English",
        "Hindi"
    ],
    "Friday": [
        "CTIP (Work Education)", "Yoga", "Chemistry", "English", "Break",
        "Maths", "Physics", "Free"
    ]
}


def checkSlot(hour, min):
    timenow = hour + min / 60
    if timenow > (7 + 30 / 60) and timenow <= (7 + 55 / 60):  # CTIP
        return 0, "Starts at 7:30, Ends at 7:55"
    if timenow > (7 + 55 / 60) and timenow <= (8 + 45 / 60):  # First Period
        return 1, "Starts at 8:00, Ends at 8:45"
    if timenow > (8 + 45 / 60) and timenow <= (9 + 40 / 60):  # Second Period
        return 2, "Starts at 8:55, Ends at 9:40"
    if timenow > (9 + 40 / 60) and timenow <= (10 + 35 / 60):  # Third Period
        return 3, "Starts at 9:50, Ends at 10:35"
    if timenow > (10 + 35 / 60) and timenow <= (10 + 45 / 60):  # Break
        return 4, "Starts at 10:35, Ends at 10:55"
    if timenow > (10 + 45 / 60) and timenow <= (11 + 40 / 60):  # Fourth Period
        return 5, "Starts at 10:55, Ends at 11:40"
    if timenow > (11 + 40 / 60) and timenow <= (12 + 35 / 60):  # Fifth Period
        return 6, "Starts at 11:50, Ends at 12:35"
    if timenow > (12 + 35 / 60) and timenow <= (13 + 30 / 60):  # Sixth Period
        return 7, "Starts at 12:45, Ends at 1:30"
    return None


sys.path.append("/home/agastya/pythonprojects/discord-bot")


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.spam_count = 0

        self.blackmagicposts = make_posts_list('blackmagicfuckery')
        self.memes = make_posts_list('Memes')
        self.wholesomeMemes = make_posts_list('wholesomememes')
        self.Showerthoughts = make_posts_list_title('Showerthoughts')
        self.lifeprotips = make_posts_list_title('LifeProTips')
        self.facts = make_posts_list_title('todayilearned')
        self.minecraftmemes = make_posts_list('MinecraftMemes')
        self.news = make_posts_list_title('news')
        self.jokes = make_posts_lists_title_and_body('jokes')

        self.statuses = cycle([
            'League of Legends', 'Rainbow Six: Siege', 'Among Us', 'Minecraft',
            'Valorant', 'Rocket League', 'Overwatch', 'Genshin Impact',
            'Call of Duty: Modern Warfare', 'Hearthstone',
            'Grand Theft Auto V', 'World of Warcraft', 'Fall Guys', 'Dota 2',
            'Phasmophobia', 'Counter-Strike: Global Offensive', 'Porknight'
        ])

    @commands.command(aliases=['tt'],
                      help="(tt) Check today's school's schedule")
    async def schedule(self, ctx):
        area = ctx.message.channel
        await area.send(file=discord.File(f'cogs/{Month}{Date}.png'))

    @commands.command(
        help="Get the latency between your input and the bot's output")
    async def ping(self, ctx):
        await ctx.send(f"Latency - {self.client.latency}")

    @commands.command(help='Get a greeting')
    async def hello(self, ctx):
        await ctx.send('Hey! Type .help for a list of commands ')

    @commands.command(aliases=['m'], help='(m)Get a Meme')
    async def meme(self, ctx):
        url = give_random_post(self.memes)
        await ctx.send('Meme- (Type .help for a list of commands)')
        await ctx.send(url)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def echo(self, ctx, *, sentence):
        await ctx.message.delete()
        await ctx.send(sentence)

    @commands.command(aliases=["rn"], help="returns random numbers ")
    async def random_number(self, ctx, lower, upper):
        upper = int(upper)
        lower = int(lower)
        await ctx.send(str(random.randint(lower, upper)))

    @commands.command(aliases=['wm'], help='(wm)Get a Wholesome Meme')
    async def wholesomememe(self, ctx):
        url = give_random_post(self.wholesomeMemes)
        await ctx.send('Wholesome Meme(Type .help for a list of commands)')
        await ctx.send(url)

    @commands.command(
        aliases=['wa'],
        help=
        'Ask a question (mathematics, sciences etc and get a result from wolfram alpha'
    )
    async def wolfram(self, ctx, *, question):
        await ctx.send("Hold up a minute. I'm getting the answer")
        app_id = "6RHU64-XKUKR3UGY4"
        x = Speller('en')
        correct_spelling = x(str(question))
        if correct_spelling != question and '-no' not in question:
            await ctx.send(
                f"I think you meant '{correct_spelling}' I'll take that as the question then"
            )
            question = correct_spelling

        client = wolframalpha.Client(app_id)

        res = client.query(question)

        try:

            for c in range(len(next(res.results)['subpod'])):
                await ctx.send(next(res.results)['subpod'][c]['img']['@src'])

        except:
            try:
                await ctx.send(next(res.results)['subpod']['img']['@src'])
            except:
                await ctx.send("I couldn't find any results. Try asking .8ball"
                               )

    @commands.command(aliases=["ms"],
                      help="Get the optimal moveset for a pokemon")
    async def moveset(self, ctx, *, pokemon):
        done = False
        ret = f"```Moveset for {pokemon}:\n"
        for i in range(len(x) - 1):
            if pokemon in x[i] and "#" not in x[i + 1]:
                done = True
                y = "#"
                z = 1
                while y not in x[i + z]:
                    ret += x[i + z]
                    ret += "\n"
                    z += 1
        if not done:
            ret += f"Couldn't find the pokemon {pokemon}"
        ret += "```"
        await ctx.send(ret)

    @commands.command(aliases=["c"])
    async def calc(self, ctx, expression):
        try:
            await ctx.send(eval(expression))
        except:
            return await ctx.send("Error")

    @commands.command(aliases=['w'], help='Get a summary from wikipedia')
    async def wiki(self, ctx, *, question):
        try:
            summ = wikipedia.summary(question)
            await ctx.send(f'A summary on {question}-')
            await ctx.send(f'{summ}')
        except Exception as e:
            try:
                await ctx.send(
                    f'The summary on {question} is too long to send on discord. Here is the link of the page instead:'
                )
                await ctx.send(f"{wikipedia.page(f'{question}').url}")
            except:
                await ctx.send(f"Couldn't find anything on {question}")

    @commands.command(aliases=['st'], help='(st)Get a perplexing thought')
    async def showerthought(self, ctx):
        title = give_random_post(self.Showerthoughts)
        await ctx.send(title)

    @commands.command(help='(lpt)Get a Life Pro Tip to make your life easier')
    async def lpt(self, ctx):
        title = give_random_post(self.lifeprotips)
        await ctx.send('Life Pro Tip-')
        await ctx.send(title)

    @commands.command(
        aliases=['8ball'],
        help=
        "(8ball)Ask a question and get a random answer. Type '.8ball' and any question after it"
    )
    async def _8ball(self, ctx, *, question):
        responses = [
            "It is certain.", "It is decidedly so.", "Without a doubt.",
            "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
            "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
            "Reply hazy, try again.", "Ask again later.",
            "Better not tell you now.", "Cannot predict now.",
            "Concentrate and ask again.", "Don't count on it.",
            "My reply is no.", "My sources say no.", "Outlook not so good.",
            "Very doubtful."
        ]
        await ctx.send(f"{random.choice(responses)}")

    @commands.command(aliases=['f'], help='(f)Get an interesting Fact')
    async def fact(self, ctx):
        title = give_random_post(self.facts)
        title = title[3:]
        if title.split()[0] == 'that':
            title = ' '.join(title.split()[1:])
        await ctx.send('A cool fact-')
        await ctx.send(title)

    @commands.command(aliases=['mm'], help='(mm)Get a Minecraft Meme')
    async def minecraftmeme(self, ctx):
        url = give_random_post(self.minecraftmemes)
        await ctx.send('A Minecraft Meme')
        await ctx.send(url)

    @commands.command(aliases=['j'], help='(j)Get a Joke')
    async def joke(self, ctx):
        jk = give_random_post(self.jokes)
        await ctx.send(jk)

    @commands.command(
        aliases=['bm'],
        help=
        '(bm)Get some confusing phenomena that makes you wonder if reality is broken'
    )
    async def blackmagic(self, ctx):
        post = give_random_post(self.blackmagicposts)
        await ctx.send('Black Magic!')
        await ctx.send(post)

    @commands.command(aliases=['n'], help='(n)Get a news headline')
    async def news(self, ctx):
        title = give_random_post(self.news)
        await ctx.send('News Headline-')
        await ctx.send(title)

    @commands.command(help='Get current class')
    async def period(self, ctx):
        day = datetime.now().strftime("%A")

        hour = datetime.now().hour
        minute = datetime.now().minute

        total = hour * 60 + minute
        total += 330

        hour = int((total - total % 60) / 60)
        minute = int(total % 60)

        await ctx.send(
            f"{schedule[day][checkSlot(hour, minute)[0]]}\n{checkSlot(hour, minute)[1]}"
        )

    @commands.command(help="Get a list of todays classes")
    async def today(self, ctx):
        day = datetime.now().strftime("%A")
        val = "Today's classes:\n```"

        for i in range(len(schedule[day])):
            val += (schedule[day][i] + "\n")
        val += "```"
        await ctx.send(val)

    @commands.command(help='Get current class')
    async def period2(self, ctx):
        day = datetime.now().strftime("%A")

        hour = datetime.now().hour
        minute = datetime.now().minute

        total = hour * 60 + minute
        total += 330

        hour = int((total - total % 60) / 60)
        minute = int(total % 60)

        await ctx.send(
            f"{schedule2[day][checkSlot(hour, minute)[0]]}\n{checkSlot(hour, minute)[1]}"
        )

    @commands.command(help="Get a list of todays classes")
    async def today2(self, ctx):
        day = datetime.now().strftime("%A")
        val = "Today's classes:\n```"

        for i in range(len(schedule2[day])):
            val += (schedule2[day][i] + "\n")
        val += "```"
        await ctx.send(val)



def setup(client):
    client.add_cog(Commands(client))
