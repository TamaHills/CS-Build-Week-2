from stack import Stack

import requests
import random
from json import dumps, loads
import time

maze_map = loads(open('map', 'r').read())

visited = set()

tmap = {}

BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api"
headers = {"Authorization": "Token ce973da1f80b171cc2de6e4310f51fd2600d2614"}

r = requests.get(url=BASE_URL+"/adv/init", headers=headers)
data = r.json()
time.sleep(data['cooldown'] + 1)

def search_map(room):
    room_id = str(room['room_id'])
    if room_id not in visited:
        tmap[room_id] = room
        print(room)
        visited.add(room_id)
        print(visited)
        room_map = maze_map[room_id]
        for r in room['exits']:
            print(room_map)
            if room_map[r] not in visited:
                print(True)
                body = {"direction": r, "next_room_id": room_map[r]}
                r = requests.post(url=BASE_URL+"/adv/move",
                                  json=body, headers=headers)
                next_room = r.json()
                time.sleep(next_room['cooldown'] + 1)

                for item in next_room['items']:
                    
                    if 'treasure' in item:
                        body = { "name": item}
                        r = requests.post(url=BASE_URL+"/adv/take",
                                  json=body, headers=headers)
                        print('took', item)
                        print(r.json())
                        time.sleep(r.json['cooldown'])

                search_map( next_room)

                with open('search', 'w') as f:
                    f.truncate()
                    f.write(dumps(tmap))
                    f.close()


search_map(data)
