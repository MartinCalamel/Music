"""
Author: Martin Calamel
Created: 2025-03-15
Description: fonction pour recuperer les videos youtubes
TODO: 
"""

# importation des modules
from bs4 import BeautifulSoup
import requests
import re
import json
import yt_dlp



def youtube_search(query:str):
    """
    fonction pour faire la requête de recherche YouTube
    """
    query = '+'.join(query.split())
    
    url = f'https://www.youtube.com/results?search_query={query}&sp=EgIQAQ%253D%253D'

    # Envoyer la requête HTTP pour obtenir la page de résultats
    response = requests.get(url)

    # Vérifier que la requête a réussi
    if response.status_code != 200:
        print(f"Erreur {response.status_code}: Impossible d'accéder à YouTube.")
        return []
    # Utiliser BeautifulSoup pour analyser le HTML de la page
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_data_from_soup(soup):
    """fonction pour récupperer les infos sur les vidéo a partir de la soup"""
    soup = str(soup)
    match = re.search(r'var ytInitialData = ({.*?});', soup, re.DOTALL)
    if match:
        yt_initial_data_str = match.group(1)

        try:
            yt_initial_data = json.loads(yt_initial_data_str)
            video_info = [[video["videoRenderer"]["videoId"],video["videoRenderer"]["title"]["runs"][0]["text"]] for video in [ video for video in yt_initial_data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"] if "videoRenderer" in video.keys()]]
            return video_info

        except json.JSONDecodeError as e:
            print(f"Erreur lors du chargement du JSON : {e}")
    else:
        print("Variable ytInitialData non trouvée.")

def make_choice(video,bot = False):
    """
    fonction pour proposer les choix de video retourne l'id de la video choisie
    """
    if bot:
        msg = ""
        msg += "choisissez la video que vous voulez télécharger\n"
        for i in range(5):
            msg += f'[ {i} ] {video[i][1]}\n'
        return msg
    print("choisissez la video que vous voulez télécharger")
    for i in range(5):
        print(f'[ {i} ] {video[i][1]}')
    return video[int(input(">>> "))][0]

def make_url(id):
    return f'https://youtu.be/{id}'

# def download(url):
#     ydl_opts = {
#         'format': 'm4a/bestaudio',  # Télécharge l'audio au format M4A
#         'outtmpl': './music/%(title)s.%(ext)s',  # Nom du fichier = titre de la vidéo
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])


def download(url):
    def clean_title(title):
        # Remplacer les caractères non valides par '-'
        return re.sub(r'[⧸/\\]', '-', title)

    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
        video_extension = "m4a"
        
        if video_title:
            # Nettoyer le titre avant de définir le nom du fichier
            safe_title = clean_title(video_title)
            ydl_opts = {
                'format': 'm4a/bestaudio',  # Télécharge l'audio au format M4A
                'outtmpl': f'./music/{safe_title}.%(ext)s',  # Utilisation du titre nettoyé
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            new_file_name = f'./music/{safe_title}.{video_extension}'
            return new_file_name
        else:
            return None


def main():
    query = input("Entrez le terme de recherche (ex: 'Python tutorial') : ")

    # Rechercher les vidéos
    soup = youtube_search(query)
    video_info = extract_data_from_soup(soup)
    video_id = make_choice(video_info)
    download(make_url(video_id))

if __name__ == '__main__':
    main()