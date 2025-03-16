import discord
from discord.ext import commands
import sys

from fonction import extract_data_from_soup, youtube_search,make_choice, make_url, download

#-------------------- on récupère le token
with open("./code/token.txt","r",encoding="utf-8") as fichier :
    token= fichier.readline()

# #-------------------- on choisit le préfixe pour nos commandes, ici !
# intents = discord.Intents.default()
# intents.messages = True

# bot = commands.Bot(command_prefix="!", intents=intents)

# ##########################################################################
# # à la connexion
# ##########################################################################
# @bot.event
# async def on_ready():
#     channel = discord.utils.get(bot.get_all_channels(), name="général")  #remplacer "général" par le nom du salon
#     await bot.get_channel(channel.id).send("Bonjour à tous !")
#     print(f"{bot.user.name} est prêt.")  


# ##########################################################################
# # en cas d'erreur dans les commandes
# ##########################################################################
# @bot.event
# async def on_command_error(ctx,error):
#     if isinstance(error,commands.CommandNotFound):
#         await ctx.reply("Vérifier votre commande.")
#     else :
#         raise error


# ##########################################################################
# # Coucou
# ##########################################################################
# @bot.command(name="coucou")
# async def bonjour(ctx):
#     reponse=f"Ça va, {ctx.message.author.name} ?"
#     await ctx.reply(reponse)
#     print(f"Réponse à message {ctx.message.id} : {reponse}")

# ##########################################################################
# # envoyer_audio
# ##########################################################################

# @bot.command(name="envoyer_audio")
# async def envoyer_audio(ctx):
#     print('ok')
#     # Spécifie le chemin de ton fichier audio
#     file_path = "Alfons - Basta Boi.m4a"  # Remplace par le chemin de ton fichier audio

#     # Envoie le fichier audio dans le salon où la commande a été appelée
#     await ctx.send("Voici ton fichier audio :", file=discord.File(file_path))

# ##########################################################################
# # Déconnexion
# ##########################################################################
# @bot.command(name="exit")
# async def exit(ctx):
#     reponse="Bot déconnecté. Bye Bye !"
#     await ctx.reply(reponse)
#     await bot.close()
#     print(f"Réponse à message {ctx.message.id} : {reponse}")


# ##########################################################################
# ##########################################################################
# ##########################################################################
# # Exécution du bot
# ##########################################################################
# ##########################################################################
# ##########################################################################

# import discord
# from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True  # Utilisez cet intent pour lire les messages

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')
    channel = discord.utils.get(bot.get_all_channels(), name="général")  #remplacer "général" par le nom du salon
    await bot.get_channel(channel.id).send("Bonjour à tous !")


@bot.command(name='music')
async def music(ctx, *, titre: str):
    soupe = youtube_search(titre)
    video_info = extract_data_from_soup(soupe)
    msg = make_choice(video_info, True)
    await ctx.send(msg)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
        nombre = int(msg.content)
        file_path = download(make_url(video_info[nombre][0]))
        await ctx.send("Voici ton fichier audio :", file=discord.File(file_path))
        # await ctx.send(f"{resultat}.")
    except ValueError:
        await ctx.send("Le deuxième nombre n'est pas valide. Veuillez entrer un nombre valide.")
    except TimeoutError:
        await ctx.send("Temps écoulé. Veuillez réessayer la commande.")

bot.run(token)
