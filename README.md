# Music
Music est un outils pour télécharger des vidéos YouTube via un bot discord.

## installation
Pour récupérer installer ce module il suffit de télécharger le zip.  
Ou en ligne de commande :  
```
git clone https://github.com/MartinCalamel/Music.git
```

Pour le faire fonctionner il est nécessaire d'avoir python et d'installer les package requis.
```
pip install -r requirement.txt
``` 

Il faut également un token de bot discord stocker dans un fichier `Code/token.txt`  
  
Une autre possibilité est d'utiliser docker : 
```
docker pull martincalamel/music:0.1
docker run -e TOKEN="votre_tocken" docker.io/martincalamel/music:0.1
```

## usage
Pour le lancer entrez la commande :
```
python Code/bot.py

# ou bien 
python3 Code/bot.py
```
Le bot se connectera a discord.  
Pour communiquer avec lui il y a une unique commande :  
`!music titre de la musique`  
Après cela il vous enverra un message afin de préciser votre demande via 5 suggestion il faut lui renvoyer le numéro voulue dans les 30 secondes.  
Après un peu de temps un vocal vous est envoyer avec votre chanson.

## fonctionnement 
une fois le titre de la music reçu le bot va faire une requête a YouTube :  
```
url = f'https://www.youtube.com/results?search_query={query}&sp=EgIQAQ%253D%253D'
```
il en ressortira une soup (*objet de beautifulSoup*) dont on extraira les vidéos qui ne sont pas des sorts grace a la variable `ytInitialData` stocker dans un script de la page.
```
# on récupère l'ID et le titre des vidéos
video_info = [[video["videoRenderer"]["videoId"],video["videoRenderer"]["title"]["runs"][0]["text"]] for video in [ video for video in yt_initial_data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"] if "videoRenderer" in video.keys()]]
```
On en propose ensuite 5 à l'utilisateur qui nous revoie celui qu'il desire.  
Après cela on télécharge la video via `yt_dlp` et on l'envoie via discord.