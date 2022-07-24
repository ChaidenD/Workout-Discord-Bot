import discord
import numpy
from keep_alive import keep_alive
import time
import sched
import datetime
from datetime import timedelta

import pytz


class WorkOutDays:
    def __init__(self):
        self.workOutDays = numpy.array(['Push', 'Pull', 'Leg', 'Rest'])
        self._counter = 0

    def loopCounter(self):
        if self._counter >= len(self.workOutDays):
            self._counter %= len(self.workOutDays)
        else:
            self._counter += 1

    @property
    def currentDay(self):
        return self.workOutDays[self._counter]


def getNextRun():
    timezone = pytz.timezone('America/Los_Angeles')
    noon = datetime.time(hour=12, tzinfo=timezone)
    currentDay = datetime.datetime.today().astimezone(timezone)
    return datetime.datetime.combine(
        currentDay + timedelta(days=int(currentDay.time() > noon)), noon,
        timezone)


client = discord.Client()
s = sched.scheduler(time.time, time.sleep)
workouts = WorkOutDays()
nextRun = getNextRun()
channel = None


def nextDay():
    global workouts
    global s
    global nextRun
    workouts.loopCounter()
    sendCurrentWorkout()
    s.enterabs(nextRun, 1, nextDay)
    nextRun = nextRun + timedelta(days=1)


s.enterabs(nextRun, 1, nextDay)


@client.event
async def on_ready():
    global channel
    print('We have logged in as {0.user}'.format(client))
    channel = client.get_channel(999742180509884416)

@client.event
async def on_message(message):
    global channel
    if message.content.startswith('WOD?'):
        await sendCurrentWorkout()
    elif message.content.startswith('!push'):
        await message.channel.send('Filler')

    if message.content.startswith("?Test"):
        await channel.send(workouts.currentDay)


async def sendCurrentWorkout():
    global client
    global workouts
    #998093562908520448
    channel = client.get_channel(999742180509884416)
    #await client.channels.get('684946298595704856').send(workouts.currentDay)
    await channel.send(workouts.currentDay)
    #run loopCounter after sending daily reminder


keep_alive()
client.run('OTk5NzM0Nzk2NDkyMjI2NTkw.GUWzkM.N0n-1Q2OubmjOdAgBJ7uMpgCGW0FSHp9ROf4zY')
