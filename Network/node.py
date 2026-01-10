from Models import Blockchain

class Node:
    def __init__(self, node_id, blockchain: Blockchain):
        self.node_id = node_id
        self.blockchain = blockchain
        self.peers = set()

    def add_peer(self, peer_url):
        self.peers.add(peer_url)

    def receive_credential(self, credential):
        return self.blockchain.add_credential(credential)

    def should_accept_chain(self, incoming_chain):
        if len(incoming_chain) <= len(self.blockchain.chain):
            return False

        return self.blockchain.is_external_chain_valid(incoming_chain)

    def replace_chain(self, chain):
        self.blockchain.chain = chain
