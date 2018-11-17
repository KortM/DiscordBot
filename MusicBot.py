import discord
import requests
from discord.ext import commands
from Audio import Music
from mutagen.mp3 import MP3
import os
import asyncio
BOT_TOKEN = 'NTEyMzc3MjU0NTgwMzIyMzA0.Ds4qIg.FGVcxoNOLens7RbyJJ93Ng_ncxU'
client = commands.Bot(command_prefix='!')

players  = {}
musics = {}
basedir = os.path.dirname(__file__) + '/Musics/'
music_list = Music()
queues = {}
channel  = None
currentQue = {}
numbers = []
@client.event
async def on_ready():
    print('Logged in as', client.user.name)
    print(client.user.id)
    print('================')


@client.command(pass_context=True)
async def join(ctx):
    """Подключить бота.
        Для воспроизведения композиций из директории необходимо сначала подключить бота к каналу.
        В ином случае работать он не будет.

        Хорошего пользования! ))
    """
    print(os.path.dirname(__file__))
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    count = 0
    for m in music_list.getMusics():
        musics[count] = m
        count += 1

@client.command(pass_context=True)
async def leave(ctx):
    """Отключить бота."""
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context = True)
async def play(ctx):
    """Проигрывание track's из директории."""
    server = ctx.message.server
    voice = client.voice_client_in(server)
    try:
        player = voice.create_ffmpeg_player(basedir + currentQue[0], after=lambda: check_queue(server.id))
        players[server.id] = player
        music_list.count = 0
        player.start()
    except FileNotFoundError:
        await client.send_message(ctx.message.channel, 'Файл не найден. Проверте корректность имени.')

@client.command(pass_context = True)
async def skip(ctx):
    """Пропустить track"""
    server = ctx.message.server
    player = players[server.id]
    player.stop()

@client.command(pass_context = True)
async def list(ctx):
    """Вывод списка файлов .mp3 из директории."""

    for k,v in musics.items():
        await client.send_message(ctx.message.channel, str(k)+': '+ str(v))

@client.command(pass_context = True)
async def volume(ctx, vol:float):
    """Изменение уровня громкости.
        В качестве параметра принимается значение громкости от 0(минимум) до 200 (максимум)

        Parameters
        -------------
        volume: number [Required]
            После указания команды, необходимо указать через пробел уровень громкости от 0 до 200.
    """
    voice = client.voice_client_in(ctx.message.server)
    player = players[ctx.message.server.id]
    print('Change volume : ', vol)
    player.volume = vol /100

@client.command(pass_context = True)
async def pause(ctx):
    """Пауза"""
    player = players[ctx.message.server.id]
    player.pause()

@client.command(pass_context = True)
async def resume(ctx):
    """Возобновление"""
    player = players[ctx.message.server.id]
    player.resume()
    await client.send_message(ctx.message.channel, 'Resume')


@client.command(pass_context = True, aliases = ['q', 'playlist'])
async def queue(ctx, *key:int):
    print(key)
    count = 0
    for k in key:
        try:
            if musics[k] !=[]:
                numbers.append(k)
                file = musics.get(k)
                currentQue[count] = musics.get(k)
                server = ctx.message.server
                voice = client.voice_client_in(server)
                player = voice.create_ffmpeg_player(basedir+file, after= lambda : check_queue(server.id))

                if server.id in queues:
                    queues[server.id].append(player)
                else:
                    queues[server.id] = [player]
                count +=1
                await client.say('Track {0} поставлен в очередь.'.format(file))
        except KeyError:
            print('Ошибка! Не такого ключа')
    await client.say('Queue successfully created!')


@client.command(pass_context=True)
async def save_queue(ctx):
    file = os.path.dirname(__file__) + '/queue.txt'
    f = open(file, 'w')
    for n in numbers:
        f.write(str(n))
    f.close()
    await client.say('Queue saved.')
@client.command(pass_context = True)
async def load_queue(ctx):
    file = os.path.dirname(__file__) + '/queue.txt'
    f = open(file, 'r')
    for line in f:
        a =line.split(':')[0]
        await auto_queue(ctx,*tuple(a))
    f.close()
    await client.say('Queue successfully loaded!')


async def auto_queue(ctx, *key:int):
    count = 0
    for k in key:
        try:
            if musics[int(k)] != []:
                numbers.append(int(k))
                file = musics.get(int(k))
                currentQue[count] = musics.get(int(k))
                server = ctx.message.server
                voice = client.voice_client_in(server)
                player = voice.create_ffmpeg_player(basedir + file, after=lambda: check_queue(server.id))

                if server.id in queues:
                    queues[server.id].append(player)
                else:
                    queues[server.id] = [player]
                count += 1
        except KeyError:
            print('Ошибка! Не такого ключа')

@client.command(pass_context = True, aliases = ['current','now'])
async def now_playing(ctx):
    print(currentQue)
    current_count = music_list.count
    current_count -= 1
    if current_count < 0:
        current_count = 0
    music = currentQue[current_count]
    await client.say('Сейчас играет :: '+music[:len(music)-4]+' '+music_list.get_track_duration(basedir+currentQue[current_count]))

def check_queue(id,):
    if queues[id] != []:
        music_list.inc_count()
        player = queues[id].pop(0)
        players[id] = player
        player.start()
if __name__=='__main__':
    client.run(BOT_TOKEN)