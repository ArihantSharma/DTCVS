class Node:
    def __init__(self, node_id, blockchain):
        self.node_id = node_id
        self.blockchain = blockchain
        self.peers = []

    def add_peer(self, peer_node):
        if peer_node not in self.peers:
            self.peers.append(peer_node)

    def receive_credential(self, credential):
        self.blockchain.add_credential(credential)

    def share_chain(self, peer):
        peer.receive_chain(self.blockchain.chain)

    def receive_chain(self, incoming_chain):
        if len(incoming_chain) <= len(self.blockchain.chain):
            return

        if not self.validate_external_chain(incoming_chain):
            return

        self.blockchain.chain = incoming_chain

    def validate_external_chain(self, chain):
        for i in range(1, len(chain)):
            curr = chain[i]
            prev = chain[i - 1]

            if curr.hash != curr.calculate_hash():
                return False

            if curr.prev_hash != prev.hash:
                return False

        return True
