import discord
import asyncio
from utils.texttime import time_to_timedelta, timetotext, is_valid_time
from datetime import datetime, timedelta
from discord.ext import commands
from utils.db import ToDo, to_csv, get_min_datetime, get_remaining_task
from utils.constants import COLOURS

class Todo(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def refresh_sleep(self, ctx):
        task_list = sorted(await get_min_datetime(), key = lambda x: x[2])
        task_list = [(row[0], row[1], row[2]) for row in task_list if row[2]>datetime.now()]
        try:
            min_datetime = task_list[0]
        except Exception:
            return None
        await asyncio.sleep((min_datetime[2]-datetime.now()).total_seconds())
        mem_obj = await self.client.fetch_user(min_datetime[0])
        await ctx.send(f'{mem_obj.mention} Task: "**{min_datetime[1]}**" is remaining!')
        await self.refresh_sleep(ctx)

    @commands.command
    async def backup(self, ctx):
        await to_csv()
        await ctx.send("Backed UP")

    @commands.command(aliases = ['td'])
    async def todo(self, ctx, cmd = None, *, task = None):
        todo_obj = ToDo(ctx.author.id)
        if cmd is None:
            try:
                tasks_tuple = await todo_obj.all_tasks()
                string = ""
                for i in range(len(tasks_tuple)):
                    if tasks_tuple[i][1] is not None:
                        if (tasks_tuple[i][1]-datetime.now()).total_seconds() < 0:
                            string += f'{i+1}. {tasks_tuple[i][0]} _late by_ {timetotext(tasks_tuple[i][1]-datetime.now())}\n'
                        else:
                            string += f'{i+1}. {tasks_tuple[i][0]} in {timetotext(tasks_tuple[i][1]-datetime.now())}\n'
                    else:
                        string += f'{i+1}. {tasks_tuple[i][0]}\n'
                e = discord.Embed(colour=COLOURS['purple'])
                e.set_author(name=ctx.author, icon_url=ctx.author.avatar_url) 
                e.add_field(name="Todo:", value = f'{string.strip()}')
                await ctx.send(embed = e)
            except Exception:
                await ctx.send("No tasks available!!!")
        elif cmd.lower() == 'add':
            if task is None:
                await ctx.send("No task given!")
            else:
                time = task.split()[-1]
                if is_valid_time(time):
                    time = datetime.now() + time_to_timedelta(time)
                    task = " ".join(task.split()[:-1])
                else:
                    time = None
                await todo_obj.todo_add(task, time)
                await ctx.message.add_reaction("\U0001f4cb")
                await self.refresh_sleep(ctx)

        elif cmd.lower() == 'remove':
            try:
                choice = int(task)
                try:
                    await todo_obj.todo_remove(choice)
                    await ctx.message.add_reaction("\U00002705")
                    await self.refresh_sleep(ctx)
                except Exception:
                    await ctx.send("No task available at that index")
            except Exception:
                if task.lower() == 'all':
                    await todo_obj.todo_remove_all()
                    await ctx.message.add_reaction("\U00002705")
                else:
                    await ctx.send("Invalid Index")


def setup(client):
    client.add_cog(Todo(client))
