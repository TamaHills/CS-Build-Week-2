from json import loads, dumps
import requests
import time

maze_map = loads(open('map', 'r').read())

def find_path(room_id, target):
    path = []
    q = []
    visited = set()

    q.insert(0, [(room_id, '')])

    while len(q) > 0:
        path = q.pop()
        r, d = path[-1]
        for e in maze_map[r].keys():
            next_room = maze_map[r][e]
            if next_room not in visited and next_room != '?':
                if next_room == target:
                    return (path + [(next_room, e)])[1:]
                visited.add(next_room)
                q.insert(0, path + [(next_room, e)])


BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api"
headers = {"Authorization": f"Token {input('token >>>')}"}
r = requests.get(url=BASE_URL+"/adv/init", headers=headers)

time.sleep(r.json()['cooldown'] + 1)

for room_id, direction in find_path(str(r.json()['room_id']), input('target>>>')):
    body = {"direction": direction, "next_room_id": room_id}
    r = requests.post(url=BASE_URL+"/adv/move",
                      json=body, headers=headers)
    next_room = r.json()
    print(next_room)
    time.sleep(next_room['cooldown'] + 1)
