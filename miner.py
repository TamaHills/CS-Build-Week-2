import hashlib
import requests
import json
import time
import sys

def proof_of_work(last_proof, difficulty):
    print("Starting proof search!")
    proof = 0

    last_hash = hashlib.sha256(f'{last_proof}'.encode()).hexdigest()

    while valid_proof(last_hash, last_proof, proof, difficulty) is False:
        proof +=1
    print(proof)
    return proof

def valid_proof(last_hash, last_proof, proof, difficulty):
    guess = hashlib.sha256(f"{last_proof}{proof}".encode()).hexdigest()

    if guess[:difficulty] == difficulty * "0":
        print("Found valid proof!")
        return True
    else:
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"
        headers={"Authorization": f"Token {input('token >>>')}"}

    while True:
        last_data = requests.get(url=node+"/last_proof", headers=headers)
        data = last_data.json()
        time.sleep(data["cooldown"])
        new_proof = proof_of_work(data["proof"], data["difficulty"])

        post_data = {"proof": new_proof}

        r = requests.post(url=node+"/mine", json=post_data, headers=headers)
        post_data = r.json()
        time.sleep(post_data["cooldown"])
        