import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_votes = []
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'votes': self.current_votes,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_votes = []
        self.chain.append(block)
        return block

    def new_vote(self, voter, candidate):
        self.current_votes.append({
            'voter': voter,
            'candidate': candidate,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# Sample usage
if __name__ == '__main__':
    blockchain = Blockchain()
    blockchain.new_vote("Alice", "Bob")
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_block(proof)

    print("Current Blockchain:")
    print(json.dumps(blockchain.chain, indent=4))
