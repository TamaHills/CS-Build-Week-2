from stack import Stack

import requests
import random
from ast import literal_eval

import time

traversal_path = []
visited = []

BASE_URL = "https://lambda-treasure-hunt.herokuapp.com/api"
headers={"Authorization": "Token 103b91d44d0b4d88ee6d3a6fda97355cafc575b0"}

def explore(traversal_path=None, visitied=None):
    trackBack = Stack()
    thisRoom = requests.get(url=BASE_URL+"/adv/init", headers=headers)
    print(thisRoom)
    visited.append(thisRoom)
    roomExits = thisRoom['exits']
    roomNumbers = []

    for direction in roomExits:
        roomNumbers.append(thisRoom.get_room_in_direction(direction))

    unexploredDirections = []

    for room in roomNumbers:
        if room.id not in visited:
            unexploredDirections.append(roomExits[roomNumbers.index(room)])

    if len(unexploredDirections) > 0:
        direction = random.randint(0, len(unexploredDirections)-1)
        moveDir = unexploredDirections[direction][0]
        trackBackDir = ''
        if moveDir == 'n':
            trackBackDir = 's'
        if moveDir == 's':
            trackBackDir = 'n'
        if moveDir == 'e':
            trackBackDir = 'w'
        if moveDir == 'w':
            trackBackDir = 'e'

        if len(unexploredDirections) >= 1:
            pathBack = []
            trackBack.push(pathBack)

        print("here")
        pathBack.append(trackBackDir)
        r = requests.post(url=BASE_URL+"/adv/move", json= {"direction": direction}, headers=headers)
        cooldown = r.json()["cooldown"]
        time.sleep(cooldown + .2)
        print(r)
        traversal_path.append(moveDir)

    if len(unexploredDirections) == 0:
        if trackBack.size() > 0:
            pathBack = trackBack.pop()
            while len(pathBack) > 0:
                move = pathBack[-1]
                del pathBack[-1]
                requests.post(url=BASE_URL+"/adv/move", json= {"direction": move}, headers=headers)
                cooldown = r.json()["cooldown"]
                time.sleep(cooldown + .2)
                traversal_path.append(move)
        else:
            return traversal_path

    return traversal_path

explore()