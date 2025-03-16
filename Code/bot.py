import discord
from discord.ext import commands
import os
from fonction import extract_data_from_soup, youtube_search,make_choice, make_url, download

#-------------------- on récupère le token
with open("./code/token.txt","r",encoding="utf-8") as fichier :
    token= fichier.readline()

# on met les droit de lire les messages
intents = discord.Intents.default()
intents.messages = True  

# initialisation du bot
bot = commands.Bot(command_prefix='!', intents=intents)

# fonction pour que le bot envoie un message quand il est connecté
@bot.event
async def on_ready():
    print(f'Bot connecté en tant que {bot.user}')
    channel = discord.utils.get(bot.get_all_channels(), name="général")  #remplacer "général" par le nom du salon
    await bot.get_channel(channel.id).send("Bonjour à tous !")


# Commande pour télécharger la musique
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
        os.remove(file_path)
    except ValueError:
        await ctx.send("Le deuxième nombre n'est pas valide. Veuillez entrer un nombre valide.")
    except TimeoutError:
        await ctx.send("Temps écoulé. Veuillez réessayer la commande.")


if __name__ == '__main__':
    bot.run(token)
