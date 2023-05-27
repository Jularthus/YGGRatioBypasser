from requests import post
from properties import pwd, webhook_url  #Le mot de passe est stocké dans un fichier à part
from time import sleep
from os import system

system("title " + 'YGGRatioBypasser by JA')
print('''
██╗░░░██╗░██████╗░░██████╗░  ██████╗░░█████╗░████████╗██╗░█████╗░
╚██╗░██╔╝██╔════╝░██╔════╝░  ██╔══██╗██╔══██╗╚══██╔══╝██║██╔══██╗
░╚████╔╝░██║░░██╗░██║░░██╗░  ██████╔╝███████║░░░██║░░░██║██║░░██║
░░╚██╔╝░░██║░░╚██╗██║░░╚██╗  ██╔══██╗██╔══██║░░░██║░░░██║██║░░██║
░░░██║░░░╚██████╔╝╚██████╔╝  ██║░░██║██║░░██║░░░██║░░░██║╚█████╔╝
░░░╚═╝░░░░╚═════╝░░╚═════╝░  ╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░

██████╗░██╗░░░██╗██████╗░░█████╗░░██████╗░██████╗  ██████╗░██╗░░░██╗  ░░░░░██╗░█████╗░
██╔══██╗╚██╗░██╔╝██╔══██╗██╔══██╗██╔════╝██╔════╝  ██╔══██╗╚██╗░██╔╝  ░░░░░██║██╔══██╗
██████╦╝░╚████╔╝░██████╔╝███████║╚█████╗░╚█████╗░  ██████╦╝░╚████╔╝░  ░░░░░██║███████║
██╔══██╗░░╚██╔╝░░██╔═══╝░██╔══██║░╚═══██╗░╚═══██╗  ██╔══██╗░░╚██╔╝░░  ██╗░░██║██╔══██║
██████╦╝░░░██║░░░██║░░░░░██║░░██║██████╔╝██████╔╝  ██████╦╝░░░██║░░░  ╚█████╔╝██║░░██║
╚═════╝░░░░╚═╝░░░╚═╝░░░░░╚═╝░░╚═╝╚═════╝░╚═════╝░  ╚═════╝░░░░╚═╝░░░  ░╚════╝░╚═╝░░╚═╝

Le bypass est correctement lancé !
''')

reqID = 1
tracker_org = "joinpeers.org"

url = "http://127.0.0.1:8112/json"
headers = {'Accept': 'application/json',
           'Content-Type': 'application/json'}
data = {"id": reqID, "method": "auth.login", "params": [pwd]}

getAuth = post(url, headers=headers, json=data)
headers['Cookie'] = getAuth.headers['Set-Cookie'].split(";")[0]

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
    print(f'[ DEL ] Trackers supprimés pour {name} !\n')
    discord_data = {"username":"YGGRatioBypass", "embeds":[{"title": f":white_check_mark: Trackers supprimés pour `{name}`","color": 0x00bb19,"footer": {"text": "YGGRatioBypass"}}]}
    post(webhook_url, json=discord_data)

#Rajoute un tracker (-> s'est révélé parfaitement inutile mais fonctionnel)
def addTrackers(torrentID, name, tracker):
    global reqID
    reqID += 1
    data = {"method":"core.set_torrent_trackers","params":[torrentID,[{"tier":0,"url":tracker}]],"id":reqID}
    post(url, headers=headers, json=data)
    print(f'[ OK ] Trackers mis à jour pour {name} ({tracker})!\n')

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
            
    
    #Commandes pour rajouter le ratio a la fin
    #MEGA USELESS (le ratio s'actualise quand meme quand on rajoute à la fin)
    '''for a in getAllTorrentsList()['result']['torrents']:
        progress = getAllTorrentsList()['result']['torrents'][a]['progress']
        if progress==100 and not getAllTorrentsList()['result']['torrents'][a]['tracker_host'] == "joinpeers.org":
             addTrackers(a, getAllTorrentsList()['result']['torrents'][a]['name'], tracker)
    for e in getAllTorrentsList()['result']['torrents']:
        reqID += 1
        data = {"method":"web.get_torrent_status","params":[e,["tracker_status"]],"id":reqID}
        status = post(url, headers=headers, json=data).json()['result']['tracker_status']
        if "Error" in status and not "Not Found" in status:
            addTrackers(e, getSpecificTorrentsList(tracker_org)['result']['torrents'][e]['name'], tracker[0:-41])
    '''

while 1:
    auto()
    sleep(5)
