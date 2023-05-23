from requests import post
from properties import pwd
from time import sleep

reqID = 1
tracker = "joinpeers.org"

url = "http://localhost:8112/json"
headers = {'Accept': 'application/json',
           'Content-Type': 'application/json'}
data = {"id": reqID, "method": "auth.login", "params": [pwd]}

getAuth = post(url, headers=headers, json=data)
headers['Cookie'] = getAuth.headers['Set-Cookie'].split(";")[0]

def getSpecificTorrentsList(tracker):
    global reqID
    reqID += 1
    data = {"method":"web.update_ui","params":[["queue","name","total_wanted","state","progress","num_seeds","total_seeds","num_peers","total_peers","download_payload_rate","upload_payload_rate","eta","ratio","distributed_copies","is_auto_managed","time_added","tracker_host","download_location","last_seen_complete","total_done","total_uploaded","max_download_speed","max_upload_speed","seeds_peers_ratio","total_remaining","completed_time","time_since_transfer","label"],{"tracker_host":tracker}],"id":reqID}
    req = post(url, headers=headers, json=data)
    return req.json()

def getAllTorrentsList():
    global reqID
    reqID += 1      #A FAIRE SUPER IMPORTANT
    data = {"method":"web.update_ui","params":[["queue","name","total_wanted","state","progress","num_seeds","total_seeds","num_peers","total_peers","download_payload_rate","upload_payload_rate","eta","ratio","distributed_copies","is_auto_managed","time_added","tracker_host","download_location","last_seen_complete","total_done","total_uploaded","max_download_speed","max_upload_speed","seeds_peers_ratio","total_remaining","completed_time","time_since_transfer","label"],{"tracker_host":""}],"id":reqID}
    req = post(url, headers=headers, json=data)
    return req.json()
    

def deleteTrackers(torrentID, name):
    global reqID
    reqID += 1
    data = {"method":"core.set_torrent_trackers","params":[torrentID,[]],"id":reqID}
    post(url, headers=headers, json=data)
    print(f'❌ Trackers supprimés pour {name} !')

def addTrackers(torrentID, name):
    global reqID
    reqID += 1
    data = {"method":"core.set_torrent_trackers","params":[torrentID,[{"tier":0,"url":"http://connect.joinpeers.org:8080/xJpxLN32Qy8PRlOl6hYaoEsl8uAoFk9j/announce"}]],"id":reqID}
    post(url, headers=headers, json=data)
    print(f'✅ Trackers ajoutés pour {name} !')

def auto():
    for j in getSpecificTorrentsList(tracker)['result']['torrents']:
        progress = getSpecificTorrentsList(tracker)['result']['torrents'][j]['progress']
        if progress>0 and progress<100:
               deleteTrackers(j, getSpecificTorrentsList(tracker)['result']['torrents'][j]['name'])
    for a in getAllTorrentsList()['result']['torrents']:
        progress = getAllTorrentsList()['result']['torrents'][a]['progress']
        if progress==100:
             addTrackers(a, getAllTorrentsList()['result']['torrents'][a]['name'])
        
while True:
    auto()
    sleep(5)

#http://connect.joinpeers.org:8080/xJpxLN32Qy8PRlOl6hYaoEsl8uAoFk9j/announce