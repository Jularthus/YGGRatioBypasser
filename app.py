from requests import post
import json 
from os import system
properties = open('properties.json')
properties = json.load(properties)  #Le mot de passe est stocké dans un fichier à part
from time import sleep
from datetime import datetime
from sys import stdout


system("title " + 'YGGRatioBypasser by JA')
print('''
██╗░░░██╗░██████╗░░██████╗░  ██████╗░░█████╗░████████╗██╗░█████╗░
╚██╗░██╔╝██╔════╝░██╔════╝░  ██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗
░╚████╔╝░██║░░██╗░██║░░██╗░  ██████╔╝███████║░░░██║░░░██║██║░░██║
░░╚██╔╝░░██║░░╚██╗██║░░╚██╗  ██╔══██╗██╔══██║░░░██║░░░██║██║░░██║
░░░██║░░░╚██████╔╝╚██████╔╝  ██║░░██║██║░░██║░░░██║░░░██║╚█████╔╝
░░░╚═╝░░░░╚═════╝░░╚═════╝░  ╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░

██████╗░██╗░░░██╗██████╗░░█████╗░░██████╗░██████╗          ██████╗░██╗░░░██╗  ░░░░░██╗░█████╗░
██╔══██╗╚██╗░██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝          ██╔══██╗╚██╗░██╔╝  ░░░░░██║██╔══██╗
██████╦╝░╚████╔╝░██████╔╝███████║╚█████╗░╚█████╗░    V2!   ██████╦╝░╚████╔╝░  ░░░░░██║███████║
██╔══██╗░░╚██╔╝░░██╔═══╝░██╔══██║░╚═══██╗░╚═══██╗          ██╔══██╗░░╚██╔╝░░  ██╗░░██║██╔══██║
██████╦╝░░░██║░░░██║░░░░░██║░░██║██████╔╝██████╔╝          ██████╦╝░░░██║░░░  ╚█████╔╝██║░░██║
╚═════╝░░░░╚═╝░░░╚═╝░░░░░╚═╝░░╚═╝╚═════╝░╚═════╝░          ╚═════╝░░░░╚═╝░░░  ░╚════╝░╚═╝░░╚═╝

Lancement en cours...
''', end="")

reqID = 1
tracker_org = properties["tracker_org"]

url = "http://127.0.0.1:8112/json"
headers = {'Accept': 'application/json',
           'Content-Type': 'application/json'}
data = {"id": reqID, "method": "auth.login", "params": [properties["pwd"]]}

def hour():
    return "[" + str(datetime.now().hour) + ":" + str(datetime.now().minute) + "]"

while 1:
    try:
        getAuth = post(url, headers=headers, json=data)
        break
    except:
        stdout.write('\x1b[1A')
        print(f'{hour()} Deluge est indisponible pour l\'IP indiquée ({url}). Nouvel essai dans 3 secondes.')
        sleep(1)
        stdout.write('\x1b[1A')
        print(f'{hour()} Deluge est indisponible pour l\'IP indiquée ({url}). Nouvel essai dans {3} secondes..')
        sleep(1)
        stdout.write('\x1b[1A')
        print(f'{hour()} Deluge est indisponible pour l\'IP indiquée ({url}). Nouvel essai dans {2} secondes...')
        sleep(1)
        stdout.write('\x1b[1A')
        print(f'{hour()} Deluge est indisponible pour l\'IP indiquée ({url}). Nouvel essai dans {1} secondes.     ')
headers['Cookie'] = getAuth.headers['Set-Cookie'].split(";")[0]

stdout.write('\x1b[1A')
print('''Le bypass est correctement lancé !''')

#Permet de récupérer tous les torrents qui ont un certain tracker_org
def getSpecificTorrentsList(tracker):
    global reqID
    reqID += 1
    data = {"method":"web.update_ui","params":[["queue","name","total_wanted","state","progress","num_seeds","total_seeds","num_peers","total_peers","download_payload_rate","upload_payload_rate","eta","ratio","distributed_copies","is_auto_managed","time_added","tracker_host","download_location","last_seen_complete","total_done","total_uploaded","max_download_speed","max_upload_speed","seeds_peers_ratio","total_remaining","completed_time","time_since_transfer","label"],{"tracker_host":tracker}],"id":reqID}
    req = post(url, headers=headers, json=data)
    return req.json()

#Récupère l'entièreté des torrents
def getAllTorrentsList():
    global reqID
    reqID += 1
    data = {"method":"web.update_ui","params":[["queue","name","total_wanted","state","progress","num_seeds","total_seeds","num_peers","total_peers","download_payload_rate","upload_payload_rate","eta","ratio","distributed_copies","is_auto_managed","time_added","tracker_host","download_location","last_seen_complete","total_done","total_uploaded","max_download_speed","max_upload_speed","seeds_peers_ratio","total_remaining","completed_time","time_since_transfer","label"],{}],"id":reqID}
    req = post(url, headers=headers, json=data)
    return req.json()
    
#Supprime tous les tracker d'un torrent en fonction de son ID
def deleteTrackers(torrentID, name):
    global reqID
    reqID += 1
    data = {"method":"core.set_torrent_trackers","params":[torrentID,[]],"id":reqID}
    post(url, headers=headers, json=data)
    print(f'{hour()} [ DEL ] Trackers supprimés pour {name} !\n')
    discord_data = {"username":"YGGRatioBypass", "content":"<@433560387305340928>", "embeds":[{"title": f":white_check_mark: Trackers supprimés pour `{name}`","color": 0x00bb19,"footer": {"text": "YGGRatioBypass"}}]}
    post(properties["webhook_url"], json=discord_data)

#Rajoute un tracker (-> s'est révélé parfaitement inutile mais fonctionnel)
def addTrackers(torrentID, name, tracker):
    global reqID
    reqID += 1
    data = {"method":"core.set_torrent_trackers","params":[torrentID,[{"tier":0,"url":tracker}]],"id":reqID}
    post(url, headers=headers, json=data)
    print(f'{hour()} [ OK ] Trackers mis à jour pour {name} ({tracker})!\n')

#verification que le torrent ne possede pas le tracker (actualisation lente de l'UI Deluge -> c'est obligatoire)
def checkTracker(torrentID):
    global reqID
    reqID += 1
    data = {"method":"core.get_torrent_status","params":[torrentID,["trackers"]],"id":reqID}
    a = post(url, headers=headers, json=data)
    if a.json()['result']['trackers']:
        return True
    else:
        return False

#Le programme qui tourne en boucle
def auto():
    global reqID
    for j in getSpecificTorrentsList(tracker_org)['result']['torrents']:
        progress = getSpecificTorrentsList(tracker_org)['result']['torrents'][j]['progress']
        if progress>0 and progress<100:
            if checkTracker(j):
               deleteTrackers(j, getSpecificTorrentsList(tracker_org)['result']['torrents'][j]['name'])



while 1:
    auto()
    sleep(5)