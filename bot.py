import discord, time, re, asyncio, random, requests
time, re, asyncio, random, requests
from discord.ext import commands
from termcolor import colored
from unidecode import unidecode
from threading import Thread

Arquivos = {
    'main.py': 'https://raw.githubusercontent.com/Kameil/autocatch3chats-termux/main/main.py', 'bot.py': 'https://raw.githubusercontent.com/Kameil/autocatch3chats-termux/main/bot.py', 'data/pokemon': 'https://raw.githubusercontent.com/Kameil/autocatch3chats-termux/main/data/pokemon', 'data/legendary': 'https://raw.githubusercontent.com/Kameil/autocatch3chats-termux/main/data/legendary', 'data/mythical': 'https://raw.githubusercontent.com/Kameil/autocatch3chats-termux/main/data/mythical'
    }

version = '2.8 codigo otmizado'
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'
}

# bota os CATCH ID AI TA LIGADO PQ OREA SECA E DESENROLADO

catch_ids = []

from config import *

for catch_id in [catch_id, catch_id2, catch_id3, catch_id4, catch_id5, catch_id6]:
    catch_ids.append(catch_id)

catch_ids = [catch_id for catch_id in catch_ids if catch_id != '']
with open('data/pokemon', 'r', encoding='utf8') as file:
    pokemon_list = file.read()

def CarregarPokemons():
    global pokemon_list
    print('Carregando lista dos Pokemons..')
    try:
        url = Arquivos['data/pokemon']
        pokemons = requests.get(url)
        if pokemons.status_code == 200:
            with open('data/pokemon', 'w', encoding='utf8') as PokemonList:
                PokemonList.write(pokemons.text)
                print('lista dos pokemons atualizada.')
        else:
            print('nao foi possivel atualizar a lista dos pokemons.')
    except:
        pass
    with open('data/pokemon', 'r', encoding='utf8') as file:
        pokemon_list = file.read()

Thread(target=CarregarPokemons).start()




def decidirtimesleep():
    return 0

with open('data/legendary', 'r') as file:
    legendary_list = file.read()
with open('data/mythical', 'r') as file:
    mythical_list = file.read()
with open('data/level', 'r') as file:
    to_level = file.readline()

num_pokemon = 0
shiny = 0
legendary = 0
mythical = 0
captcha_content = None
captcha = False
poketwo = 716390085896962058
Mpoketwo = "<@" + str(poketwo) + ">"
client = commands.Bot(command_prefix=[f"{prefix} ", f"{prefix}"], help_command=None)
def solve(message):
    hint = []
    for i in range(15, len(message) - 1):
        if message[i] != '\\':
            hint.append(message[i])
    hint_string = ''
    for i in hint:
        hint_string += i
    hint_replaced = hint_string.replace('_', '.')
    solution = re.findall('^' + hint_replaced + '$', pokemon_list, re.MULTILINE)
    return solution


paused = False

@client.event
async def on_ready():
    print(colored(f'Autocatch em execuçao em : {client.user.name}', 'black', 'on_white'))
    try:
        channel = client.get_channel(int(catch_ids[0]))
        if channel:
            await asyncio.sleep(2)
            pro = ["autocatch online.", "ac online", "ac on", "autocatch on"]
            await channel.send(random.choice(pro))
        else:
            print(colored(f"Nao foi possivel obter o canal: {catch_id}!", "red"))
    except Exception as e:
        print(colored(f"Ocorreu um erro: {e}", "red"))


def remover_emojis(texto): 
     texto_sem_emojis = texto.replace('♀️', '').replace('♂️', '') 
     return texto_sem_emojis 
  

 
         
def remover_acentos(palavra):
    return unidecode(palavra)
  
  
def limpar_texto(texto): 
    texto_sem_emojis = remover_emojis(texto) 
    texto_sem_acentos = remover_acentos(texto_sem_emojis) 
    return texto_sem_acentos

