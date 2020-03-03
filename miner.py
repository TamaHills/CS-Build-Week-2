import hashlib
import requests
import json
import random
import time

def proof_of_work(last_proof):
    proof = random.random()

    while valid_proof(last_proof, proof) is False:

        proof +=1

    return proof

def valid_proof(last_proof, proof):
    last_hash = hashlib.sha256(str(last_proof).encode()).hexdigest()
    guess = hashlib.sha256(str(proof).encode()).hexdigest()

    return guess[:last_proof["difficulty"]] == last_proof["difficulty"] * "0"

if __name__ == '__main__':
    node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"
    headers={"Authorization": "Token 103b91d44d0b4d88ee6d3a6fda97355cafc575b0"}

    while True:
        r = requests.get(url=node+"/last_proof", headers=headers)
        cooldown = r.json()["cooldown"]
        time.sleep(cooldown + .2)
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof}

        r = requests.post(url=node + "/mine", json=post_data)
        cooldown = r.json()["cooldown"]
        time.sleep(cooldown + .2)
        data = r.json()