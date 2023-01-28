
from modelos.modelo import Banco
import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.members = False
intents.message_content = True

# define Bot with **needed** parameters
bot = commands.Bot(command_prefix="$", intents=intents)

# You can now use `@bot.tree.command()` as a decorator:
@bot.command(name="cria_conta")
async def cria_conta(ctx):
  id= ctx.author.discriminator
  ser = ctx.guild.name
  contar= Banco(id=id,server=ser)
  msm=contar.abrir_conta()
  await ctx.send(f"{ctx.author} {msm}")
@bot.command(name="saldo")
async def saldo(ctx):
  id= ctx.author.discriminator
  ser = ctx.guild.name
  contar= Banco(id=id,server=ser)
  salto = contar.consuta()
  if type(salto) == type(list()):
    bz = salto[0][0]
    ag = salto[0][1]
    au = salto[0][2]
    pt = salto[0][3]
    print(bz,ag,au,pt)
    await ctx.send(f"""Bz:` {bz} ` \nAg:` {ag} ` \nAu:` {au} ` \nPt:` {pt} `""")
#
bot.run(TONCK)