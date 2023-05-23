from requests import post
from properties import pwd

reqID = 1

url = "http://localhost:8112/json"
headers = {'Accept': 'application/json',
           'Content-Type': 'application/json'}
data = {"id": reqID, "method": "auth.login", "params": [pwd]}

getAuth = post(url, headers=headers, json=data)
headers['Cookie'] = getAuth.headers['Set-Cookie'].split(";")[0]

def getTorrentsList():
    global reqID
    reqID += 1
    data = {"method":"web.update_ui","params":[["queue","name","total_wanted","state","progress","num_seeds","total_seeds","num_peers","total_peers","download_payload_rate","upload_payload_rate","eta","ratio","distributed_copies","is_auto_managed","time_added","tracker_host","download_location","last_seen_complete","total_done","total_uploaded","max_download_speed","max_upload_speed","seeds_peers_ratio","total_remaining","completed_time","time_since_transfer","label"],{"tracker_host":"tracker.wf"}],"id":reqID}
    req = post(url, headers=headers, json=data)
    return req.json()
    

def setTrackers(torrentID, name):
    global reqID
    reqID += 1
    data = {"method":"core.set_torrent_trackers","params":[torrentID,[]],"id":reqID}
    post(url, headers=headers, json=data)
    print(f'Trackers supprimés pour {name} !')

def checker():
    for i in getTorrentsList()['result']['torrents']:
        setTrackers(i, getTorrentsList()['result']['torrents'][i]['name'])

while 1:
    checker()
    print('t')