@client.event
async def on_message(message : discord.Message):
    global paused, captcha_content, captcha
    if str(message.channel.id) in catch_ids:
        if message.author.id == poketwo:
            if not paused:
                if message.embeds:
                    embed_title = message.embeds[0].title
                    if 'wild pokémon has appeared!' in embed_title:
                        async with message.channel.typing():
                            await asyncio.sleep(random.uniform(0.5, 1.4))
                            await message.channel.send(f'{Mpoketwo} h')
                else:
                    content = message.content
                    if 'The pokémon is ' in content:
                        if not len(solve(content)):
                            print('Pokemon not found.')
                        else:
                            for i in solve(content):
                                async with message.channel.typing():
                                    timesleep = random.uniform(0.8, 2.3)
                                    pokemon_name = limpar_texto(i.lower())
                                    await asyncio.sleep(timesleep)
                                    await message.channel.send(f'{Mpoketwo} c {pokemon_name}')
                    elif 'Congratulations' in content:
                        global shiny
                        global legendary
                        global num_pokemon
                        global mythical
                        num_pokemon += 1
                        split = content.split(' ')
                        pokemon = split[7].replace('!', '')
                        if 'seem unusual...' in content:
                            shiny += 1
                            print(f'Shiny Pokémon caught! Pokémon: {pokemon}')
                            print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                        elif re.findall('^' + pokemon + '$', legendary_list, re.MULTILINE):
                            legendary += 1
                            print(f'Legendary Pokémon caught! Pokémon: {pokemon}')
                            print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                        elif re.findall('^' + pokemon + '$', mythical_list, re.MULTILINE):
                            mythical += 1
                            print(f'Mythical Pokémon caught! Pokémon: {pokemon}')
                            print(f'Shiny: {shiny} | Legendary: {legendary} | Mythical: {mythical}')
                        else:
                            print(f'Total Pokémon Caught: {num_pokemon} :{pokemon}')
                    elif 'human' in content:
                        paused, captcha = True, True
                        captcha_content = message.content
                        async with message.channel.typing():
                            await asyncio.sleep(random.uniform(0.5,3.5))
                            await message.channel.send(f'<@{ping}> Captcha Detectado! Bot pausado.')
                        
    if not message.author.bot:
        await client.process_commands(message)
  
"""
Comando desativado
@client.command()
async def say(ctx, *, args):
    if str(ctx.channel.id) in str(catch_ids):
        await ctx.send(args)
"""

@client.command()
async def start(ctx):
    global paused
    async with ctx.typing():
        if str(ctx.channel.id) in catch_ids:
            await asyncio.sleep(random.uniform(0.5, 0.9))
            if not paused:
                await ctx.send('Bot ja esta em Execuçao.')
            else:
                paused = False
                await ctx.send('Bot Iniciado.')

@client.command()
async def stop(ctx):
    global paused
    async with ctx.typing():
        if str(ctx.channel.id) in catch_ids:
            await asyncio.sleep(random.uniform(0.5, 0.9))
            if not paused:
                paused = True
                await ctx.send('Bot Pausado.')
            else:
                await ctx.send('Bot Ja esta pausado.')
      


      

def Alerts():
    time.sleep(1)
    print(colored(f'\nPokétwo Autocacther.\n\nsò mitada violenta.', 'black', 'on_light_cyan')) 
    print(colored(f'Versao: {version} || TERMUX', 'black', 'on_white')) 
    print(colored(f'o prefix do autocatch é "{prefix}".\n\nuse {prefix}ajuda para ver a lista de comandos.', 'yellow')) 
    

def ProcurarAtualizaçoes():
    requisicoes = 1
    time.sleep(60)
    while True:
        for file, url in Arquivos.items():
            print(f'{requisicoes} - (GET)[{url}]')
            requisicoes += 1
            response = requests.get(url)
            if response.status_code == 200:
                with open(file, 'w', encoding="utf-8") as arch:
                    arch.write(response.text)
                    print(f'{file} Foi Recarregado.')
        time.sleep(600)


Thread(target=Alerts).start()
Thread(target=ProcurarAtualizaçoes).start()
try:
    client.run(f"{user_token}")
except discord.HTTPException as e:
    if e.status == 429:
        print(colored('Discord Recusou a Conexao com o Codigo De status: 429 too many requests.\n', 'red'), str(e))
        """
        FlasK.terminate()
        """
