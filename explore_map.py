from stack import Stack

import requests
import random
from ast import literal_eval
from json import dumps, loads
import time


BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api"
headers = {"Authorization": f"Token {input('token >>>')}"}

reverse_map = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

starting_map = {}

with open('map', 'r') as f:
    m = f.read()
    starting_map = loads(m)


def explore_map(maze_map, starting_room):
    unexplored = {}

    room = starting_room

    s = Stack()

    s.push('exit')

    while s.size() > 0:
        room_id = str(room['room_id'])
        if not maze_map.get(room_id):
            maze_map[room_id] = {}
            for e in room['exits']:
                maze_map[room_id][e] = '?'

        if unexplored.get(room_id) is None:
            unexplored[room_id] = room['exits']

        print('stack size:', s.size())
        if s.size() > 50:
            unexplored[next_room_id] = [
                ex for ex in room['exits'] if maze_map[room_id][ex] == '?']

        if len(unexplored[room_id]) > 0:
            e = unexplored[room_id].pop()
            s.push(reverse_map[e])
        else:
            e = s.pop()

        body = {"direction": e}

        if maze_map[room_id][e] != '?':
            body["next_room_id"] = str(maze_map[room_id][e])

        print(body)
        r = requests.post(url=BASE_URL+"/adv/move", json=body, headers=headers)

        data = r.json()

        next_room_id = str(data['room_id'])

        if not maze_map.get(next_room_id):
            maze_map[next_room_id] = {}
            for ex in data['exits']:
                maze_map[next_room_id][ex] = '?'

        if unexplored.get(next_room_id) is None:
            unexplored[next_room_id] = data['exits']

        maze_map[room_id][e] = next_room_id

        maze_map[next_room_id][reverse_map[e]] = room_id

        if len(unexplored[next_room_id]) > 0 and reverse_map[e] in unexplored[next_room_id]:
            unexplored[next_room_id].remove(reverse_map[e])

        print(next_room_id, unexplored[next_room_id])
        # print(maze_map)
        print(len(maze_map.keys()), 'rooms mapped')
        with open('map', 'w') as f:
            f.truncate()
            f.write(dumps(maze_map))
            f.close()
            
        print(data['cooldown'])
        time.sleep(data['cooldown'])
        for item in data['items']:
            if 'treasure' in item:
                body = {"name": item}
                r = requests.post(url=BASE_URL+"/adv/take",
                                  json=body, headers=headers)
                print('took', item)
                print(r.json())
                time.sleep(r.json()['cooldown'])

        room = data
        print(data)
        
        
        


r = requests.get(url=BASE_URL+"/adv/init", headers=headers)
print(starting_map)
data = r.json()
time.sleep(data['cooldown'])
explore_map(starting_map, data)
