import json
import time
import hashlib

class Block:
    def __init__(self, index, timestamp, credentials, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.credentials = credentials
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = None

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "credentials": self.credentials,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce
        }, sort_keys=True)

        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith(target):
                break
            self.nonce += 1


def create_genesis_block():
    genesis = Block(0, time.time(), [], "0")
    genesis.mine_block(3)
    return genesis

