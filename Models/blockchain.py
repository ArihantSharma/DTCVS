from . import Block, create_genesis_block, verify_signature, sign_data, generate_issuer_keys
import time

class Blockchain:
    def __init__(self, difficulty=4, block_size=2):
        self.difficulty = difficulty
        self.block_size = block_size
        self.chain = [create_genesis_block()]
        self.pending_credentials = []

    def add_credential(self, credential):
        self.pending_credentials.append(credential)

        if len(self.pending_credentials) >= self.block_size:
            self.mine_pending_credentials()

    def mine_pending_credentials(self):
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            credentials=self.pending_credentials.copy(),
            prev_hash=self.chain[-1].hash
        )

        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_credentials = []

    def issue_credential(blockchain, issuer_private_key, issuer_id, credential_hash):
        signature = sign_data(issuer_private_key, credential_hash)

        data = {
            "credential_hash": credential_hash,
            "issuer_id": issuer_id,
            "signature": signature
        }

        blockchain.add_block(data)

    def verify_credential(blockchain, issuer_public_key, credential_hash):
        for block in blockchain.chain:
            data = block.data
            if isinstance(data, dict) and data.get("credential_hash") == credential_hash:
                return verify_signature(
                    issuer_public_key,
                    credential_hash,
                    data["signature"]
                )
        return False

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.chain[-1]
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=time.time(),
            data=data,
            prev_hash=latest_block.hash
        )

        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            if curr.hash != curr.calculate_hash():
                return False

            if curr.prev_hash != prev.hash:
                return False

            if curr.hash[:self.difficulty] != "0" * self.difficulty:
                return False

        return True
    
    def is_external_chain_valid(self, chain: list[Block]):
        for i in range(1, len(chain)):
            curr = chain[i]
            prev = chain[i - 1]

            if curr.hash != curr.calculate_hash():
                return False

            if curr.prev_hash != prev.hash:
                return False

        return True

# if __name__ == "__main__":
#     bc = Blockchain(difficulty=3, block_size=2)

#     cred1 = {"credential_hash": "H1", "issuer_id": "UNI", "signature": "SIG1"}
#     cred2 = {"credential_hash": "H2", "issuer_id": "UNI", "signature": "SIG2"}
#     cred3 = {"credential_hash": "H3", "issuer_id": "UNI", "signature": "SIG3"}

#     bc.add_credential(cred1)
#     bc.add_credential(cred2)  # block mined here
#     bc.add_credential(cred3)
#     bc.add_credential(cred1)
#     bc.add_credential(cred2)  # block mined here
#     bc.add_credential(cred3)

#     for block in bc.chain:
#         print(block.index, block.credentials)

#     print("Chain valid?", bc.is_chain_valid())

