import discord
from discord.ext import commands
from controller.controller import AccountController

intents = discord.Intents.default()
intents.members = False
intents.message_content = True

# define Bot with **needed** parameters
bot = commands.Bot(command_prefix="$", intents=intents)
controller = AccountController

@bot.command(name="abrir_conta")
async def abrir_conta(ctx):
    name = ctx.author
    controller.add_account(name)
    await ctx.send(f'Conta para {name} criada.')

@bot.command(name='salto')
async def salto(ctx):
    name = ctx.author
    account = controller.get_account(name)
    if account is None:
        await ctx.send(f'Conta para {name} não encontrada.')
    else:
        message = f'Saldo de {account.name}:'
        message += f'\nBronze: {account.bronze}'
        message += f'\nPrata: {account.silver}'
        message += f'\nOuro: {account.gold}'
        message += f'\nPlatina: {account.platinum}'
        await ctx.send(message)

@bot.command(name='depósito')
async def deposito(ctx, type, amount):
    name = ctx.author
    account = controller.get_account(name)
    if account is None:
        await ctx.send(f'Conta para {name} não encontrada.')
    else:
        if type == 'bronze':
            account.bronze += int(amount)
        elif type == 'silver':
            account.silver += int(amount)
        elif type == 'gold':
            account.gold += int(amount)
        elif type == 'platinum':
            account.platinum += int(amount)
        else:
            await ctx.send('Tipo de moeda inválido.')
            return
        if controller.update_account(account):
            await ctx.send(f'{amount} {type} depositado na conta de {name}.')
        else:
            await ctx.send('Saldo de moeda excede o limite permitido.')

@bot.command(name='sacar')
async def sacar(ctx, type, amount):
    name = ctx.author
    account = controller.get_account(name)
    if account is None:
        await ctx.send(f'Conta para {name} não encontrada.')
    else:
        if type == 'bronze':
            account.bronze -= int(amount)
        elif type == 'silver':
            account.silver -= int(amount)
        elif type == 'gold':
            account.gold -= int(amount)
        elif type == 'platinum':
            account.platinum -= int(amount)
        else:
            await ctx.send('Tipo de moeda inválido.')
            return
        if controller.update_account(account):
            await ctx.send(f'{amount} {type} sacado da conta de {name}.')
        else:
            await ctx.send('Saldo de moeda insuficiente ou excede o limite permitido.')

@bot.command(name='delete')
async def delete(ctx, name):
    controller.delete_account(name)
    await ctx.send(f'Conta para {name} excluída.')


@bot.command(name='converter')
async def converter(ctx,  from_type, to_type, amount):
    name = ctx.author
    account = controller.get_account(name)
    if account is None:
        await ctx.send(f'Conta para {name} não encontrada.')
    else:
        if controller.convert(account, from_type, to_type, int(amount)):
            await ctx.send(f'{amount} {from_type} convertido para {amount * 10 ** (to_type - from_type)} {to_type} na conta de {name}.')
        else:
            await ctx.send(f'Conversão inválida ou saldo insuficiente na conta de {name}.')


@bot.command(name='transferir')
async def transferir(ctx,  receiver, amount):
    sender= ctx.author
    if controller.transfer(sender, receiver, int(amount)):
        await ctx.send(f'{amount} de moedas transferidas da conta de {sender} para a conta de {receiver}.')
    else:
        await ctx.send('Transferência inválida ou saldo insuficiente na conta de origem.')



@bot.command()
async def close(ctx):
    controller.close()  
@bot.command(name='help')
async def help(ctx):
    help_text = '''
    **Comandos disponíveis:**
    `$abrir_conta`: abre uma nova conta.
    `$salto`: exibe o saldo de uma conta.
    `$depósito [tipo] [quantidade]`: deposita uma certa quantidade de moedas em uma conta.
    `$sacar [tipo] [quantidade]`: saca uma certa quantidade de moedas de uma conta.
    `$converter [de] [para] [quantidade]`: converte uma certa quantidade de moedas de um tipo para outro.
    `$transferir [destinatário] [quantidade]`: transfere uma certa quantidade de moedas para outra conta.
    `$delete [nome]`: exclui uma conta.
    '''
    await ctx.send(help_text)


TONCK = None
bot.run(TONCK)