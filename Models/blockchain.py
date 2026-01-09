from Models.block import Block, create_genesis_block
import time

class Blockchain:
    def __init__(self, difficulty=4):
        self.difficulty = difficulty
        self.chain = [create_genesis_block()]


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

# if __name__ == "__main__":
#     bc = Blockchain()

#     bc.add_block("Credential Hash: ABC123")
#     bc.add_block("Credential Hash: XYZ789")

#     for block in bc.chain:
#         print(vars(block))

#     print("Blockchain valid?", bc.is_chain_valid())
