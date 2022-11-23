from asyncio import tasks
import datetime
import telegramMain
from discord.ext import commands
import asyncio 


bot = commands.Bot("!")    


@bot.event
async def on_ready():
    print(f"Estou pronto! Estou conectado como {bot.user}")
    current_time.start()

@bot.event
async def on_message(message):
#algo síncrono: é executado em ordem de chegada(muitas vezes é demorado, espera um para realizar o outro)
#assíncrona (ASYNC): não precisa de esperar a finalização de outrs comandos para executar o próximo
    if message.author == bot.user:
        return

    if "palavrão" in message.content:
        await message.channel.send(f"Por favor, {message.author.name}, não ofenda")
        await message.delete()
        #AWAIT aerve para esperar para que o próximo seja executado, espera enviar a mensagem para continuar

    await bot.process_commands(message)
    # for the bot precess all the commands using the (message)

    

# quando digitar o prefixo (!) mais oi ele chama a função !oi
@bot.command(name="oi")
async def send_hi(ctx):
    name = ctx.author.name

    response = "Olá, " + name

    await ctx.send(response)

@tasks.loop(seconds=10)
async def current_time():
    now = datetime.datetime.now()

    now = now.strftime("%d/%m/%Y às %H:%M:%S")

    channel = bot.get_channel(1022289024737607783)
    await channel.send("Data atual: " + now)

bot.run("MTAyMjI4NzI2NDY2NTA0MzA5NQ.GFXMJt.DZjpD4LaJ80UOCPdg_PyZBQaVGPX7nlUHGJBGU")
    
